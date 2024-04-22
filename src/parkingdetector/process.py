import  cv2
import imutils
from detect import Detect
import mask
from slack import Slack 
from analyse import Analyse
import status

def execute(filename):
    print("Start process")
    print("Load image")
    img = cv2.imread(filename)

    img, contours = mask.apply(img)
    gaps = Detect(img, contours).spaces()

    spaces = Analyse().findParking(gaps,img)

    img = imutils.resize(img, width=min(1500, img.shape[1]))

    print(f"sapces: {len(spaces)}")

    if(status.shouldAlert(len(spaces))):
        Slack().sendMsg(f"Parking report: {len(spaces)} open",img)

    if __debug__:
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    print("Done!!")