import cv2
import pytesseract
from PIL import Image

img = cv2.imread('out.jpg')

def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    im_resized = im.resize(size, Image.ANTIALIAS)
    # temp_file = tempfile.NamedTemporaryFile(delete=False,   suffix='.png')
    # temp_filename = temp_file.name
    im_resized.save('dpi_more.jpg', dpi=(300, 300))
    return im_resized

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)



set_image_dpi('out.jpg')
img = cv2.imread('dpi_more.jpg')

custom_config = r'--oem 3 --psm 6'
pytesseract.image_to_string(img, config=custom_config)



# h, w, c = img.shape
# boxes = pytesseract.image_to_boxes(img) 
# for b in boxes.splitlines():
#     b = b.split(' ')
#     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

# cv2.imshow('img', img)
# cv2.waitKey(0)
