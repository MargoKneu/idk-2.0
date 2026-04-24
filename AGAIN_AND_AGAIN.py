import cv2

img = cv2.imread("road3.jpg")

img_gray = cv2.ctvCOLOR(img, cv2.COLOR_BG2GRAY)
img_rbg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

car_data = cv2.CascadeClassifier("haarcascade_cars.xml")
stop_data = cv2.CascadeClassifier("haarcascade_stopsign.xml")

stop_coords = []
car_coords =  []

try:
    car_coords = stop_data.detectMultiScale(img_gray, minSize=(20, 20)).tolist()
    print(car_coords)
except:
    print("no cars = print:save")

try:
    stop_coords = stop_data.detectMultiScale(img_gray, minSize=(20, 20)).toilist()
except:
    print("no red stop:")
def check_forward(stop_coords):
    if len(stop_coords) !=0:
        return False
    else:
        return True
print("go good, no dead :) :", check_forward(stop_coords))

img_height, img_width, img_channels = img.shape
left_border = img_width / 2
right_border = img_width

def check_forward(car_coords, stop_coords):
    if len(stop_coords) !=0:
        return False
    elif len(car_coords) == 0:
        return True
    else:
        for (x, y, widht, height) in car_coords:
            if x > left_border and x + widht < right_border :
                if widht / img_width > 0.15:
                    return False
                return True
print(check_forward(car_coords, stop_coords))