import subprocess
import re
import shlex
from PyQt6.QtCore import pyqtSignal, QThread

class ADBCommandThread(QThread):
    """此线程用于异步执行ADB命令。"""
    data_ready = pyqtSignal(str)  # 信号，当有数据时发出
    command_finished = pyqtSignal(bool, str, str) # 信号，参数：success (bool), stdout (str), stderr (str)

    def __init__(self, command_args, selected_device, data_ui_queue, data_queue, parent=None):
        super().__init__(parent)
        self.command_args = command_args
        self.selected_device = selected_device
        self.data_ui_queue = data_ui_queue
        self.data_queue = data_queue
        self.running = True

    def run(self):
        """执行ADB命令并处理输出。"""
        if not self.selected_device:
            self.data_ui_queue.put("错误：线程执行时未选择设备。")
            self.command_finished.emit(False, "", "错误：线程执行时未选择设备。")
            return

        processed_args = []
        if isinstance(self.command_args, list):
            processed_args = self.command_args
        elif isinstance(self.command_args, bytes):
            try:
                decoded_args = self.command_args.decode('utf-8')
                processed_args = shlex.split(decoded_args)
            except UnicodeDecodeError:
                error_msg = f"错误：无法将命令参数解码为 UTF-8: {self.command_args!r}"
                self.data_ui_queue.put(error_msg)
                self.command_finished.emit(False, "", error_msg)
                return
            except Exception as e:
                error_msg = f"错误：解析命令参数时出错: {e}"
                self.data_ui_queue.put(error_msg)
                self.command_finished.emit(False, "", error_msg)
                return
        elif isinstance(self.command_args, str):
            try:
                processed_args = shlex.split(self.command_args)
            except Exception as e:
                error_msg = f"错误：解析命令参数时出错: {e}"
                self.data_ui_queue.put(error_msg)
                self.command_finished.emit(False, "", error_msg)
                return
        else:
            error_msg = f"错误：不支持的命令参数类型: {type(self.command_args)}"
            self.data_ui_queue.put(error_msg)
            self.command_finished.emit(False, "", error_msg)
            return

        if processed_args == ['su']:
            full_command = ['adb', '-s', self.selected_device, 'root']
        else:
            full_command = ['adb', '-s', self.selected_device, 'shell'] + processed_args

        try:
            self.data_ui_queue.put(f"线程执行命令: {' '.join(full_command)}")
            # 使用 Popen 进行异步执行
            process = subprocess.Popen(full_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
            
            stdout_list = []
            # 实时读取stdout
            if process.stdout:
                for line in iter(process.stdout.readline, ''):
                    if not self.running:
                        process.terminate() # 尝试终止进程
                        process.wait()
                        self.data_ui_queue.put("命令被用户中止")
                        self.command_finished.emit(False, "".join(stdout_list), "命令已中止")
                        return
                    line = line.strip()
                    if line:
                        stdout_list.append(line + '\n')
                        self.data_queue.put(line)
                        self.data_ui_queue.put(f"实时输出: {line}")
                        self.data_ready.emit(line)
                process.stdout.close()
            
            # 等待进程结束并获取stderr
            stderr_output = ""
            if process.stderr:
                stderr_output = process.stderr.read()
                process.stderr.close()

            return_code = process.wait()
            stdout_full = "".join(stdout_list)

            if return_code != 0:
                error_detail = f"命令执行出错，返回码: {return_code}. Stderr: {stderr_output.strip()}"
                self.data_ui_queue.put(error_detail)
                self.command_finished.emit(False, stdout_full, stderr_output.strip() or error_detail)
            else:
                self.data_ui_queue.put("命令执行完成")
                self.command_finished.emit(True, stdout_full, stderr_output.strip())

        except FileNotFoundError:
            error_msg = "错误：未找到 'adb' 命令。请确保 ADB 已安装并添加到系统 PATH 中。"
            self.data_ui_queue.put(error_msg)
            self.command_finished.emit(False, "", "ADB not found")
        except Exception as e:
            error_msg = f"执行 ADB 命令时发生意外错误: {e}"
            self.data_ui_queue.put(error_msg)
            self.command_finished.emit(False, "", str(e))

    def stop(self):
        self.running = False

class ADBPort:
    """此类用于通过命令行与 ADB 交互，管理 USB 连接的设备。"""

    def __init__(self, data_ui_queue, data_queue):
        self.selected_device = None
        self.data_ui_queue = data_ui_queue
        self.data_queue = data_queue

    def _execute_command(self, command_args):
        """执行给定的 ADB 命令并处理常见的错误。"""
        try:
            self.data_ui_queue.put(f"执行命令: {' '.join(command_args)}")
            result = subprocess.run(command_args, capture_output=True, text=True, check=True, encoding='utf-8')
            # self.data_ui_queue.put(f"命令输出:\n{result.stdout}") # 根据需要取消注释以查看详细输出
            return result.stdout, result.stderr
        except FileNotFoundError:
            self.data_ui_queue.put("错误：未找到 'adb' 命令。请确保 ADB 已安装并添加到系统 PATH 中。")
            return None, "ADB not found"
        except subprocess.CalledProcessError as e:
            self.data_ui_queue.put(f"执行 ADB 命令时出错: {e}")
            self.data_ui_queue.put(f"错误输出: {e.stderr}")
            return e.stdout, e.stderr

    def list_usb_devices(self):
        """列出通过 USB 连接的 ADB 设备。"""
        output, error = self._execute_command(['adb', 'devices'])
        if error:
            # 错误已在 _execute_command 中打印
            return []
        if output is None:
            return []

        devices = []
        lines = output.strip().split('\n')
        if len(lines) > 1:
            for line in lines[1:]:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    device_id, status = parts
                    if ':' not in device_id and status == 'device':
                        devices.append(device_id)
        
        if not devices:
            self.data_ui_queue.put("未找到通过 USB 连接的 ADB 设备。")

        return devices

    def select_device(self, device_id):
        """选择要进行通信的特定 ADB 设备。"""
        available_devices = self.list_usb_devices()
        if device_id in available_devices:
            self.selected_device = device_id
            self.data_ui_queue.put(f"已选择设备: {self.selected_device}")
            return True
        else:
            self.data_ui_queue.put(f"错误：设备 '{device_id}' 不可用或不是有效的 USB 设备。")
            self.selected_device = None
            return False

    def get_selected_device(self):
        """获取当前选择的设备 ID。"""
        return self.selected_device

    def __init__(self, data_ui_queue, data_queue):
        self.selected_device = None
        self.data_ui_queue = data_ui_queue
        self.data_queue = data_queue
        self.current_command_thread = None # 用于跟踪当前运行的命令线程

    def run_adb_command(self, command_args):
        """在选定的设备上执行 ADB 命令。"""
        if not self.selected_device:
            self.data_ui_queue.put("错误：请先选择一个设备。")
            # 可以考虑发出一个信号或返回一个特定的错误状态
            return False # 表示命令未启动

        if self.current_command_thread and self.current_command_thread.isRunning():
            self.data_ui_queue.put("错误：已有ADB命令正在运行,等待完成...")
            while self.current_command_thread and self.current_command_thread.isRunning():
                 QThread.msleep(100)

        # 创建并启动线程
        self.current_command_thread = ADBCommandThread(command_args, self.selected_device, self.data_ui_queue, self.data_queue)
        self.current_command_thread.start()
        self.data_ui_queue.put(f"ADB命令 '{str(command_args)}' 已异步启动。")
        return True # 表示命令已成功启动

    def stop_current_command(self):
        """停止当前正在运行的ADB命令（如果存在）。"""
        if self.current_command_thread and self.current_command_thread.isRunning():
            self.data_ui_queue.put("正在尝试停止当前ADB命令...")
            self.current_command_thread.stop()
            return True
        else:
            self.data_ui_queue.put("没有正在运行的ADB命令可以停止。")
            return False

