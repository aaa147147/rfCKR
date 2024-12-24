import litepoint

ipAddress = '192.168.100.254'
BandWidth=20
Channel=1

IQ = litepoint._LitePointKeywords()

#连接并复位仪器
IQ.open_lite_point_connection(ipAddress)
IQ.send_raw_command('SYS;*CLS;*RST;FORM:READ:DATA ASC')

#配置端口
IQ.send_raw_command('''ROUT1;PORT:RES:ADD RF1A,VSA1''')
IQ.send_raw_command('''ROUT1;PORT:RES:ADD RF1A,VSG1''')

#模式配置
IQ.config_vsa_technology_settings(
             bandType=litepoint.WifiBandType.G2_4,
             channel=litepoint.MEASChannel.CH1,
             userMargin=0,
             expectedPNom=0,
             bandwidth=BandWidth,
             technology=litepoint.Technology.WIFI
         )
IQ.config_vsa_common_settings(standardFamily=litepoint.WifiModulation.DSSS)
IQ.config_vsa_ofdm_settings(
                 standard=litepoint.WifiOFDMStandard.A_P_N_AC_AX,
                 freqCorrect=litepoint.WifiFreqCorrect.LTF,
                 phaseCorrect=True,
                 ampCorrect=False,
                 symCorrect=True,
                 channelEst=litepoint.WifiFreqCorrect.LTF,
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

IQ.config_vsa_common_settings(standardFamily=litepoint.WifiModulation.DSSS)
IQ.config_vsa_dsss_settings(
    evmMethod=litepoint.EvmMethod.RMS,
    equalTaps=litepoint.EqualizerTaps.OFF,
    dcRemoval=True
)   


   
IQ.config_vsa_hardware_settings(freq=2412,referLevel=None,enableAGC=True,interval=10,samRate= litepoint.SamplingRate.MHZ_240)
         
#触发测试
IQ.send_raw_command('VSA1;CAPT:TIME 0.013')     
IQ.send_raw_command('VSA1;init;WIFI;calc:pow 3,10;calc:txq 3,10;calc:ccdf 3,10;calc:spec 3,10')

#获取测试结果
a = IQ.send_raw_command('FETC:POW:AVER?;FETC:TXQ:OFDM?;FETC:SPEC:AVER:OBW?;FETC:SPEC:MARG?;FETC:OFDM:SFL:MARG?').split(';')

#获取功率
a[0]

#获取EVM
IQ._convert_wifi_tx_quality_values(a[1])[0]

#获取频偏
IQ._convert_wifi_tx_quality_values(a[1])[3]

#获取OBW
IQ._convert_wifi_tx_occupied_bandwidth(a[2]) / 1000000         

#获取频谱模板
IQ._convert_wifi_tx_margin(a[3])[0]
IQ._convert_wifi_tx_margin(a[3])[1]
IQ._convert_wifi_tx_margin(a[3])[2]
IQ._convert_wifi_tx_margin(a[3])[3]
IQ._convert_wifi_tx_margin(a[3])[4]
IQ._convert_wifi_tx_margin(a[3])[5]
IQ._convert_wifi_tx_margin(a[3])[6]
IQ._convert_wifi_tx_margin(a[3])[7]








import litepoint

ipAddress = '192.168.100.254'

IQ = litepoint._LitePointKeywords()

#连接并复位仪器
IQ.open_lite_point_connection(ipAddress)
IQ.send_raw_command('SYS;*CLS;*RST;FORM:READ:DATA ASC')

#配置端口
IQ.send_raw_command('''ROUT1;PORT:RES:ADD RF1A,VSA1''')
IQ.send_raw_command('''ROUT1;PORT:RES:ADD RF1A,VSG1''')

#vsg_technology_settings
IQ.send_raw_command("CHAN1;WIFI;")

#加载波形文件
IQ.send_raw_command("VSG1; WAVE:LOAD '/user/WiFi_11N_HT20_S0_MCS7.iqvsg'")

#设置发射频率
IQ.send_raw_command("VSG1;FREQ:cent 5700000000")

#设置发射功率
IQ.send_raw_command("VSG1;POW:lev -40")

#设置Sampling Rate
IQ.send_raw_command("VSG1;SRAT 240000000")

#设置发射数量
IQ.send_raw_command("VSG1;WLIS:COUN 1000")

#开始发送
IQ.send_raw_command("VSG1;wave:exec off;WLIST:WSEG1:DATA '/user/WiFi_11N_HT20_S0_MCS7.iqvsg';WLIST:WSEG1:SAVE;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1")
IQ.send_raw_command("VSG1;WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1")






















   
         
         