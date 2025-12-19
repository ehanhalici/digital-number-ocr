import cv2
import findContour
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

while 1==1:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (1920, 1080), interpolation=cv2.INTER_CUBIC)
    frame = findContour.find(frame)
    time.sleep(0.1)
    cv2.imshow("debugframe",frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
