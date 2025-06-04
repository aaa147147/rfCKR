import subprocess
import re
import shlex

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

    def run_adb_command(self, command_args):
        """在选定的设备上执行 ADB 命令。"""
        if not self.selected_device:
            self.data_ui_queue.put("错误：请先选择一个设备。")
            return None

        # Ensure command_args is a list of strings
        processed_args = []
        if isinstance(command_args, list):
            processed_args = command_args
        elif isinstance(command_args, bytes):
            try:
                decoded_args = command_args.decode('utf-8')
                processed_args = shlex.split(decoded_args) # Use shlex for robust splitting
            except UnicodeDecodeError:
                 self.data_ui_queue.put(f"错误：无法将命令参数解码为 UTF-8: {command_args!r}")
                 return None
            except Exception as e:
                 self.data_ui_queue.put(f"错误：解析命令参数时出错: {e}")
                 return None
        elif isinstance(command_args, str):
             try:
                 processed_args = shlex.split(command_args) # Use shlex for robust splitting
             except Exception as e:
                 self.data_ui_queue.put(f"错误：解析命令参数时出错: {e}")
                 return None
        else:
            self.data_ui_queue.put(f"错误：不支持的命令参数类型: {type(command_args)}")
            return None
        #  单独处理 su 命令
        if processed_args == ['su']:
            full_command = ['adb', '-s', self.selected_device ] + ['root'] # Concatenate lists
        else:
            full_command = ['adb', '-s', self.selected_device , 'shell'] + processed_args # Concatenate lists
        stdout, stderr = self._execute_command(full_command)

        if stderr and "ADB not found" in stderr:
            # ADB 未找到的错误已处理
            return None 
        elif stderr:
            # 其他命令执行错误，返回 stderr
            self.data_ui_queue.put(f"命令输出 (stdout):\n{stdout}") # 即使出错也可能需要看stdout
            return stderr
        else:
            # 成功执行，返回 stdout
            self.data_ui_queue.put(f"命令输出:\n{stdout}")
            self.data_queue.put(stdout)
            return stdout

