import imgprocess as imp
import tess
import cv2
import imutils
from imutils import contours
import manuelFound

#---area where the calculator is searched on the camera
cutx = 240
cuty = 210
cutw = 400
cuth = 270

#---for contours
cntsMinw = 3
cntsMaxw = 20
cntsMinh = 5
cntsMaxh = 25 * 2

#---for contours combined
deviationx = 3
deviationy = 3

def find(frame):

    gray = imp.imgProcess(frame)
    #gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)[1]
    cut = gray[cuty:cuth, cutx:cutw ]
    cv2.rectangle(frame,(cutx,cuty),(cutw, cuth),(255, 50, 0), 1)
    cv2.imshow("debugcut",cut)

#---FIND CONTOUR
    cutReverse = cv2.threshold(cut, 0, 255, cv2.THRESH_BINARY_INV)[1]
    cnts = cv2.findContours(cutReverse,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    digitCnts = []
    
#---SHORT CONTOUR, left to right
    if len(cnts) > 0:
        cnts = contours.sort_contours(cnts,method="left-to-right")[0]

#---ELECTION CONTOUR
#---small ones are eliminated
        temp1 =[]
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c) 
            if (w >= cntsMinw and w <= cntsMaxw) or (h >= cntsMinh and h <= cntsMaxh):
                temp1.append((x, y, w, h) )    
#---similar x-axis are combined
        temp2 = []
        for j in temp1:
            for i in temp1:
                (x1, y1, w1, h1) = j
                (x2, y2, w2, h2) = i
                
                if i == j:
                    continue
                if (abs(x1-x2) < deviationx or abs((x1+w1) - (x2+w2)) < deviationx)  and (abs(y1-y2) - h1 < deviationy or abs(y1-y2) - h2 < deviationy):
                    c = (min(x1,x2),min(y1,y2),max(w1,w2),h1+h2) 
                    temp2.append(c)
                    temp1.remove(i)
                    try:
                        temp1.remove(j)
                    except:
                        pass
#---contain big and combined contour
#---combined
        for c in temp2:
            (x, y, w, h) = c 
            if (w >= cntsMinw and w <= cntsMaxw) and (h >= cntsMinh*2 and h <= cntsMaxh):
                digitCnts.append(c)
#---big
        for t in temp1:
            (x, y, w, h) = t
            if (w >= cntsMinw and w <= cntsMaxw) and (h >= cntsMinh*2 and h <= cntsMaxh):
                digitCnts.append((x, y, w, h))
        
        for j in digitCnts:
            for i in digitCnts:
                (x1, y1, w1, h1) = j
                (x2, y2, w2, h2) = i
                if x1<x2 :
                    (x3, y3, w3, h3) = i
                    i=(x1, y1, w1, h1)
                    j=(x3, y3, w3, h3)

#---CONTOUR PROCESSING
        text = ""
        if len(digitCnts)>0 :
            for c in digitCnts:
                (x, y, w, h) = c
                roi = cut[y:y + h, x:x + w]
                #roi = frame[y:y + h, x:x + w]
                cv2.rectangle(frame, (cutx+x, cuty+y), (cutx+x + w, cuty+y + h), (0, 255, 0), 1)
                
                #select detection algorithm
                #use pytesseract
                #text = text + tess.getText(roi) 
                #or use manuel detection   
                text = text + manuelFound.getText(roi,x,y,w,h)
            
            print(text)
            text = ""        

    return frame