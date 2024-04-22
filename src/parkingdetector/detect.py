import cv2
import cvzone
import math
import statistics

class Detect:
    FONTFACE = cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.7
    THICKNESS = 1

    def __init__(self, img, contours):
        self.img = img
        self.contours = contours

    def spaces(self):
        print("Detect object/gaps")
        from ultralytics import YOLO
        
        import imutils
        import numpy as np

        model = YOLO('models/yolov8x.pt')
        gaps = []
        height, width, channels = self.img.shape

        results = model(self.img) #, stream=True)
        for r in results:
            self.__processBoxes(r.boxes, gaps)
            self.__addLeftGap(r.boxes,gaps)
            self.__addRightGap(r.boxes,gaps,width)

        if __debug__:
             cv2.drawContours(image=self.img, contours=self.contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
        if __debug__:
            self.__showGaps(gaps)
        return gaps

    def __processBoxes(self, boxes, gaps):
        from classnames import __classNames__
        for box in boxes:
            cls = box.cls[0]
            conf = math.ceil((box.conf[0]*100))/100
            
            # rect
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2-x1, y2-y1

            if __debug__:
                cvzone.cornerRect(self.img, (x1, y1, w, h))

            #gaps
            if (self.__objectOfInterest(cls,conf) and self.__inAreaOfInterest(x1, y1, x2, y2)) :
                if __debug__:
                    cvzone.cornerRect(self.img, (x1, y1, w, h), colorC=[0, 0, 250], colorR=[0, 0, 250])
                gap = 2000
                gapBox = None
                for box2 in boxes:
                    cls2 = box2.cls[0]
                    conf2 = math.ceil((box2.conf[0]*100))/100
                    if self.__objectOfInterest(cls2,conf2):
                        xx1, yy1, xx2, yy2 = box2.xyxy[0]
                        xx1, yy1, xx2, yy2 = int(xx1), int(yy1), int(xx2), int(yy2)
                        if self.__inAreaOfInterest( xx1, yy1, xx2, yy2):
                            g = xx1-x2
                            if(xx1 > x1 and g < gap):
                                gap = g
                                if (gap > 0): 
                                    gapBox = (x2, int((y1+yy1)/2) ,xx1, int((y2+yy2)/2))
                                else:
                                    gapBox = (xx1, int((y1+yy1)/2) ,x2, int((y2+yy2)/2))

                if(gapBox != None and gap < 2000):
                    gaps.append([gap,gapBox])
                    print(gapBox)
            #label 
            name = __classNames__[int(cls)]
            
            if __debug__:
                cvzone.putTextRect(self.img, f'{cls:n}-{name} 'f'{conf}', (max(0,x1), max(35,y1)), scale = self.FONT_SCALE, thickness=self.THICKNESS, font=self.FONTFACE)
                print(f"object:{cls:n}-{name}, conf: {conf}, x1:{x1}, x2:{x2}, y1:{y1}, w:{w}, h:{h}')")

    def __addLeftGap(self, boxes, gaps): 
        gap = 2000
        gapBox = None
        for box in boxes:
            cls = box.cls[0]
            conf = math.ceil((box.conf[0]*100))/100
            if self.__objectOfInterest(cls,conf):      
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                if (self.__inAreaOfInterest(x1, y1, x2, y2)):
                    g = x1
                    if(g < gap):
                        gap = g
                        gapBox = (0, y1 ,x1, y2)

        if(gapBox != None and gap < 2000 and gap > 0):
            gaps.append([gap,gapBox])

    def __addRightGap(self, boxes, gaps, width): 
        gap = 2000
        gapBox = None
        for box in boxes:
            cls = box.cls[0]
            conf = math.ceil((box.conf[0]*100))/100
            if self.__objectOfInterest(cls,conf):      
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                if (self.__inAreaOfInterest(x1, y1, x2, y2)):
                    g = width-x2
                    if(g < gap):
                        gap = g
                        gapBox = (x2, y1 ,width, y2)

        if(gapBox != None and gap < 2000 and gap > 0):
            gaps.append([gap,gapBox])

    def __showGaps(self, gaps):
        print(f"gaps: {len(gaps)}")
        for gap in gaps:
            # print(g)
            try:
                g = int(gap[0])
                x1, y1, x2, y2 = int(gap[1][0]), int(gap[1][1]), int(gap[1][2]), int(gap[1][3])
                w, h = x2-x1, y2-y1
                if(g > 0):
                    cvzone.cornerRect(self.img, (x1, y1, w, h), colorR=(255, 0, 0), colorC=(255, 0, 0))
                else:
                    cvzone.cornerRect(self.img, (x1, y1, w, h), colorR=(255, 255, 0), colorC=(255, 255, 0))
                print(f'gap:{g}, x1:{x1}, x2:{x2}, y1:{y1}, w:{w}, h:{h}')
            except:
                print(f'gap:{g}, x1:{x1}, x2:{x2}, y1:{y1}, w:{w}, h:{h}')

    def __objectOfInterest(self,cls,conf):
        return ((cls >= 2 and cls <=8 and conf >= 0.5) 
                    #car cover
                    or (cls == 8) # boat
                    or (cls==59) # bed = 59
                    or (cls==25) # umbrella = 25
                    or (cls==28) # suitcase = 28
                )

        # "car", = 2
        # "motorbike",
        # "aeroplane",
        # "bus",
        # "train",
        # "truck",
        # "boat",

    def __inAreaOfInterest(self, x1, y1, x2, y2):
        x = int((x2+x1)/2)
        top = 2000
        bottom = 0
        for contour in self.contours:
            for point in contour:
                # print(f"point: {point}")
                if(point[0][0] == x):
                    y = point[0][1]
                    if (y>bottom): bottom = y
                    if (y<top): top = y

        
        if(top == 2000 and bottom == 0):
            # not area
            return False
        
        y = int((top+bottom)/2) # calculate vertical mid point
        if __debug__:
            cv2.drawMarker(self.img, (x, y), color=[0, 0, 250], thickness=5, markerType= cv2.MARKER_TILTED_CROSS, line_type=cv2.LINE_AA,markerSize=50)

        return True if (y2>y) else False # True if box bottom end is below vertical mid point


