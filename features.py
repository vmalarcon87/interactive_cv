import tkinter as tk
import cv2 as cv
import numpy as np


from PIL import Image as pilim
from PIL import ImageTk as pilimtk

class Feature(tk.Toplevel):
    
    def __init__(self, parent):
        
        super().__init__(parent)

        self.parent = parent
        self.geometry('600x600')
        self.title('Toplevel Window')    
        self.attributes('-topmost', True)

        self.lblInfo2 = tk.Label(self, text="Features", width=10)
        self.lblInfo2.grid(column=0, row=5)

        self.width_label = tk.Label(self, text="Width", width=10)
        self.width_label.grid(column=1, row=3)

        self.height_label = tk.Label(self, text="Height", width=10)
        self.height_label.grid(column=2, row=3)

        self.slider_w = tk.Scale(self, from_=0, to=50, orient=tk.HORIZONTAL)
        self.slider_h = tk.Scale(self, from_=0, to=50, orient=tk.HORIZONTAL)
        self.slider_w.grid(column=1, row=4)
        self.slider_h.grid(column=2, row=4)

        self.morpho = tk.IntVar()
        self.rad1 = tk.Radiobutton(self, text='Dilate', value=1, variable=self.morpho)
        self.rad2 = tk.Radiobutton(self, text='Erode', value=2, variable=self.morpho)
        self.rad3 = tk.Radiobutton(self, text='Opening', value=3, variable=self.morpho)
        self.rad4 = tk.Radiobutton(self, text='Closing', value=4, variable=self.morpho)
        self.rad5 = tk.Radiobutton(self, text='Gradient', value=5, variable=self.morpho)
        self.rad6 = tk.Radiobutton(self, text='Top Hat', value=6, variable=self.morpho)
        self.rad7 = tk.Radiobutton(self, text='Black Hat', value=7, variable=self.morpho)

        self.rad1.grid(column=1, row=5)
        self.rad2.grid(column=1, row=6)
        self.rad3.grid(column=1, row=7)
        self.rad4.grid(column=1, row=8)
        self.rad5.grid(column=2, row=5)
        self.rad6.grid(column=2, row=6)
        self.rad7.grid(column=2, row=7)
        self.morpho.set(1)

        self.kernel_btn = tk.Button(self, text="Exec", width=10, command=self.apply_morpho).grid(column=3, row=7)      
        
        self.blur_label = tk.Label(self,text='Blur:')
        self.blur_slider = tk.Scale(self, from_=0, to=50, orient=tk.HORIZONTAL)
        self.blur_label.grid(column=0, row=9)
        self.blur_slider.grid(column=1, row=9)
        self.blur_btn = tk.Button(self, text="Exec", width=10, command=self.blur_image)
        self.blur_btn.grid(column=3, row=9)

        self.gsd_entry = tk.Entry (self, width=10)
        self.gsd_entry.grid(column=1, row=11)
        self.gsd_button = tk.Button(self, text="GSD", width=10, command=self.resizeTiff)
        self.gsd_button.grid(column=3, row=11)
        
    def apply_morpho(self):

     
        r = self.slider_w.get()
        c = self.slider_h.get()
        
        kernel = np.ones((r,c),np.uint8)
        
        if self.morpho.get() == 1:
            self.parent.morpho = cv.dilate(self.parent.morpho, kernel)

        elif self.morpho.get() == 2:
            self.parent.morpho = cv.erode(self.parent.morpho, kernel)

        elif self.morpho.get() == 3:
            self.parent.morpho = cv.morphologyEx(self.parent.morpho, cv.MORPH_OPEN, kernel)
        
        elif self.morpho.get() == 4:
            self.parent.morpho = cv.morphologyEx(self.parent.morpho, cv.MORPH_CLOSE, kernel)
        
        elif self.morpho.get() == 5:
            self.parent.morpho = cv.morphologyEx(self.parent.morpho, cv.MORPH_GRADIENT, kernel)
        
        elif self.morpho.get() == 6:
            self.parent.morpho = cv.morphologyEx(self.parent.morpho, cv.MORPH_TOPHAT, kernel)
        
        elif self.morpho.get() == 7:
            self.parent.morpho = cv.morphologyEx(self.parent.morpho, cv.MORPH_BLACKHAT, kernel)

        width, height = self.parent.calcule_ratio(self.parent.image.shape[1], self.parent.image.shape[0])
            
        im = pilim.fromarray(self.parent.morpho)
        im = im.resize((width,height),pilim.Resampling.NEAREST)
        img = pilimtk.PhotoImage(image=im)
        self.parent.lblOutputImage.configure(image=img)
        self.parent.lblOutputImage.image = img           
    

    def blur_image(self):
        self.parent.morpho = cv.medianBlur(self.parent.morpho, self.blur_slider.get())
        width, height = self.parent.calcule_ratio(self.parent.image.shape[1], self.parent.image.shape[0])
        
        im = pilim.fromarray(self.parent.morpho)
        im = im.resize((width,height),pilim.Resampling.NEAREST)
        img = pilimtk.PhotoImage(image=im)
        self.parent.lblOutputImage.configure(image=img)
        self.parent.lblOutputImage.image = img           


    def resizeTiff(self):
        gsd_ = float(self.gsd_entry.get())
                
        gsdX = self.parent.gsdX
        gsdY = self.parent.gsdY
        unit = self.parent.unit
        
        x = 100*gsdX/gsd_
        y = 100*gsdY/gsd_

        width = int(self.parent.green.shape[1] * x / 100)
        height = int(self.parent.green.shape[0] * y / 100)
        dim = (width, height)
        
        rsz = cv.resize(self.parent.green, dim)
        im = pilim.fromarray(rsz)
        img = pilimtk.PhotoImage(image=im)
        self.parent.lblRszImage.configure(image=img)
        self.parent.lblRszImage.image = img

        s += "x: {} ; y: {} ; Units: {}".format(gsd_, gsd_, unit)
        self.parent.gsd_text.set(s)


    def calcule_contours(self):
        contours, hierarchy1 = cv.findContours(self.morpho, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        drawCont = cv.drawContours(self.morpho, contours, -1, (0, 0, 255), 2)
        im = pilim.fromarray(drawCont)
        img = pilimtk.PhotoImage(image=im)
        self.lblOutputImage.configure(image=img)
        self.lblOutputImage.image = img