import cv2          
import pytesseract
import numpy as np
import re
import sys


  
def getPlateNumber(imgIn):
    print(imgIn)
    image1 = cv2.imread(imgIn) 
    
    #cv2.imshow('car', image1)          

    img = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY) 
    
    #cv2.imshow('car', img)          

    ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)      

    #cv2.imshow('thresh1', thresh1)          

    contours, new  = cv2.findContours(thresh1.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:30]

    #cv2.imshow('contours', contours)          

    # Initialize license Plate contour and x,y coordinates
    contour_with_license_plate = None
    license_plate = None
    x = None
    y = None
    w = None
    h = None

    # Find the contour with 4 potential corners and creat ROI around it
    for contour in contours:
            # Find Perimeter of contour and it should be a closed contour
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
            if len(approx) == 4: #see whether it is a Rect
                contour_with_license_plate = approx
                x, y, w, h = cv2.boundingRect(contour)
                license_plate = thresh1[y:y + h, x:x + w]
                break


    license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)
    (thresh, license_plate) = cv2.threshold(license_plate, 50, 160, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(license_plate, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    LIC_NUM = re.sub("[^0-9]", "", text)
    print("License Plate: ",LIC_NUM)


    #cv2.imshow('License Plate Detection', license_plate)          
    return LIC_NUM

    # De-allocate any associated memory usage          
    if cv2.waitKey(0) & 0xff == 27: 
        cv2.destroyAllWindows() 
