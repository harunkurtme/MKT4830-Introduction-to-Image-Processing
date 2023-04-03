import cv2
import tkinter as tk
from PIL import Image, ImageTk
import os
from glob import glob
from tqdm import tqdm
import os

from model import Image2Drawer

class ImageWindow(Image2Drawer):
    fileType = "*.jpeg"
    filesPath = os.getcwd()+'/HW1/images/'
    def __init__(self, master):
        Image2Drawer.__init__(self=self,filesPath=self.filesPath,fileType=self.fileType)
        self.master = master
        
        self.master.title("Teknik Resim Yazdırma Arayüzü 2006A701_Harun_KURT")
        self.image_list=[]
        for img in self.getImages4tqdm():
            self.image_list.append(img)
        self.current_image = 0
        self.processed_label = tk.Label(self.master)
        self.processed_label.pack(side=tk.RIGHT)
        self.original_label = tk.Label(self.master)
        self.original_label.pack(side=tk.LEFT)
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.BOTTOM)
        self.back_button = tk.Button(self.button_frame, text="<<", command=self.back)
        self.back_button.pack(side=tk.LEFT)
        self.save_button = tk.Button(self.button_frame, text="Kaydet", command=self.save_image)
        self.save_button.pack(side=tk.LEFT)
        self.next_button = tk.Button(self.button_frame, text=">>", command=self.next)
        self.next_button.pack(side=tk.RIGHT)
        self.load_image()
        
    def load_image(self):
        image_path = self.image_list[self.current_image]
        image = self.get_image_read(image_path)
        image=self.get_resize_img(image)
        self.original_photo = ImageTk.PhotoImage(image=Image.fromarray(image))
        self.original_label.config(image=self.original_photo)
        self.processed_func(self.drawed_img(image=image))
    
    def processed_func(self,processed_img):
        self.processed_photo = ImageTk.PhotoImage(image=Image.fromarray(processed_img))
        self.processed_label.config(image=self.processed_photo)
        self.processed_image = processed_img
        
    def first_load_images(self):
        image_file = self.image_list[self.current_image]
        img = cv2.imread(image_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channels = img.shape
        new_height = 500
        new_width = int(new_height * (width / height))
        img = cv2.resize(img, (new_width, new_height))
        self.original_photo = ImageTk.PhotoImage(image=Image.fromarray(img))
        self.original_label.config(image=self.original_photo)
        processed_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        processed_img = cv2.Canny(processed_img, 100, 200)
        self.processed_photo = ImageTk.PhotoImage(image=Image.fromarray(processed_img))
        self.processed_label.config(image=self.processed_photo)
        self.processed_image = processed_img
    

    def save_image(self):
        file_name = os.path.splitext(self.image_list[self.current_image])[0] + "_processed.jpg"
        cv2.imwrite(file_name, self.processed_image)

    def next(self):
        self.current_image += 1
        if self.current_image == len(self.image_list):
            self.current_image = 0
        self.load_image()

    def back(self):
        self.current_image -= 1
        if self.current_image < 0:
            self.current_image = len(self.image_list) - 1
        self.load_image()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageWindow(root)
    root.mainloop()
