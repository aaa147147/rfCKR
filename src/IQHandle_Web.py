import time
from selenium import webdriver
import iniHandle
import os

class IQHandle_Web:
    def __init__(self, iq_data_queue):

        self.iq_data_queue = iq_data_queue

        self.ip_address = iniHandle.get_ini_value('DEFAULT', 'IQ_LITE_POINT_IP')
        if not self.ip_address:
            self.ip_address = '192.168.100.254'

        #打开浏览器
        try:
            self.browser = webdriver.Chrome()
            self.browser.get('http://' + self.ip_address)
        except Exception as e:
            self.iq_data_queue.put(f"打开浏览器失败：{e}")
            self.browser.quit()

        #检查screenshot文件夹是否存在，如果不存在，创建
        if not os.path.exists('./screenshot'):
            os.mkdir('./screenshot')
        
        #创建当前时间戳的文件夹
        current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.current_folder = './screenshot/' + current_time + '/'
        os.mkdir(self.current_folder)
        self.iq_data_queue.put(f"创建文件夹：{self.current_folder}")

    def __del__(self):
        self.browser.quit()
    def screenshot(self, file_name):
        try:
            self.browser.get_screenshot_as_file(self.current_folder + file_name + '.png')
        except Exception as e:
            self.iq_data_queue.put(f"截图失败：{e}")



