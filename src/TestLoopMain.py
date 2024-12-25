import subprocess
import time
import re
from datetime import datetime
import queue
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtCore

from IQHandle import IQHandle
import iniHandle

# 确定给定值所属的区间
def determine_interval(temp, intervals):
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    
    if temp < sorted_intervals[0][0]:
        return "小于所有区间"
    
    for interval in sorted_intervals:
        lower_bound, upper_bound = interval
        if lower_bound <= temp < upper_bound:
            return f"区间 [{lower_bound}, {upper_bound})"
    
    if temp >= sorted_intervals[-1][1]:
        return "大于所有区间"

# 调整发射功率类
class TxPowerAdjuster:
    def __init__(self, CriteriaAccuracy):
        self.iniHandle = iniHandle
        self.txLevelRange = [-100, 10]
        self.criteriaAccuracy = CriteriaAccuracy

        minStep = float(self.iniHandle.get_ini_value('DEFAULT', 'RX_Min_Step'))
        self.closeStep = []
        self.closeStep.append(minStep)
        while True:
            minStep *= 5 
            self.closeStep.append(minStep)
            if minStep >= 10:
                break
        print(self.closeStep)
        self.closeIndex = 0

    # 根据当前测量结果调整发射功率
    def adjustTxPower(self, txLevel, direction, accuracy):
        self.txLevelRange.sort()
        self.closeStep = sorted(self.closeStep, reverse=True)

        self.closeIndex = 0
        rangeWidth = self.txLevelRange[1] - self.txLevelRange[0]
        for temp in self.closeStep:
            if rangeWidth <= temp:
                self.closeIndex += 1

        if accuracy > self.criteriaAccuracy:
            if direction == -1:
                self.txLevelRange[1] = txLevel
            elif direction == 1:
                self.txLevelRange[0] = txLevel
            nextTxLevel = txLevel + self.closeStep[self.closeIndex] * direction
            
        elif accuracy < self.criteriaAccuracy:
            if direction == -1:
                self.txLevelRange[0] = txLevel
            elif direction == 1:
                self.txLevelRange[1] = txLevel
            nextTxLevel = txLevel - self.closeStep[self.closeIndex] * direction

        if nextTxLevel < self.txLevelRange[0]:
            nextTxLevel = self.txLevelRange[0]
        elif nextTxLevel > self.txLevelRange[1]:
            nextTxLevel = self.txLevelRange[1]

        if self.txLevelRange[1] - self.txLevelRange[0] <= min(self.closeStep):
            nextTxLevel = 999

        print(f"当前范围: {self.txLevelRange}, 下一个测量值: {nextTxLevel}")
        return nextTxLevel

