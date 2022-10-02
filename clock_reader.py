import cv2
import numpy as np
from matplotlib import pyplot as plt
from numpy.core.numeric import array_equal
from skimage import io,color
# from skimage.filters import roberts, sobel, sobel_h, sobel_v, scharr, \
#     scharr_h, scharr_v, prewitt, prewitt_v, prewitt_h, farid_v, farid_h, \
#     threshold_otsu
from skimage.transform import resize
import copy
import time


start_time = time.time()
img = cv2.imread('./sample_img.jpg',)

scale_percent = 60 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
 
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

circle_detection = copy.deepcopy(resized)

(w, h) = gray.shape


mask = np.zeros((w,h), np.uint8)
cimg=cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(circle_detection, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(circle_detection, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
# show the output image
# cv2.imshow("output", circle_detection)
# cv2.waitKey(0)

(x, y, r) = circles[0]

# given x,y are circle center and r is radius
rectX = (x - r) 
rectY = (y - r)
crop_img = resized[rectY:(rectY+2*r), rectX:(rectX+2*r)]
(w,h,k) = crop_img.shape

# cv2.imshow("output", crop_img)
# cv2.waitKey(0)

flags = cv2.INTER_CUBIC + cv2.WARP_POLAR_LINEAR
rotate_frame = cv2.rotate(crop_img, cv2.ROTATE_90_CLOCKWISE)
dst = cv2.warpPolar(rotate_frame, (w, 2*h), (int(w/2),int(h/2)), r, flags)

# io.imshow(dst)
# cv2.waitKey(0)

kernel = np.ones((1,80), np.uint8)

img_dilation = cv2.dilate(dst, kernel, iterations=1)

# io.imshow(img_dilation)
# io.show()

grayImage = cv2.cvtColor(img_dilation, cv2.COLOR_BGR2GRAY)

(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 100, 255, cv2.THRESH_BINARY_INV)

# io.imshow(blackAndWhiteImage)
# io.show()

contours, hierarchy=cv2.findContours(image=blackAndWhiteImage.copy(),mode=cv2.RETR_TREE,method=cv2.CHAIN_APPROX_NONE)

thresh_area = 100
thresh_length = 100

hands_square = []
hands_length = []

for c in contours:
    x,y,w,h=cv2.boundingRect(c)
    # print(f'x{x} y{y} w{w} h{h}')
    
    area = cv2.contourArea(c)     
    # print(f'AREA {area}')    
    if area > thresh_area and (w+h) > thresh_length: 
        hands_square.append([x,y,w,h])
        hands_length.append(w)        

ordered = [x for _, x in sorted(zip(hands_length, hands_square))]

hands_square = ordered
# print(hands_square)

#map seconds

height = blackAndWhiteImage.shape[0]

[x,y,w,h] = hands_square[1]
y_seg = y+(h/2)

seconds = int(np.floor(60*(y_seg/height)))

# print(f'height {height} and secs {y_seg} seconds {seconds}')

#map hours

# height = blackAndWhiteImage.shape[0]

[x,y,w,h] = hands_square[0]
y_hour = y+(h/2)

# y_hour = hands_square[0][1]

hour = int(np.floor(12*(y_hour/height)))

# print(f'height {height} Y SEG {y_hour} hours {hour}')

#mapear minuto

# height = blackAndWhiteImage.shape[0]

[x,y,w,h] = hands_square[2]
y_min = y+(h/2)

# y_min = hands_square[2][1]

minutes = int(np.floor(60*(y_min/height)))

# print(f'height {height} Y MIN {y_min} minutes {minutes}')

print(f'{hour}:{minutes}:{seconds}')

#just benchmarking processing time
print("--- %s seconds ---" % (time.time() - start_time))
