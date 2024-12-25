import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
import queue
import hashlib
import wmi
import os
import datetime
from PyQt5.QtCore import QItemSelectionModel
import chardet

sys.path.append('./src')
sys.path.append('./GUI')

from SerialPort import SerialPort
from FileHandle import FileHandle
from TestLoopMain import TestLoopMain
from rfCKR_MainUI import Ui_MainWindow

class rfCKR(QMainWindow):
    data_received = pyqtSignal(str)
    
    def __init__(self,file_handle):
        super().__init__()
        self.serial_port = SerialPort()  
        self.fileHandle = file_handle

        # 初始化队列
        self.debugDataQueue = queue.Queue()
        self.testLoopDataQueue = queue.Queue()
        self.iqDataQueue = queue.Queue()
        
        self.initUI()
        self.setupTimers()
        self.initializeQueues()
        self.testLoopMain = TestLoopMain(self.serial_port, self.fileHandle, self.debugDataQueue, self.testLoopDataQueue, self.iqDataQueue, self)

        # 创建log文件夹
        self.log_folder = "./log"
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        # 生成日志文件名
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.debugDataLogFilename = f"{self.log_folder}/debugData_{current_time}.txt"
        self.testLoopDataLogFilename = f"{self.log_folder}/testLoopData_{current_time}.txt"
        self.iqDataLogFilename = f"{self.log_folder}/iqData_{current_time}.txt"
    def initUI(self):
        # 初始化用户界面
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('rfCKR-V02 Copyright © 2024 #EE_Lixin. All Rights Reserved.')
        self.setWindowIcon(QIcon('./GUI/ico/rfCKR.jpg'))
        self.ui.SDMC_Logo.setStyleSheet("""QPushButton {border-image: url('./GUI/ico/SDMC_Logo.png') 0 0 0 0 stretch stretch;}""")

        # 绑定信号事件
        self.ui.loadButton.clicked.connect(self.loadTestItem)
        self.ui.debugInputEdit.returnPressed.connect(self.debugSendcommand)
        self.ui.openSerButton.clicked.connect(self.openSerial)
        self.ui.closeSerButton.clicked.connect(self.closeSerial)
        self.ui.startButton.clicked.connect(self.startTest)
        self.ui.pauseButton.clicked.connect(self.pauseTest)
        self.ui.stopButton.clicked.connect(self.stoptTest)
        
        # 初始化控件状态
        self.ui.pauseButton.setEnabled(False)
        self.ui.stopButton.setEnabled(False)
        self.ui.closeSerButton.setEnabled(False)

        # 获取串口列表
        self.ui.comNumComboBox.clear()
        self.ui.baudRateComboBox.clear()
        self.ui.comNumComboBox.addItems(self.serial_port.get_available_ports())
        self.ui.baudRateComboBox.addItems(['921600', '115200'])

        # 设置Log窗口为只读
        self.ui.debugConsoleEdit.setReadOnly(True)
        self.ui.cmdEdit.setReadOnly(True)
        self.ui.iqLogEdit.setReadOnly(True)

    def setupTimers(self):
        # 设置定时器，每5毫秒遍历一次数据
        self.read_timer = QTimer(self)
        self.read_timer.timeout.connect(self.QtimerHandle)
        self.read_timer.start(5)

    def initializeQueues(self):
        # 初始化队列数据
        self.debugDataQueue.put("串口打印信息")
        self.testLoopDataQueue.put("测试任务打印信息")
        self.iqDataQueue.put("iQ仪器打印信息")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.ui.verticalWidget.resize(self.size())

    def updateLogWindow(self, data_queue, log_edit,log_filename):
        # 更新单个Log窗口
        while not data_queue.empty():
            logItem = data_queue.get_nowait()

            with open(log_filename, 'a', encoding='utf-8', errors='ignore') as file:
                file.write(f"{logItem}\n")
            
            log_edit.append(logItem)

    def QtimerHandle(self):
        # 更新各个Log窗口
        self.updateLogWindow(self.debugDataQueue, self.ui.debugConsoleEdit,self.debugDataLogFilename)
        self.updateLogWindow(self.testLoopDataQueue, self.ui.cmdEdit,self.testLoopDataLogFilename)
        self.updateLogWindow(self.iqDataQueue, self.ui.iqLogEdit,self.iqDataLogFilename)
        # 高亮当前行
        self.highlightRowInTestListView(self.fileHandle.test_item_Num) 
        
    def debugSendcommand(self):
        # 发送调试命令
        command = self.ui.debugInputEdit.text()
        if command:
            success, message = self.serial_port.write(command + '\n')
            if not success:
                self.show_message(message)

    def openSerial(self):
        # 打开串口
        success, message = self.serial_port.open(self.ui.comNumComboBox.currentText(), int(self.ui.baudRateComboBox.currentText()), self.debugDataQueue)
        self.debugDataQueue.put(message)
        if success:
            self.ui.closeSerButton.setEnabled(True)
            self.ui.openSerButton.setEnabled(False)

    def closeSerial(self):
        # 关闭串口
        success, message = self.serial_port.close()
        self.debugDataQueue.put(message)
        self.ui.closeSerButton.setEnabled(False)
        self.ui.openSerButton.setEnabled(True)

    def highlightRowInTestListView(self, row_index):
        # 获取模型
        model = self.ui.testListView.model()
        # 检查 testListView 中是否有内容
        if model is None or model.rowCount() == 0:
            return  # 如果没有内容，直接退出函数

        # 确保行索引在有效范围内
        if 0 <= row_index < self.ui.testListView.model().rowCount():
            # 获取模型
            model = self.ui.testListView.model()
            # 创建一个选择模型
            selection_model = self.ui.testListView.selectionModel()
            # 创建一个选择范围
            index = model.index(row_index, 0)
            # 清除之前的高亮
            selection_model.clearSelection()
            # 选择并高亮指定行
            selection_model.select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def loadTestItem(self):
        # 加载测试项目并显示在列表中
        self.fileHandle.load_test_item()
        model = QStandardItemModel()
        for line in self.fileHandle.test_item_list:
            testItemName = line['testItemName']
            if testItemName:
                list_item = QStandardItem(testItemName)
                model.appendRow(list_item)
        self.ui.testListView.setModel(model)
        
    def startTest(self):
        # 开始测试
        if self.testLoopMain.startTest():
            self.ui.startButton.setEnabled(False)
            self.ui.pauseButton.setEnabled(True)
            self.ui.stopButton.setEnabled(True)

    def pauseTest(self):
        # 暂停测试
        self.testLoopMain.pauseTest()

    def stoptTest(self):
        # 停止测试
        self.testLoopMain.stopTest()
        
    def show_message(self, message):
        # 显示消息对话框
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("信息")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()


