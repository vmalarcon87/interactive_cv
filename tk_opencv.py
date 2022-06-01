from copy import copy
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np


def resizeTiff(filename):
    img = cv2.imread(filename)
    
    for scale_percent in [3]:
        height = img.shape[0]
        width = img.shape[1]
        
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim)
        return resized

def select_image():
    path_image = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
        ("image", ".tif")])
    
    if len(path_image) > 0:
        global image
        global green
        
        image = cv2.imread(path_image) #resizeTiff(path_image)
        green = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        upper = np.array([36, 25, 25])
        lower = np.array([86, 255, 255])      
        green = cv2.inRange(green, upper, lower)
        

        im = Image.fromarray(image)
        img = ImageTk.PhotoImage(image=im)
        lblInputImage.configure(image=img)
        lblInputImage.image = img
        
        imgray = Image.fromarray(green)
        imggray = ImageTk.PhotoImage(image=imgray)
        lblInputImageGray.configure(image=imggray)
        lblInputImageGray.image = imggray

        lblInfo1 = Label(root, text="Input image:")
        lblInfo1.grid(column=0, row=1)
        
        lblInfoGray = Label(root, text="Gray image:")
        lblInfoGray.grid(column=1, row=1)

        lblOutputImage.image = ""

        
        
        

def reset_image():
    global image
    im = Image.fromarray(image)
    img = ImageTk.PhotoImage(image=im)
    lblInputImage.configure(image=img)
    lblInputImage.image = img
    lblInfo1 = Label(root, text="Input image:")
    lblInfo1.grid(column=0, row=1)
    lblOutputImage.image = ""

def apply_morpho():
    global image
    global copy
    copy = image.copy()
    r = slider_w.get()
    c = slider_h.get()
    kernel = np.ones((r,c),np.uint8)
    
    if morpho.get() == 1:
        copy = cv2.dilate(copy, kernel)

    elif morpho.get() == 2:
        copy = cv2.erode(copy, kernel)

    elif morpho.get() == 3:
        copy = cv2.morphologyEx(copy, cv2.MORPH_OPEN, kernel)
    
    elif morpho.get() == 4:
        copy = cv2.morphologyEx(copy, cv2.MORPH_CLOSE, kernel)
    
    elif morpho.get() == 5:
        copy = cv2.morphologyEx(copy, cv2.MORPH_GRADIENT, kernel)
    
    elif morpho.get() == 6:
        copy = cv2.morphologyEx(copy, cv2.MORPH_TOPHAT, kernel)
    
    elif morpho.get() == 7:
        copy = cv2.morphologyEx(copy, cv2.MORPH_BLACKHAT, kernel)

    im = Image.fromarray(copy)
    img = ImageTk.PhotoImage(image=im)
    lblOutputImage.configure(image=img)
    lblOutputImage.image = img
    lblInfo3 = Label(root, text="Output Image:")
    lblInfo3.grid(column=4, row=1)
    

def blur_image():
    global image
    global copy
    copy = image.copy()
    blur = cv2.medianBlur(copy, blur_slider.get())
    im = Image.fromarray(blur)
    img = ImageTk.PhotoImage(image=im)
    lblOutputImage.configure(image=img)
    lblOutputImage.image = img
    lblInfo3 = Label(root, text="Output Image:")
    lblInfo3.grid(column=4, row=1)

def calcule_contours():
    global image
    global copy
    contours, hierarchy1 = cv2.findContours(copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    drawCont = cv2.drawContours(copy, contours, -1, (0, 0, 255), 2)
    im = Image.fromarray(drawCont)
    img = ImageTk.PhotoImage(image=im)
    lblOutputImage.configure(image=img)
    lblOutputImage.image = img

   
root = Tk()
root.geometry('1500x1000')

lblInputImage = Label(root)
lblInputImage.grid(column=0, row=2, columnspan=4)

lblInputImageGray = Label(root)
lblInputImageGray.grid(column=4, row=2, columnspan=4)

lblOutputImage = Label(root)
lblOutputImage.grid(column=8, row=2)



lblInfo2 = Label(root, text="Features", width=10)
lblInfo2.grid(column=0, row=5)

width_label = Label(root, text="Width", width=10)
width_label.grid(column=1, row=3)

height_label = Label(root, text="Height", width=10)
height_label.grid(column=2, row=3)

contours_btn = Button(root, text="Contours", width=10, command=calcule_contours)
contours_btn.grid(column=3, row=3)


slider_w = Scale(root, from_=0, to=5, orient=HORIZONTAL)
slider_h = Scale(root, from_=0, to=5, orient=HORIZONTAL)
slider_w.grid(column=1, row=4)
slider_h.grid(column=2, row=4)

morpho = IntVar()
rad1 = Radiobutton(root, text='Dilate', value=1, variable=morpho)
rad2 = Radiobutton(root, text='Erode', value=2, variable=morpho)
rad3 = Radiobutton(root, text='Opening', value=3, variable=morpho)
rad4 = Radiobutton(root, text='Closing', value=4, variable=morpho)
rad5 = Radiobutton(root, text='Gradient', value=5, variable=morpho)
rad6 = Radiobutton(root, text='Top Hat', value=6, variable=morpho)
rad7 = Radiobutton(root, text='Black Hat', value=7, variable=morpho)

rad1.grid(column=1, row=5)
rad2.grid(column=1, row=6)
rad3.grid(column=1, row=7)
rad4.grid(column=1, row=8)
rad5.grid(column=2, row=5)
rad6.grid(column=2, row=6)
rad7.grid(column=2, row=7)

kernel_btn = Button(root, text="Exec", width=10, command=apply_morpho)
kernel_btn.grid(column=3, row=7)

blur_label = Label(root,text='Blur:')
blur_slider = Scale(root, from_=0, to=5, orient=HORIZONTAL)
blur_label.grid(column=0, row=9)
blur_slider.grid(column=1, row=9)
blur_btn = Button(root, text="Exec", width=10, command=blur_image)
blur_btn.grid(column=3, row=9)



btn = Button(root, text="Input", width=10, command=select_image)
btn.grid(column=0, row=0)

reset_btn = Button(root, text="Reset", width=10, command=reset_image)
reset_btn.grid(column=1, row=0)


root.mainloop()