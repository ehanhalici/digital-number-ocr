import cv2

DIGITS_LOOKUP = {
    #1  2  3  4  5  6  7
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 0, 1): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 1, 1, 0, 0, 1, 0): 7, # or (1, 0, 1, 0, 0, 1, 0)
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}
digits = []

"""            
            1
            _
        2 |   |  3
            4
            _
        5 |   | 6
            _
            7
"""

def getText(roi,x,y,w,h):
    text = ""
    roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    roi = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow("debugroi",roi)
    (roiH, roiW) = roi.shape
#---DIGITS_LOOKUP do not find "1". this is the solution
#---Because "1" has diffrent size others
    if roiW * 3 < roiH:
        total = cv2.countNonZero(roi)
        if total / float(roiH*roiW) > 0.3:
            return "1"
#---for other numbers
    (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
    dHC = int(roiH * 0.05)
    if dW == 0:
        dW = 1
    if dH == 0:
        dH = 1
    if dHC == 0:
        dHC = 1

	# define the set of 7 segments
    segments = [
        # x  y
		((dW, 0), (w-2*dW, dH)), #rearranged for the number  "4"    # top
		((0, 0), (dW, h // 2)),                                     # top-left
		((w - dW, 0), (w, h // 2)),                                 # top-right
		((0, (h // 2) - dHC) , (w, (h // 2) + dHC)),                # center
		((0, h // 2), (dW, h)),	                                    # bottom-left
		((w - dW, h // 2), (w, h)),	                                # bottom-right
		((0, h - dH), (w, h))	                                    # bottom
	]
    on = [0] * len(segments)

	# loop over the segments
    
    for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
            # extract the segment ROI
        segROI = roi[yA:yB, xA:xB]
        #for debug
        #tmp = roi.copy()
        #tmp = cv2.cvtColor(tmp,cv2.COLOR_GRAY2BGR)
        #cv2.rectangle(tmp, (xA, yA), (xB, yB), (0, 255, 0), 1)
        #cv2.imshow("segROI",tmp)   
        #cv2.waitKey(0)
        total = cv2.countNonZero(segROI)
        area = (xB - xA) * (yB - yA)
        # if the total number of non-zero pixels is greater than
        # 30% of the area, mark the segment as "on"
        if total == 0: # division by zero
            on[i] = 0
        elif total / float(area) > 0.3:
            on[i]= 1
        
    try:
        digit = DIGITS_LOOKUP[tuple(on)]       
        text = text + str(digit)
        return text
    except:
        #print("not found  ",tuple(on))
        return ""
    