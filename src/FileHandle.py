import pandas as pd
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import os
import iniHandle

class FileHandle:
    def __init__(self):
        """
        初始化FileHandle类，设置测试项目列表和结果文件路径。
        """
        self.test_item_list = []  # 存储测试项目的列表
        self.result_file_path = None  # 存储结果文件的路径
        self.result_file_df = None  # 存储结果文件的DataFrame
        self.test_item_Num = 0
    def load_test_item(self):
        """
        打开文件选择对话框，让用户选择测试文件并加载数据。
        """
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(None, "选择测试文件", "", "Excel Files (*.xlsx);;All Files (*)")
        
        # 检查是否选择了文件
        if file_path:
            try:
                # 读取Excel文件
                df = pd.read_excel(file_path)
                
                # 将数据转换为列表
                self.convert_to_list(df)
                
                # 显示成功消息
                self.show_message("测试文件加载成功")
            except Exception as e:
                self.show_message(f"读取文件时发生错误: {e}")
        else:
            self.show_message("未选择文件")

    def convert_to_list(self, df):
        """
        将DataFrame中的数据转换为字典列表，并存储到self.test_item_list中。
        
        :param df: 包含测试数据的DataFrame
        """
        # 初始化列表
        self.test_item_list = []
        
        # 遍历DataFrame，将每一行数据转换为字典并添加到列表中
        for index, row in df.iterrows():
            data_dict = {
                'No': row['No'],
                'isExec': row['isExec'],
                'isRecord': row['isRecord'],
                'socName': row['socName'],
                'testType': row['testType'],
                'testItemName': row['testItemName'],
                'Frequency': row['Frequency'],
                'execCmd': row['execCmd'],
                'powerLowerLimit': row['powerLowerLimit'],
                'powerTestValue': row['powerTestValue'],
                'powerUpperLimit': row['powerUpperLimit'],
                'freErrorLowerLimit': row['freErrorLowerLimit'],
                'freErrorTestValue': row['freErrorTestValue'],
                'freErrorUpperLimit': row['freErrorUpperLimit'],
                'evmLowerLimit': row['evmLowerLimit'],
                'evmTestValue': row['evmTestValue'],
                'evmUpperLimit': row['evmUpperLimit'],
                'maskMargin': row['maskMargin'],
                'minReceiveLevelLowerLimit': row['minReceiveLevelLowerLimit'],
                'minReceiveLevelTestValue': row['minReceiveLevelTestValue'],
                'minReceiveLevelUpperLimit': row['minReceiveLevelUpperLimit'],
                'maxReceiveLevelLowerLimit': row['maxReceiveLevelLowerLimit'],
                'maxReceiveLevelTestValue': row['maxReceiveLevelTestValue'],
                'maxReceiveLevelUpperLimit': row['maxReceiveLevelUpperLimit']
            }
            if iniHandle.get_ini_value('DEFAULT', 'TX_GET_PEAK_POWER') == '1':
                data_dict['peakPowerTestValue '] = ''
            # 清空测试数据
            data_dict['powerTestValue'] = ''
            data_dict['freErrorTestValue'] = ''
            data_dict['evmTestValue'] = ''
            data_dict['minReceiveLevelTestValue'] = ''
            data_dict['maxReceiveLevelTestValue'] = ''
            data_dict['maskMargin'] = ''
            self.test_item_list.append(data_dict)

    def open_test_result_file(self):
        """
        打开文件对话框，让用户选择新建的测试结果文件路径，并保存初始数据。
        
        :return: 如果文件创建成功返回True，否则返回False
        """
        # 打开文件对话框
        self.result_file_path, _ = QFileDialog.getSaveFileName(None, "新建测试结果文件", "", "Excel Files (*.xlsx);;All Files (*)")
        if self.result_file_path:
            try:
                # 创建一个空的DataFrame
                self.result_file_df = pd.DataFrame(self.test_item_list)
                
                # 保存DataFrame到Excel文件
                self.result_file_df.to_excel(self.result_file_path, index=False)
                
                # 检查文件是否存在
                if not os.path.exists(self.result_file_path):
                    raise FileNotFoundError(f"文件 {self.result_file_path} 不存在")
                return True

            except FileNotFoundError as e:
                self.show_message(str(e))
            except IOError as e:
                self.show_message(str(e))
            except Exception as e:
                self.show_message(f"保存文件时发生错误: {e}")
        else:
            self.show_message("未选择文件")
        return False

    def save_test_result(self):
        """
        保存当前的测试结果到已选择的结果文件中。
        
        :return: 如果保存成功返回True，否则抛出异常
        """
        try:
            # 更新DataFrame
            self.result_file_df = pd.DataFrame(self.test_item_list)
            
            # 保存更新后的DataFrame到Excel文件
            self.result_file_df.to_excel(self.result_file_path, index=False)
            return True
        except IOError as e:
            raise Exception(f"保存文件时发生错误: {e}")
        except Exception as e:
            raise Exception(f"保存文件时发生错误: {e}")

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