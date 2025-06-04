import litepoint
import iniHandle
from PyQt6.QtWidgets import QMessageBox
import time
from PyQt6.QtCore import QObject, QThread, pyqtSignal

class IQHandle:
    def __init__(self, iq_data_queue, cable_loss_list):
        """
        初始化IQHandle类，设置LitePoint仪器对象，读取配置文件中的IP地址，并初始化数据队列。
        
        :param iq_data_queue: 用于传递数据的队列对象
        """
        self.IQ = litepoint._LitePointKeywords()
        self.tx_mea_config = (None, None, None, None)  # 保存上一次的发射测试配置
        self.rx_mea_config = None  # 保存上一次的接收测试配置
        
        self.ip_address = iniHandle.get_ini_value('DEFAULT', 'IQ_LITE_POINT_IP')
        self.SCPI_timeout = float(iniHandle.get_ini_value('DEFAULT', 'IQ_LITE_TIMEOUT'))
        if not self.ip_address:
            self.ip_address = '192.168.100.254'
        
        self.iq_data_queue = iq_data_queue
        self.iq_data_queue.put(f'IQ_LITE_POINT_IP:{self.ip_address}')
        self.cable_loss_list = cable_loss_list
    def connect(self):
        self.iq_data_queue.put("连接iQ仪器...")
        self.IQ.open_lite_point_connection(self.ip_address,timeout=self.SCPI_timeout)
        return self.IQ.send_raw_command("*IDN?")

    def reset(self):
        """复位LitePoint仪器"""
        self.iq_data_queue.put(f'复位仪器')
        self.IQ.send_raw_command('SYS;*CLS;*RST;FORM:READ:DATA ASC')
        

    def disconnect(self):
        """断开与LitePoint仪器的连接"""
        try:
            self.IQ.close_lite_point_connection()
        except Exception as e:
            self.iq_data_queue.put(f"断开连接失败：{e}")

    def port_config(self, port='RF1A', port_mode='VSA&VSG'):
            """
            配置LitePoint仪器的端口设置，包括加载线损文件并应用到指定端口。
            
            :param port: 端口号，默认为'RF1A'
            :param port_mode: 端口模式，默认为'VSA&VSG'
            """
            print(f'仪器端口设置')
            self.iq_data_queue.put(f'仪器端口设置')
            # 配置端口
            self.IQ.send_raw_command('''ROUT1;PORT:RES:ADD RF1A,VSA1''')
            self.IQ.send_raw_command('''ROUT1;PORT:RES:ADD RF1A,VSG1''')    

            # 清空现有线损设置
            self.IQ.send_raw_command('MEM:TABL:LOSS:DEL:ALL;')

            # 发送新的线损表
            command = f'MEM:TABLE "RF_TABLE1";MEM:TABLE:DEFINE "FREQ,LOSS";'
            command += 'MEMory:TABLe:INSert:POINt ' + ', '.join([f"{item['fre']}MHz,{item['loss']:.2f}" for item in self.cable_loss_list])
            self.IQ.send_raw_command(command)

            # 应用线损表到指定端口
            self.IQ.send_raw_command('''TABL:STOR;VSA1;RFC:USE "RF_TABLE1",RF1A;RFC:STAT ON,RF1A''')
            self.IQ.send_raw_command('''TABL:STOR;VSG1;RFC:USE "RF_TABLE1",RF1A;RFC:STAT ON,RF1A''')

    def wifi_tx_measure_config(self, channel=36, band_type='5G', modulation='OFDM',  mcs_value = 0, bandwidth=20, frequency=5180):
        """
        配置LitePoint仪器进行WiFi发射测试。
        
        :param channel: WiFi信道，默认为36
        :param band_type: 频段类型，默认为'5G'
        :param modulation: 调制方式，默认为'OFDM'
        :param bandwidth: 带宽，默认为20MHz
        :param frequency: 中心频率，默认为5180MHz
        """
        channel = int(channel)
        frequency = int(frequency)

        # 检查配置是否发生变化
        if (band_type, modulation, bandwidth, mcs_value) != self.tx_mea_config:
            self.tx_mea_config = (band_type, modulation, bandwidth, mcs_value)

            # 设置VSA技术参数
            self.IQ.config_vsa_technology_settings(
                bandType=band_type,
                channel=channel,
                userMargin=0,
                expectedPNom=0,
                bandwidth=bandwidth,
                technology=litepoint.Technology.WIFI
            )

            # 设置VSA公共参数
            self.IQ.config_vsa_common_settings(standardFamily=modulation)

            # 根据调制方式设置具体参数
            if modulation == 'OFDM':

                #配置OFDM的DATA或者LTF模式
                TX_DATA_MODE_START_MCS = int(iniHandle.get_ini_value('DEFAULT', 'TX_DATA_MODE_START_MCS'))
                if mcs_value >= TX_DATA_MODE_START_MCS:
                    channel_est = litepoint.WifiFreqCorrect.DATA
                elif mcs_value < TX_DATA_MODE_START_MCS:
                    channel_est = litepoint.WifiFreqCorrect.LTF

                self.IQ.config_vsa_ofdm_settings(
                    standard=litepoint.WifiOFDMStandard.A_P_N_AC_AX,
                    freqCorrect=litepoint.WifiFreqCorrect.AUTO,
                    phaseCorrect=True,
                    ampCorrect=False,
                    symCorrect=True,
                    channelEst=channel_est,
                    packetFormat=litepoint.WifiOFDMPacketFormat.AUTO,
                    freqSeg=None,
                    useAllSig=True,
                    analyMode=None,
                    powerClass=litepoint.WifiOFDMPowerClass.A,
                    symbolTimeAdj=None,
                    specLimitType=litepoint.SpectrumLimitType.AUTO,
                    specLimitBW=litepoint.SpectrumLimitBW.AUTO,
                    enablePreAVG=True
                )
            elif modulation == 'DSSS':
                self.IQ.config_vsa_dsss_settings(
                    evmMethod=litepoint.EvmMethod.RMS,
                    equalTaps=litepoint.EqualizerTaps.OFF,
                    dcRemoval=True
                )
            

        # 设置VSA硬件参数
        self.IQ.config_vsa_hardware_settings(
            freq=frequency,
            referLevel=None,
            enableAGC=True,
            interval=10,
            samRate=litepoint.SamplingRate.MHZ_240
        )
        self.IQ.send_raw_command('VSA1;CAPT:TIME 0.015')

    def get_peak_wifi_tx_measure_results(self, modulation='OFDM'):
        """
        获取WiFi发射测试的所有测量结果。
        
        :param modulation: 调制方式，默认为'OFDM'
        :return: 包含功率、EVM、频偏、频谱模板数据最小值的元组
        """  
        try:
            if modulation == 'OFDM':
                self.IQ.send_raw_command('VSA1;init;WIFI;calc:pow 3,10;calc:txq 3,10;calc:ccdf 3,10;calc:spec 3,10')
                result = self.IQ.send_raw_command('FETC:POW:PEAK:MAX?;FETC:TXQ:OFDM:AVER?;FETC:SPEC:AVER:OBW?;FETC:SPEC:AVER:MARG?;FETC:OFDM:SFL:AVER:MARG?').split(';')
                power = float(result[0].split(',')[1])
                evm = float(self.IQ._convert_wifi_tx_quality_values(result[1])[0])
                freq_error = float(self.IQ._convert_wifi_tx_quality_values(result[1])[3])
                obw = self.IQ._convert_wifi_tx_occupied_bandwidth(result[2]) / 1000000
                min_mask = min([float(item) for item in self.IQ._convert_wifi_tx_margin(result[3])[0:8]])
            elif modulation == 'DSSS':
                self.IQ.send_raw_command('VSA1;init;WIFI;calc:pow 3,10;calc:txq 3,10;calc:ccdf 3,10;calc:ramp 3,10;calc:spec 3,10')
                result = self.IQ.send_raw_command('FETC:POW:PEAK:MAX?;FETC:TXQ:DSSS:AVER?;FETC:SPEC:AVER:OBW?;FETC:SPEC:AVER:MARG?').split(';')
                power = float(result[0].split(',')[1])
                evm = float(self.IQ._convert_wifi_tx_quality_values(result[1])[0])
                freq_error = float(self.IQ._convert_wifi_tx_quality_values(result[1])[5])
                obw = self.IQ._convert_wifi_tx_occupied_bandwidth(result[2]) / 1000000
                min_mask = min([float(item) for item in self.IQ._convert_wifi_tx_margin(result[3])[0:4]])
            return power, evm, freq_error, min_mask
        except Exception as err:
            print(f"获取测试结果出现意外: {err}")
            print(result)        
    def get_all_wifi_tx_measure_results(self, modulation='OFDM', timeout=10):
        """
        获取WiFi发射测试的所有测量结果。
        
        :param modulation: 调制方式，默认为'OFDM'
        :return: 包含功率、EVM、频偏、频谱模板数据最小值的元组
        """
        start_time = time.time()
        timeout = int(timeout)
        if modulation == 'OFDM':
            while True:
                if time.time() - start_time > timeout:
                    self.iq_data_queue.put(f'超过{timeout}秒，未获取到有效信息，测试退出!')
                    raise TimeoutError(f'超过{timeout}秒，未获取到有效信息，测试退出!')
                
                self.IQ.send_raw_command('VSA1;init;WIFI;calc:pow 3,10;calc:txq 3,10;calc:ccdf 3,10;calc:spec 3,10')
                result = self.IQ.send_raw_command('FETC:POW:AVER?;FETC:TXQ:OFDM:AVER?;FETC:SPEC:AVER:OBW?;FETC:SPEC:AVER:MARG?;FETC:OFDM:SFL:AVER:MARG?').split(';')
                print(result)
                # 获取到TXQ的有效数据
                print(f'len(result)={len(result)}')
                if len(result) < 4:
                    continue
                print(f'{result[0][0]},{result[1][0]},{result[2][0]},{result[3][0]}')
                if result[0][0] == '0' and result[1][0] == '0' and result[2][0] == '0' and result[3][0] == '0':
                    self.iq_data_queue.put(f'成功获取到数据，耗时{time.time() - start_time}秒')
                    break

            power = float(result[0].split(',')[1])
            evm = float(self.IQ._convert_wifi_tx_quality_values(result[1])[0])
            freq_error = float(self.IQ._convert_wifi_tx_quality_values(result[1])[3])
            obw = self.IQ._convert_wifi_tx_occupied_bandwidth(result[2]) / 1000000
            min_mask = min([float(item) for item in self.IQ._convert_wifi_tx_margin(result[3])[0:8]])
        elif modulation == 'DSSS':
            while True:
                if time.time() - start_time > timeout:
                    self.iq_data_queue.put(f'超过{timeout}秒，未获取到有效信息，测试退出!')
                    raise TimeoutError(f'超过{timeout}秒，未获取到有效信息，测试退出!')
                
                self.IQ.send_raw_command('VSA1;init;WIFI;calc:pow 1,1;calc:txq 1,1;calc:ccdf 1,1;calc:ramp 1,1;calc:spec 1,1')
                result = self.IQ.send_raw_command('FETC:POW:AVER?;FETC:TXQ:DSSS:AVER?;FETC:SPEC:AVER:OBW?;FETC:SPEC:AVER:MARG?').split(';')
                print(result)
                # 获取到TXQ的有效数据
                print(f'len(result)={len(result)}')
                if len(result) < 4:
                    continue
                print(f'{result[0][0]},{result[1][0]},{result[2][0]},{result[3][0]}')
                if result[0][0] == '0' and result[1][0] == '0' and result[2][0] == '0' and result[3][0] == '0':
                    self.iq_data_queue.put(f'成功获取到数据，耗时{time.time() - start_time}秒')
                    break

            power = float(result[0].split(',')[1])
            evm = float(self.IQ._convert_wifi_tx_quality_values(result[1])[0])
            freq_error = float(self.IQ._convert_wifi_tx_quality_values(result[1])[5])
            obw = self.IQ._convert_wifi_tx_occupied_bandwidth(result[2]) / 1000000
            min_mask = min([float(item) for item in self.IQ._convert_wifi_tx_margin(result[3])[0:4]])
        return power, evm, freq_error, min_mask

    def wifi_rx_measure_config(self, wave_file, frequency=5180):
        """
        配置LitePoint仪器进行WiFi接收测试。
        
        :param wave_file: 波形文件路径
        :param frequency: 中心频率，默认为5180MHz
        :return: 如果配置成功返回True
        """
        self.IQ.send_raw_command("CHAN1;WIFI;")
        self.IQ.send_raw_command(f"VSG1; WAVE:LOAD '{wave_file}'")
        self.IQ.send_raw_command("VSG1;POW:lev -40")
        self.IQ.send_raw_command("VSG1;SRAT 240000000")
        self.IQ.send_raw_command("VSG1;WLIS:COUN 1000")
        self.IQ.send_raw_command(f"VSG1;FREQ:cent {frequency}000000")
        return True

    def wifi_rx_send_packets(self, wave_file, tx_level='-40'):
        """
        发送WiFi数据包。
        
        :param wave_file: 波形文件路径
        :param tx_level: 发射功率，默认为'-40'
        """
        self.IQ.send_raw_command(f"VSG1;POW:lev {tx_level}")
        self.IQ.send_raw_command(f"VSG1;wave:exec off;WLIST:WSEG1:DATA '{wave_file}';WLIST:WSEG1:SAVE;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1")
        QThread.msleep(3000)
        self.IQ.send_raw_command("VSG1;WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1")

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