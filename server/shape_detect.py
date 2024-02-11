# shape_detector.py
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from PIL import Image, ImageFilter


class AIProcessor_Shape:
    @staticmethod
    def detect_shape(input_image):
        img = cv.imread(input_image, cv.IMREAD_GRAYSCALE)
        edges = cv.Canny(img, 100, 200)

        area = 0
        perimeter = 0
        contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv.contourArea(cnt)
            perimeter = cv.arcLength(cnt, True)
            # print("Area: ", area)
            # print("Perimeter: ", perimeter)

        classification = AIProcessor_Shape.get_shape_type(area, perimeter)

        # plt.subplot(121), plt.imshow(img, cmap="gray")
        # plt.title("Original Image"), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(edges, cmap="gray")
        # plt.title("Edge Image"), plt.xticks([]), plt.yticks([])
        # plt.show()

        thresh = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
        thresh = cv.adaptiveThreshold(
            img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2
        )
        thresh = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
        thresh = cv.adaptiveThreshold(
            img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2
        )
        thresh = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

        kernel = np.ones((3, 3), np.uint8)
        eroded = cv.erode(thresh, kernel, iterations=1)
        dilated = cv.dilate(eroded, kernel, iterations=1)

        thresh = dilated

        result = np.zeros_like(img)
        contours = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        for cntr in contours:
            area = cv.contourArea(cntr)
            if area > 20:
                cv.drawContours(result, [cntr], 0, 255, 1)

        cv.imwrite("thresh_temp.png", dilated)

        mask_img = Image.open("thresh_temp.png")
        mask_img = mask_img.filter(ImageFilter.MedianFilter())

        mask_img.save("thresh.png")

        return classification

        # cv.imshow("result", result)
        # cv.waitKey(0)

    @staticmethod
    def get_shape_type(area, perimeter):
        circularity = (4 * 3.1416 * area) / (perimeter**2)
        # print("Circularity: ", circularity)
        if circularity > 0.85:
            return "circle"
        elif circularity > 0.1:
            return "oval or capsule"
        else:
            return "egg"
