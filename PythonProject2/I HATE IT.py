import cv2
from matplotlib import pyplot as plt

img = cv2.imread("people1.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_rbg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

face_data = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
face = face_data.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=5)
print(face)
for (x, y, width, height) in face:
    cv2.circle(img_rbg, (x +(width // 2 ), y +  (height // 2)), width // 2, (0,255,0), 5)

plt.subplot(1, 1, 1)
plt.imshow(img_rbg)
plt.show()

