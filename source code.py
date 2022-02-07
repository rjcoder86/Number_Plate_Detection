import sys
import cv2
import pytesseract
import re
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# image=input('Please Enter Image path :') #for dynamic input
# img=cv2.imread(image)

img=cv2.imread('test_pics\car2.jfif')
# img=cv2.imread('test_pics\car3.jfif')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow('threshold image', gray)
cv2.waitKey(0)
img2=gray.copy()
erode=cv2.erode(img2,None,iterations=1)
ret,thresh1=cv2.threshold(img2,0,255,cv2.THRESH_OTSU)
rect_kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(13,5)) #rectangle size of contour
contours, new = cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

def findnp(x,y,w,h):   #function to crop rectangular shape
    rect = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
    crop = img2[y:y + h, x:x + w]
    text = pytesseract.image_to_string(crop, config='--psm 7 --oem 1')
    m = re.search('\S{2}\s*\d{2}\s*\S+\s*\d*', text) #cheching text using regular expression with numberplate formate
    if m:
        print('text found in number plate formate:',text)
        cv2.imshow('croped image', crop)
        cv2.waitKey(0)
        sys.exit(0)

for cnt in contours:
    x,y,w,h=cv2.boundingRect(cnt)
    findnp(x,y,w,h)   #calling function with passing contour points
