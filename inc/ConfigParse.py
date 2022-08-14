import configparser
import pyautogui

class ConfigParse:

    config = None

    ModeList = []
    MouseOptions = {'modelist': list(), 'startmove': 0, 'endmove': 0, 'startclick': 0, 'endclick': 0, 'radius': 0, 'angle': 0, 'timeout': 0}

    def __init__(self):
        self.config = configparser.ConfigParser()

    def write_config(self, ModeList, startMove, endMove, startClick, endClick, radius, angle, timeout):
        self.MouseOptions = {'modelist': ModeList, 'startmove': startMove, 'endmove': endMove, 'startclick': startClick, 'endclick': endClick, 'radius': radius, 'angle': angle, 'timeout': timeout}
        self.config['Mouse'] = self.MouseOptions
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        configfile.close()

    def check_config(self):
        if self.config.read('config.ini'):
            return True
        else:
            return False

    def parseQuad(self, k, v):
        quadList = v.split()
        for q in quadList:
            if 'easeInQuad' in  q:
                self.ModeList.append(pyautogui.easeInQuad)
            elif 'easeOutQuad' in q:
                self.ModeList.append(pyautogui.easeOutQuad)
            elif 'easeInOutQuad' in q:
                self.ModeList.append(pyautogui.easeInOutQuad)
            elif 'easeOutQuart' in q:
                self.ModeList.append(pyautogui.easeOutQuart)
            elif 'easeInOutQuart' in q:
                self.ModeList.append(pyautogui.easeInOutQuart)
            elif 'easeInQuad' in q:
                self.ModeList.append(pyautogui.easeInQuad)
            elif 'easeInBack' in q:
                self.ModeList.append(pyautogui.easeInBack)
            else:
                print('Modus niet beschikbaar')

        self.MouseOptions[k] = self.ModeList

    def read_config(self):
        self.config.read('config.ini')
        for section in self.config.sections():
            if section == 'Mouse':
                for k, v in self.config.items(section):
                    if k == 'modelist':
                        self.parseQuad(k, v)
                    else:
                        self.MouseOptions[k] = v

