import cv2

def convert_to_sketch(input_path, output_path):
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256.0)
    cv2.imwrite(output_path, sketch)
