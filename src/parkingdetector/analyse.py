import math
import cvzone
from config import Config

class Analyse:
    
    def __init__(self):
        analyse = Config().GetAnalyse()

        self.MERIDIEM = analyse["MERIDIEM"] #0
        self.FACTOR = analyse["FACTOR"] #0.25
        self.LENGTH = analyse["LENGTH"] #600

    def findParking(self, gaps, img):
        print("find spaces")
        space = []
        for gap in gaps:
            try:
                height, width, channels = img.shape
                width = int(width)
                g = int(gap[0])
                x1, y1, x2, y2 = int(gap[1][0]), int(gap[1][1]), int(gap[1][2]), int(gap[1][3])
                if(g > 100):
                    if(x1 == 0):
                        space.append(gap)
                        cvzone.cornerRect(img, (x1, y1, x2-x1, y2-y1), colorR=(0, 255, 255), colorC=(0, 255, 255))
                    elif (self._calculate(x1,width) < g):
                        space.append(gap)
                        cvzone.cornerRect(img, (x1, y1, x2-x1, y2-y1), colorR=(0, 255, 255), colorC=(0, 255, 255))
            except Exception as e: 
                print(e)
                raise e
        return space

    def _calculate(self,x,w):

        lf = self.LENGTH - (self.LENGTH * self.FACTOR)
        rf = self.LENGTH - lf

        #right angle camara
        a = (w-x)/w
        al = (a*lf) + rf
        print(f"cal; x:{x}, al:{al}")
        return al

        



        # r = w #- (w*FACTOR) 
        # ar = math.acos(x/r)
        # br = math.radians(90)-ar
        # al = LENGTH * math.cos(br)
        # print(f"cal; x:{x}, r:{r}, x/r:{x/r}, ar:{ar} br: {br}, al:{al}")
        # return al

