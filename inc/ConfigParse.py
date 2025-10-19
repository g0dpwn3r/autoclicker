import configparser
import pyautogui

class ConfigParse:

    config = None

    ModeList = []
    ModeListString = ""
    keyOption = {'keybind': str()}
    MouseOptions = {'modelist': list(), 'startmove': 0, 'endmove': 0, 'startclick': 0, 'endclick': 0, 'radius': 0, 'angle': 0, 'timeout': 0}

    def __init__(self):
        self.config = configparser.ConfigParser()

    def write_config(self, ModeList, key, startMove, endMove, startClick, endClick, radius, angle, timeout):
        try:
            self.keyOption = {'keybind': str(key)}
            self.MouseOptions = {'modelist': str(ModeList), 'startmove': str(startMove), 'endmove': str(endMove), 'startclick': str(startClick), 'endclick': str(endClick), 'radius': str(radius), 'angle': str(angle), 'timeout': str(timeout)}
            self.config['Mouse'] = self.MouseOptions
            self.config['key'] = self.keyOption
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(f"Error writing config: {e}")
            raise

    def write_easing_modes(self, easing_modes):
        """Write easing modes to config"""
        try:
            if not self.config.has_section('Mouse'):
                self.config.add_section('Mouse')
            self.config.set('Mouse', 'easing_modes', easing_modes)
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
        except Exception as e:
            print(f"Error writing easing modes to config: {e}")
            raise

    def check_config(self):
        if self.config.read('config.ini'):
            return True
        else:
            return False

    def parseQuad(self, k, v):
        quadList = v.split()
        for q in quadList:
            if 'easeInQuad' in q:
                self.ModeList.append(pyautogui.linear)
            elif 'easeOutQuad' in q:
                self.ModeList.append(pyautogui.linear)
            elif 'easeInOutQuad' in q:
                self.ModeList.append(pyautogui.linear)
            elif 'easeOutQuart' in q:
                self.ModeList.append(pyautogui.linear)
            elif 'easeInOutQuart' in q:
                self.ModeList.append(pyautogui.linear)
            elif 'easeInBack' in q:
                self.ModeList.append(pyautogui.linear)
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
                        self.ModeListString = v
                    elif k == 'easing_modes':
                        # Store easing modes for GUI initialization
                        self.easing_modes = v
                    else:
                        self.MouseOptions[k] = v

