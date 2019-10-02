import cv2
import numpy as np


def imgProcess(image):
 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    #equHist = cv2.equalizeHist(gray)
    #clahe = cv2.createCLAHE(clipLimit=200.0, tileGridSize=(10,10))
    #gray = clahe.apply(gray)
    #THRESHOLDING---------------------------------------------------------
    
    #thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7,7)
 
    # Close processing
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    #thresh = cv2.adaptiveThreshold(thresh,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,2)

    #EDGE DETECTION----------------------------------------------------------
       
    blurred = cv2.GaussianBlur(thresh, (7,7),0)
    blurred = cv2.medianBlur(blurred,1)
    v = np.mean(blurred)
    sigma=0.33
    lower = (int(max(0, (1.0 - sigma) * v)))
    upper = (int(min(255, (1.0 + sigma) * v)))
    edged = cv2.Canny(blurred, lower, upper)
    edged = cv2.threshold(edged, 0, 255, cv2.THRESH_BINARY_INV )[1]
    #SAVE AND EXIT-----------------------------------------------------------
    #cv2.imshow("thresh", thresh)
    #newPath = "tmp" + imgPath[3:]
    #cv2.imwrite(newPath,thresh)
    #cv2.imshow("edged", edged)
    #cv2.waitKey(0)
    return thresh
