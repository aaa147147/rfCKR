import configparser

def get_ini_value(section, option):

    section = str(section)
    option = str(option)
    # 去除 section 和 option 的前后空格
    section = section.strip()
    option = option.strip()

    ini = configparser.ConfigParser()
    file_path = './rfCKR.ini'
    
    # 读取文件
    ini.read(file_path, encoding='utf-8')
    
    # 获取值
    return ini.get(section, option)
