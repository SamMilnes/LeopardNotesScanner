# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt

# %%
# read in image and convert it to 
img = cv2.imread("seg1.png")
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_gray_img = cv2.medianBlur(gray_img, 5)
invert_blur_gray_img = cv2.bitwise_not(blur_gray_img)

# %%
# from https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
# hresholding 

ret, th1 = cv2.threshold(invert_blur_gray_img, 127, 255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(invert_blur_gray_img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
th3 = cv2.adaptiveThreshold(invert_blur_gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

th2 = cv2.bitwise_not(th2) # invert color
th3 = cv2.bitwise_not(th3) # invert color

titles = ['original', 'global v = 127', 'mean', 'gaussian']
images = [invert_blur_gray_img, th1, th2, th3]

for i in range(4):
    plt.subplot(2, 2, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()

# %%
# from https://www.youtube.com/watch?v=s4Gx4JbPdrM timestamp 4:03
# dilation / line segmentation 
kernel = np.ones((3, 85), np.uint8)
dilated = cv2.dilate(th3, kernel, iterations = 1)  # can use invert_blur_gray_img, th1, th2, th3
plt.imshow(dilated, cmap='gray')

# draw contours on each line
(contours, heirarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
sorted_contours_lines = sorted(contours, key=lambda ctr : cv2.boundingRect(ctr)[1]) # (x, y , w, h)

# %%
img2 = img.copy()

# identify lines and enclose them with rectangles
for ctr in sorted_contours_lines:
    x,y,w,h = cv2.boundingRect(ctr)
    cv2.rectangle(img2, (x,y), (x+w, y+h), (40, 100, 250), 2)

plt.imshow(img2)

# %%
# dilation / text segmentation 

kernel2 = np.ones((3,85), np.uint8)
dilated2 = cv2.dilate(invert_blur_gray_img, kernel2, iterations=1)
plt.imshow(dilated2, cmap='gray')

# %%
img3 = img.copy()

for line in sorted_contours_lines:
    # roi of each line
    x,y,w,h = cv2.boundingRect(line)
    roi_line = dilated2[y:y+w, x:x+w]

    # draw contours on eaach word
    (cnt, heirarachy) = cv2.findContours(roi_line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_contours_words = sorted(cnt, key=lambda cntr : cv2.boundingRect(cntr)[0])

    for word in sorted_contours_words:
        x2,y2,w2,h2 = cv2.boundingRect(word)
        cv2.rectangle(img3, (x+x2, y+y2), (x+x2+w2, y+y2+h2), (255,255,100), 2)

plt.imshow(img3)
# %%
