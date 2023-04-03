
from abc import abstractmethod

import abc
import numpy as np


from glob import glob
from tqdm import tqdm

import cv2


class Distance:

    def get_distance(self, p1: int, p2: int) -> float:
        return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    def get_mid_point(self, p1: int, p2: int):
        midpoint = ((p1[0] + p2[0]) // 2, (p1[1] + p2[1]) // 2)
        return midpoint

    def get_points(self, index, approx) -> list:
        p1 = tuple(approx[index][0])
        p2 = tuple(approx[(index + 1) % len(approx)][0])
        return [p1, p2]


class Shape:

    @staticmethod
    def get_widt_height(img):
        return img.shape

    def get_center_radius(self, approx):
        return cv2.minEnclosingCircle(approx)

    def get_center(self, center):
        return tuple(map(int, center))


class Kernel2Img:

    # def __init__(self,img) :
    #     self.img

    def get_blur_guassian(self, gray_image):
        return cv2.GaussianBlur(gray_image, (5, 5), 0)

    def get_kernel_5x5(self):
        return np.ones((5, 5), np.uint8)

    def get_img2dilation(self, blur_image):
        return cv2.dilate(blur_image, self.get_kernel_5x5(), iterations=3)

    def get_img2erosion(self, img):
        return cv2.erode(img, self.get_kernel_5x5(), iterations=3)

    def get_gray_image(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def get_image_read(self, img_path: str):
        return cv2.imread(img_path)

    def get_edges(self, img):
        return cv2.Canny(img, 30, 60)

    def get_find4contorus(self, edges):
        contours, _ = cv2.findContours(
            edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def get_epsilon(self, contour):
        return (0.01 * cv2.arcLength(contour, True))

    def get_resize_img(self,img,new_height= 500):
        height, width, channels = img.shape
        new_width = int(new_height * (width / height))
        img = cv2.resize(img, (new_width, new_height))
        return img
    
    def get_approx(self, contour):
        return cv2.approxPolyDP(contour, self.get_epsilon(contour), True)

    def get_zero_image(self, img_zero_shape: Shape.get_widt_height):
        print(type(img_zero_shape))
        return np.zeros(img_zero_shape, np.uint8)


class GetImages:
    color_radius = (100, 100, 100)
    color_distance = (50, 50, 50)

    def __init__(self, fileType="*.jpeg", filesPath='/HW1/images/'):
        self.fileType = fileType
        self.filesPath = filesPath

    def get_point_distance(self, img, midpoint: int, p1: int, p2: int, distance: float):

        if (distance > 30):
            cv2.putText(img, f" {distance:.1f}",
                        midpoint, cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_distance, 1)

        return img

    def get_text_radius_img(self, radius: int, center: int, img):
        cv2.putText(
            img, f"{radius}", center, cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.color_radius, 1)
        return img

    def getImages4Glob(self) -> list:
        return glob(self.filesPath+self.fileType)

    def getImages4tqdm(self) -> list:
        return tqdm(self.getImages4Glob())


class Proccess4Draw(Distance, Shape, GetImages, Kernel2Img):
    # static color
    color = (50, 50, 50)
    radiusColor = (100, 100, 100)
    p1 = 0
    p2 = 1

    def __init__(self, fileType: str, filesPath: str):
        GetImages.__init__(self, fileType=fileType, filesPath=filesPath)
        Distance.__init__(self)
        Shape.__init__(self,)
        Kernel2Img.__init__(self,)

    def draw_countur(self, contours, img):
        for contour in contours:
            approx = self.get_approx(contour)
            for i in range(len(approx)):
                get_points = self.get_points(index=i, approx=approx)
                p1 = get_points[self.p1]
                p2 = get_points[self.p2]
                cv2.line(img, p1,
                         p2, self.color, 2)
                img = self.get_point_distance(img=img, p1=p1, p2=p2,midpoint=self.get_mid_point(p1,p2), distance=self.get_distance(
                    p1, p2))

            if len(approx) > 10:
                center = self.get_center(self.get_center_radius(approx)[0])
                radius = int(self.get_center_radius(approx)[1])
                img = self.get_text_radius_img(radius=radius, center=center, img=img)

        return img


class Image2Drawer(Proccess4Draw):
    def __init__(self, fileType: str, filesPath: str):
        Proccess4Draw.__init__(self, fileType=fileType, filesPath=filesPath)

    def drawed_img(self,image):
        # print(image_path, " gelen image türü",
        #           Shape.get_widt_height(image))
        backend_image = self.get_zero_image(Shape.get_widt_height(image))
        gray_image = self.get_gray_image(image)
        blur = self.get_blur_guassian(gray_image)
        dilation = self.get_img2dilation(blur)
        erosion = self.get_img2erosion(dilation)
        get_edges = self.get_edges(erosion)
        contours = self.get_find4contorus(get_edges)
        drawed_img = self.draw_countur(contours, backend_image)
        return drawed_img
    def draw_paper_show(self):
        for image_path in self.getImages4tqdm():

            image = self.get_image_read(image_path)
            drawed_img=self.drawed_img(image)
            cv2.imshow("drawed_img", drawed_img)
            # cv2.imshow("backend_image", backend_image)
            # time.sleep(2)
            cv2.waitKey(5000)


if __name__ == '__main__':
    import os
    import time
    fileType = "*.jpeg"
    filesPath = os.getcwd()+'/HW1/images/'
    # Image2Drawer(filesPath=filesPath, fileType=fileType).draw_paper_show()
