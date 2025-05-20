import queue
import serial
import chardet
import serial.tools.list_ports
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal, QThread

from ADBPort import ADBPort

class ReaderThread(QThread):
    data_ready = pyqtSignal(str)

    def __init__(self, ser, data_queue, data_ui_queue, parent=None):
        """
        初始化ReaderThread类，用于读取串口数据。

        :param ser: 串口对象
        :param data_queue: 用于存储读取数据的队列
        :param data_ui_queue: 用于将数据传递给UI的队列
        :param parent: 父对象
        """
        super().__init__(parent)
        self.ser = ser
        self.data_queue = data_queue
        self.data_ui_queue = data_ui_queue
        self.running = True

    def run(self):
        """
        读取串口数据并将其放入队列中。
        """
        while self.running:
            if self.ser and self.ser.is_open:
                try:
                    while self.ser.in_waiting > 0:
                        data = self.ser.readline()
                        encoding = chardet.detect(data)['encoding']
                        if encoding:
                            data = data.decode(encoding)
                        else:
                            data = data.decode('utf-8', errors='replace')
                        # 将制表符转换为空格并去除末尾空白字符
                        data = data.replace('\t', '    ').rstrip()
                        if data:
                            self.data_queue.put(data)
                            self.data_ui_queue.put(data)
                            self.data_ready.emit(data)  # 发射信号，将数据发送到主线程
                except Exception as e:
                    self.data_ready.emit(f"读取数据失败: {str(e)}")  # 发射错误信号
                    self.running = False

    def stop(self):
        """
        停止读取线程。
        """
        self.running = False


class SerialPort(QObject):
    data_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self,data_ui_queue):
        """
        初始化SerialPort类，用于管理串口通信。
        """
        super().__init__()
        self.ser = None
        self.data_queue = queue.Queue()
        self.data_ui_queue = data_ui_queue
        self.reader_thread = None
        self.running = False
        self.adb_port = ADBPort(self.data_ui_queue,self.data_queue)

    def get_available_ports(self):
        """
        获取可用的串口列表。

        :return: 可用串口设备列表
        """
        ret = [port.device for port in serial.tools.list_ports.comports()]
        usb_devices = self.adb_port.list_usb_devices()
        for temp in usb_devices:
            ret.append('ADB:' + temp)

        return ret

    def open(self, port, baudrate, data_ui_queue):
        """
        打开指定的串口。

        :param port: 串口号
        :param baudrate: 波特率
        :param data_ui_queue: 用于将数据传递给UI的队列
        :return: 成功或失败的状态及消息
        """
        if "ADB:" in port:
            self.data_ui_queue = data_ui_queue
            self.adb_port.select_device(port.replace("ADB:",''))
            self.ser = 'ADB'
            self.running = True
            return True, "ADB成功打开"
        else:
            if self.ser and self.ser.is_open:
                self.close()
            try:
                self.ser = serial.Serial(port, baudrate, timeout=1)
                self.running = True
                self.reader_thread = ReaderThread(self.ser, self.data_queue, data_ui_queue)
                self.reader_thread.data_ready.connect(self.handle_data)  # 连接信号到槽函数
                self.reader_thread.start()
                self.data_ui_queue = data_ui_queue
                return True, "串口已成功打开"
            except Exception as e:
                return False, f"打开串口失败: {str(e)}"

    def close(self):
        """
        关闭串口。

        :return: 成功或失败的状态及消息
        """
        if self.ser and self.ser.is_open:
            self.running = False
            if self.reader_thread and self.reader_thread.isRunning():
                self.reader_thread.stop()
                self.reader_thread.wait()  # 等待线程结束
            self.ser.close()
            return True, "串口已成功关闭"
        return False, "串口未打开"

    def is_open(self):
        """
        检查串口是否已打开。

        :return: 如果串口已打开则返回True，否则返回False
        """
        return self.ser and self.ser.is_open

    def write(self, data):
        """
        向串口写入数据。

        :param data: 要发送的数据
        :return: 成功或失败的状态及消息
        """
        if self.ser == 'ADB':
            self.adb_port.run_adb_command(data.encode())
            return True, "数据已发送"
        else:
            try:
                if self.ser and self.ser.is_open:
                    self.ser.write(data.encode())
                    return True, "数据已发送"
                return False, "串口未打开"
            except Exception as e:
                self.close()
                return False, f"发送数据失败: {str(e)}"

    def read(self):
        """
        从数据队列中读取数据。

        :yield: 从队列中获取的数据
        """
        while not self.data_queue.empty():
            yield self.data_queue.get()

    def handle_data(self, data):
        """
        处理接收到的数据，根据数据内容发射相应的信号。

        :param data: 接收到的数据
        """
        if "读取数据失败:" in data:
            self.error_occurred.emit(data)
        else:
            self.data_received.emit(data)

    def show_message(self, message):
        """
        使用QMessageBox显示消息。
        
        :param message: 要显示的消息内容
        """
        # 使用QMessageBox显示消息
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("信息")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()