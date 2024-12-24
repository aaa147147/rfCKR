
import configparser


def get_ini_value(section,option):
    ini = configparser.ConfigParser()
    ini.read('./rfCKR.ini',encoding='utf-8')
    return ini.get(section,option)




    