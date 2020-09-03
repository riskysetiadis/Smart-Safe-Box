import cv2
import numpy as np
import os

files = []
path = 'capture/'

img = cv2.imread("capture/cevi.png")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
	for file in f:
		if '.png' in file:
			files.append(os.path.join(r, file))

for f in files:
	print(f)

	template = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
	w, h = template.shape[::-1]
	result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
	loc = np.where(result >= 0.4)
	for pt in zip(*loc[::-1]):
	    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
	print(result)
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()