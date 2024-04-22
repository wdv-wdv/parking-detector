from config import Config
import datetime

def shouldAlert(spaces):
    status = Config().GetParkingStatus()
    if(spaces>0):
        if(status["parking"]==True):
            return False
        if(status["number"] == spaces):
            first = datetime.datetime.fromisoformat(status["first"])
            if(first+datetime.timedelta(minutes=5) < datetime.datetime.now(datetime.UTC)):
                Config().SetParkingStatus(True,datetime.datetime.now(datetime.UTC) ,spaces)
                return True
            else:
                return False
        else:
            Config().SetParkingStatus(False,datetime.datetime.now(datetime.UTC) ,spaces)
            return False
    else:
        Config().SetParkingStatus(False,datetime.datetime.now(datetime.UTC) ,0)
        return False
