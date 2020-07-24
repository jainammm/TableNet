import cv2
import pytesseract
from PIL import Image
import numpy as np
from pytesseract import Output

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

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def canny(image):
    return cv2.Canny(image, 100, 200)

def remove_noise_and_smooth(img):
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 41)
    return filtered


if __name__ == "__main__":
    
    img = cv2.imread('../1.jpg')
    

    img = get_grayscale(img)
    img = remove_noise_and_smooth(img)

    # h, w = img.shape
    # boxes = pytesseract.image_to_boxes(img) 
    # for b in boxes.splitlines():
    #     b = b.split(' ')
    #     img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    # d = pytesseract.image_to_data(img, output_type=Output.DICT)
    # print(d.keys())
    # n_boxes = len(d['text'])
    # for i in range(n_boxes):
    #     if int(d['conf'][i]) > 60:
    #         (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
    #         img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    custom_config = r'--oem 3 --psm 6'
    texts = pytesseract.image_to_string(img, config=custom_config)
    print(texts)

    with open('texts4.txt', 'w') as f:
        f.write(texts)

    cv2.imwrite('cleaned4.jpg', img) 
    
    # img = cv2.resize(img, (0,0), fx=0.3, fy=0.3) 
    # cv2.imshow('jpg', img)

    # r = cv2.waitKey(0)
    # print("DEBUG: waitKey returned:", chr(r))
    # cv2.destroyAllWindows()
