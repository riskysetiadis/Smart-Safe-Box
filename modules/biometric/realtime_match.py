import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
    if key == 32:
        template = cv2.imread("capture/kanan.png", cv2.IMREAD_GRAYSCALE)
        new_img = cv2.resize(gray_frame,(int(600),int(600)))
        print(template)
        w, h = template.shape[::-1]
        result = cv2.matchTemplate(new_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= 0.4)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
        print(result)
cap.release()
cv2.destroyAllWindows()