# 测试工作线程类
class TestWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __del__(self):
        self.running = False
        self.finished.emit()
        
    def __init__(self, serial_port, fileHandle, debugDataQueue, testLoopDataQueue, iqDataQueue, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.running = False
        self.serial_port = serial_port
        self.fileHandle = fileHandle
        self.debugDataQueue = debugDataQueue
        self.testLoopDataQueue = testLoopDataQueue
        self.iqDataQueue = iqDataQueue
        self.IQHandle = IQHandle(iqDataQueue)
        self.iniHandle = iniHandle
        self.paused = False
        
    def pauseTest(self):
        self.paused = not self.paused
        if self.paused:
            self.testLoopDataQueue.put("测试暂停...")
        else:
            self.testLoopDataQueue.put("测试继续...")
    def stopTest(self):
        self.running = False
        self.testLoopDataQueue.put("停止测试...")
        self.testLoopDataQueue.put("等待测试线程结束...")
        self.wait()
        try:
            if self.fileHandle.save_test_result():
                self.testLoopDataQueue.put(f"测试结果保存成功")
        except IOError as e:
            self.testLoopDataQueue.put(f"{e}")
        self.testLoopDataQueue.put("测试线程已结束...")

    def run(self):
        self.running = True
        self.mainTestLoop()
        self.running = False
        self.finished.emit()

    # 获取测试参数
    def getTestParameter(self, testItem):
        if "11b" in testItem['testItemName']:
            modulation = 'DSSS'
        else:
            modulation = 'OFDM'

        if "20M" in testItem['testItemName']:
            bandWidth = 20
        elif "40M" in testItem['testItemName']:
            bandWidth = 40
        elif "80M" in testItem['testItemName']:
            bandWidth = 80
        else:
            self.iqDataQueue.put("未找到测试带宽...........")
            return False

        match = re.search(r'CH(\d+)', testItem['testItemName'])
        if match:
            channel = int(match.group(1))
        else:
            self.iqDataQueue.put("未找到测试信道...........")
            return False

        freq = testItem['Frequency']
        if freq / 5000 > 1:
            bandType = '5G'
        else:
            bandType = '2G4'

        return modulation, bandWidth, int(channel), int(freq), bandType

    # 执行WIFI TX测试
    def wifiTxTest(self, testItem):
        modulation, bandWidth, channel, freq, bandType = self.getTestParameter(testItem)
        self.iqDataQueue.put(f"modulation={modulation},bandWidth={bandWidth}M,channel=CH{channel},freq={freq}")

        for _ in range(3):  # 测试3次
            if not self.running:
                return
            while self.paused:
                QThread.msleep(100)

            waitTime = self.iniHandle.get_ini_value(testItem['socName'], 'TX_WAIT_TIME')
            time.sleep(float(waitTime))

            self.IQHandle.wifi_tx_measure_config(channel=channel, band_type=bandType, modulation=modulation, bandwidth=bandWidth, frequency=freq)  #channel=36, band_type='5G', modulation='OFDM', bandwidth=20, frequency=5180
            try:
                power, evm, freqError, minMask = self.IQHandle.get_all_wifi_tx_measure_results(modulation=modulation)
            except Exception as e:
                self.iqDataQueue.put(f"获取测量结果失败: {e}")
                power, evm, freqError, minMask = '_','_','_','_'
                continue
            
            self.iqDataQueue.put(f"powerTestValue={power},freErrorTestValue={freqError},evmTestValue={evm},maskMargin={minMask}")

            try:
                if (testItem['powerLowerLimit'] <= power <= testItem['powerUpperLimit'] and
                        testItem['freErrorLowerLimit'] <= freqError <= testItem['freErrorUpperLimit'] and
                        testItem['evmLowerLimit'] <= evm <= testItem['evmUpperLimit']):
                    break
                else:
                    self.iqDataQueue.put("测试失败，重新测试...........")

            except Exception as e:
                self.iqDataQueue.put(f"测结果存在问题: {e}")
                continue

        
        testItem['powerTestValue'] = power
        testItem['freErrorTestValue'] = freqError
        testItem['evmTestValue'] = evm
        testItem['maskMargin'] = minMask
        return True

    # 执行WIFI RX测试
    def wifiRxTest(self, testItem, direction):
        accuracy = 100
        testResult = -80

        modulation = '_'.join(testItem['testItemName'].split('_')[2:5])

        criteriaAccuracy = float(self.iniHandle.get_ini_value('DEFAULT', 'RX_Criteria_Accuracy_'+modulation))

        if direction == 1:
            initTxLevel = float(self.iniHandle.get_ini_value('DEFAULT', 'RX_Init_Value_'+modulation).split(',')[0])
        elif direction == -1:
            initTxLevel = float(self.iniHandle.get_ini_value('DEFAULT', 'RX_Init_Value_'+modulation).split(',')[1])
        txLevel = initTxLevel
        nextTxLevel = initTxLevel

        self.TxPowerAdjuster = TxPowerAdjuster(criteriaAccuracy)

        clearCMD = self.iniHandle.get_ini_value(testItem['socName'], 'RX_ClEAR_CMD')
        getBufferCMD = self.iniHandle.get_ini_value(testItem['socName'], 'RX_GETBUFFER_CMD')

        try:
            getCorrectValueExpression = self.iniHandle.get_ini_value(testItem['socName'], 'RX_GETCORRECTVALUE_Expression')
        except Exception as e:
            getCorrectValueExpression = None

        try:
            getFailValueExpression = self.iniHandle.get_ini_value(testItem['socName'], 'RX_GETFAILVALUE_Expression')
        except Exception as e:
            getFailValueExpression = None

        try:
            getTotalValueExpression = self.iniHandle.get_ini_value(testItem['socName'], 'RX_GETETOTALVALUE_Expression')
        except Exception as e:
            getTotalValueExpression = None

        waveFile = self.iniHandle.get_ini_value(testItem['socName'], 'IQ_WAVA_FILE_PATH') + self.iniHandle.get_ini_value("DEFAULT", f"WaveFile_{modulation}")

        self.IQHandle.wifi_rx_measure_config(waveFile, frequency=testItem['Frequency'])  #wave_file, frequency=5180):

        testCounts = 0 #测试次数
        try:
            maxTestCounts = int(self.iniHandle.get_ini_value('DEFAULT', 'RX_MAX_TESTCOUNT'))
        except Exception as e:
            maxTestCounts = 20
        while True:
            if not self.running:
                return
            while self.paused:
                QThread.msleep(100)

            testCounts = testCounts + 1
            if testCounts <= maxTestCounts: # 测试次数小于最大次数

                self.serial_port.write(clearCMD + '\r\n')

                self.IQHandle.wifi_rx_send_packets(waveFile, tx_level=str(nextTxLevel))  #wave_file, tx_level='-40'):
                txLevel = nextTxLevel

                while not self.serial_port.data_queue.empty():
                    self.serial_port.data_queue.get_nowait()

                self.serial_port.write(getBufferCMD + '\r\n')

                try:
                    waitTime = self.iniHandle.get_ini_value(testItem['socName'], 'RX_WAIT_TIME')
                except Exception as e:
                    waitTime = 1

                time.sleep(float(waitTime))

                ret = ""
                while not self.serial_port.data_queue.empty():
                    try:
                        data = self.serial_port.data_queue.get_nowait()
                        ret += str(data) + "$$$"
                    except queue.Empty:
                        break

                correctValue = int(re.search(getCorrectValueExpression, ret).group(1))
                accuracy = correctValue / 1000 * 100
                if accuracy > 100:
                    accuracy = 100

                self.iqDataQueue.put(f"当前发射功率:{txLevel},收包正确率:{accuracy}")

                if accuracy > criteriaAccuracy:
                    testResult = txLevel
                    if txLevel == 0:
                        break

                nextTxLevel = self.TxPowerAdjuster.adjustTxPower(txLevel, direction, accuracy)
                if nextTxLevel == 999:
                    break
                if nextTxLevel > 0:
                    nextTxLevel = 0
        
            else:
                self.iqDataQueue.put(f"达到最大测试次数:{testCounts}次，测试结束....")
                break
        
        try:
            testResult == 10
        except Exception as e:
            testResult = '-'
            self.iqDataQueue.put(f"未找到任何测试结果大于{criteriaAccuracy}")
            return False
        if direction == 1:
            self.iqDataQueue.put(f"最大接收电平为:{testResult}")
            testItem['minReceiveLevelTestValue'] = testResult
        elif direction == -1:
            self.iqDataQueue.put(f"最小接收电平为:{testResult}")
            testItem['maxReceiveLevelTestValue'] = testResult
    def ping_ip(self, ip):
        """
        使用系统命令ping指定的IP地址，检查网络连通性。
        
        :param ip: 要ping的IP地址
        :return: 如果IP地址可达返回True，否则返回False
        """
        response = subprocess.run(['ping', '-n', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return response.returncode == 0
    # 主测试循环
    def mainTestLoop(self):
        try:
            for attempt in range(10):
                if not self.running:
                    return True
                while self.paused:
                    QThread.msleep(100)

                if self.ping_ip(self.IQHandle.ip_address):
                    ret = self.IQHandle.connect()
                    break
                else:
                    self.iqDataQueue.put(f"IP {self.IQHandle.ip_address} 等待ping通")
        except Exception as e:
            self.iqDataQueue.put("iQ仪器连接出现意外............" + str(e))
            return False
        
        try:
            self.iqDataQueue.put(f"iQ仪器连接成功...{ret}")
        except Exception as e:
            self.iqDataQueue.put("iQ仪器连接失败............" + str(e))
            return False
        
        self.IQHandle.reset()
        self.IQHandle.port_config(port='RF1A', port_mode='VSA&VSG')

        startTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.testLoopDataQueue.put(f"开始测试...{startTime}")

        self.fileHandle.test_item_Num = 0
        for testItem in self.fileHandle.test_item_list:
            if not self.running:
                return True
            while self.paused:
                QThread.msleep(100)

            if testItem['isExec'] == 'Y':
                self.iqDataQueue.put("\r\nTest -> " + testItem['testType'] + "<->" + testItem['testItemName'])

                execCmdList = testItem['execCmd'].split('\n')
                for execCmd in execCmdList:
                    if not self.running:
                        return True
                    try:
                        self.serial_port.write(execCmd + '\r\n')
                        time.sleep(0.1)
                    except Exception as e:
                        self.debugDataQueue.put("发送命令失败....测试停止...." + str(e))
                        self.serial_port.close()
                        self.running = False
                        return

                if testItem['isRecord'] == 'Y':
                    test_type = testItem['testType']
                    soc_name = testItem['socName']

                    if test_type == 'WIFI_TX':
                        self.wifiTxTest(testItem)
                    elif test_type == 'WIFI_RX':
                        if soc_name == 'RTL8822CS':
                            self.iqDataQueue.put("测试最大接收电平...")
                            self.wifiRxTest(testItem, 1)
                            self.iqDataQueue.put("测试最小接收电平...")
                            self.wifiRxTest(testItem, -1)
                    elif test_type == 'BT_TX':
                        print('BT_TX')
                    elif test_type == 'BT_RX':
                        if soc_name == 'RTL8822CS':
                            print('RTL8822CS BT_RX')
                    #保存测试结果
                    try:
                        if self.fileHandle.save_test_result():
                            self.testLoopDataQueue.put(f"测试结果保存成功")
                    except Exception as e:
                        self.testLoopDataQueue.put(f"测试结果保存失败...{e}")

            self.fileHandle.test_item_Num = self.fileHandle.test_item_Num + 1

        self.fileHandle.test_item_Num = 0
        stoptTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.testLoopDataQueue.put(f"结束测试...{stoptTime}")
        

            
        self.IQHandle.disconnect()
        return True

# 测试主类
class TestLoopMain(QObject):
    def __init__(self, serial_port, fileHandle, debugDataQueue, testLoopDataQueue, iqDataQueue, parent=None):
        super().__init__()
        self.parent = parent
        self.serial_port = serial_port
        self.fileHandle = fileHandle
        self.debugDataQueue = debugDataQueue
        self.testLoopDataQueue = testLoopDataQueue
        self.iqDataQueue = iqDataQueue
        self.debugDataQueue.put("开始测试")
        self.testLoopDataQueue.put("开始测试")
        self.iqDataQueue.put("开始测试")
        self.worker = None

    # 开始测试
    def startTest(self):
        if not self.fileHandle.test_item_list:
            self.testLoopDataQueue.put("请先加载测试项目............")
            return False

        if not self.serial_port.is_open():
            self.debugDataQueue.put("请先打开串口............")
            return False

        if not self.fileHandle.open_test_result_file():
            self.testLoopDataQueue.put("新建测试结果文件出现意外............")
            return False

        self.running = True
        self.worker = TestWorker(self.serial_port, self.fileHandle, self.debugDataQueue, self.testLoopDataQueue, self.iqDataQueue)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()
        return True
    
    # 测试结束后的处理
    def on_worker_finished(self):
        self.parent.ui.startButton.setEnabled(True)
        self.parent.ui.stopButton.setEnabled(False)
        self.parent.ui.pauseButton.setEnabled(False)

    # 暂停测试
    def pauseTest(self):
        _translate = QtCore.QCoreApplication.translate
        self.worker.pauseTest()
        if self.worker.paused:
            self.parent.ui.stopButton.setEnabled(False)
            self.parent.ui.pauseButton.setText(_translate("MainWindow", "继续"))
        else:
            self.parent.ui.stopButton.setEnabled(True)
            self.parent.ui.pauseButton.setText(_translate("MainWindow", "暂停"))
    # 停止测试
    def stopTest(self):
        self.worker.stopTest()

    def __del__(self):
        if self.worker and self.worker.isRunning():
            self.worker.running = False
            self.worker.quit()
            self.worker.wait()