fileHandle = FileHandle()

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    if fileHandle.result_file_df is not None:
        fileHandle.save_test_result()


    print("未捕获的异常", file=sys.stderr)
    print("类型: ", exc_type.__name__, file=sys.stderr)
    print("值: ", exc_value, file=sys.stderr)
    print("回溯: ", file=sys.stderr)
    traceback.print_tb(exc_traceback, file=sys.stderr)

    # 将异常写入日志文件
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"./log/error_log_{current_time}.txt"
    with open(log_filename, "w") as f:
        f.write("未捕获的异常\n")
        f.write(f"类型: {exc_type.__name__}\n")
        f.write(f"值: {exc_value}\n")
        f.write("回溯:\n")
        traceback.print_tb(exc_traceback, file=f)

    # 获取日志文件的绝对路径
    log_file_path = os.path.abspath(log_filename)

    # 使用 QMessageBox 提示用户
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(f"程序遇到未捕获的异常，请查看日志文件。\n {log_file_path}")
    msg_box.setWindowTitle("错误")
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

    # 退出程序
    os.exit(1)

if __name__ == '__main__':
    sys.excepthook = handle_exception
    print("程序启动中..............")
    # 根据硬盘序列号判断是否允许运行
    disk_serial = wmi.WMI().Win32_DiskDrive()[0].SerialNumber
    allowed_serials = ['58bafcd4d98eaaa4821197230711e4e8', '97bb81b840885efbcac7d471d2a37589'] #测试电脑,lixin小电脑
    if hashlib.md5(disk_serial.encode('utf-8')).hexdigest() in allowed_serials:
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        tool = rfCKR(fileHandle)
        tool.show()
        sys.exit(app.exec_())
    else:
        print("hello world")

