import configparser
import os
import sys
from pathlib import Path

class Config(object):
    _instance = None
    _parser = None


    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Config, cls).__new__(cls)
            
            # Put any initialization here.
            filename = "parkingdetector.dev.ini" if __debug__ else "parkingdetector.ini"

            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            elif __file__:
                application_path = os.path.dirname(__file__)

            application_path = Path(application_path).parent.absolute()
            config_path = os.path.join(application_path, filename)

            print(f"Config filename: {config_path}")
            if (not os.path.isfile(config_path)):
                print("config file not found")
                sys.exit(1)
            cls._config_path = config_path
            cls._parser = configparser.ConfigParser()
            cls._parser.read(config_path)
            
        return cls._instance
    
    def GetMaskFilename(self):
        return self._parser.get("Detect", "mask_filename")
    
    def GetSlack(self):
        return {
            "token": self._parser.get("Slack", "token"), 
            "channel_name": self._parser.get("Slack", "channel_name") 
            }
    
    def GetAnalyse(self):
        return {
            "MERIDIEM": self._parser.getint("Analyse", "MERIDIEM"), 
            "FACTOR": self._parser.getfloat("Analyse", "FACTOR"),
            "LENGTH": self._parser.getint("Analyse", "LENGTH") 
            }
    
    def GetParkingStatus(self):
        return {
            "parking": self._parser.getboolean("Status", "parking"), 
            "first": self._parser.get("Status", "first"),
            "number": self._parser.getint("Status", "number") 
            }
    
    def SetParkingStatus(self, parking, first, n):
        self._parser.set("Status","parking", f"{parking}")
        self._parser.set("Status","first", f"{first}")
        self._parser.set("Status","number", f"{n}")
        with open(self._config_path, 'w') as configfile:
            self._parser.write(configfile)

    def PrintAll(self):
        for section_name in self._parser.sections():
            print(f"Section: {section_name}")
            print(f"Options: {self._parser.options(section_name)}")
            for name, value in self._parser.items(section_name):
                print(f"  {name} = {value}")
            print()



