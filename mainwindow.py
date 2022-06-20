import tkinter as tk
import cv2 as cv
import numpy as np

from PIL import Image as pilim
from PIL import ImageTk as pilimtk
from tkinter import filedialog
from tkinter import ttk
import rasterio

class MainWindow(tk.Tk):
    
    
    def __init__(self):

        tk.Tk.__init__(self)
        
        self.title("Main Window")
        self.geometry('1500x1000')
        
        self.tabControl = ttk.Notebook(self)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='RGB')
        self.tabControl.add(self.tab2, text='GRAY')
        self.tabControl.add(self.tab3, text='OUT')
        self.tabControl.add(self.tab4, text='GSD')
        self.tabControl.pack(expand = 1, fill ="both")

        self.lblInputImage = tk.Label(self.tab1)
        self.lblInputImageGray = tk.Label(self.tab2)
        self.lblOutputImage = tk.Label(self.tab3)
        self.lblRszImage = tk.Label(self.tab4)
        
        self.lblInputImage.grid(column=0, row=0, columnspan=4)
        self.lblInputImageGray.grid(column=0, row=0, columnspan=4)       
        self.lblOutputImage.grid(column=0, row=0, columnspan=4)       
        self.lblRszImage.grid(column=0, row=0, columnspan=4)       

        btn = tk.Button(self.tab1, text="Input", width=10, command=self.select_image)
        btn.grid(column=0, row=1)

        reset_btn = tk.Button(self.tab3, text="Reset", width=10, command=self.reset_image)
        reset_btn.grid(column=0, row=1)

        #contours_btn = tk.Button(self.tab3, text="Contours", width=10, command=self.calcule_contours)
        #contours_btn.grid(column=1, row=1)

       
        self.gsd_text = tk.StringVar()
        self.gsd_val = tk.Label(self.tab4, text='GSD Value: ', textvariable=self.gsd_text)
        self.gsd_val.grid(column=0, row=1)
        


    def select_image(self):
        path_image = filedialog.askopenfilename(
            filetypes = [("image", ".jpeg"), ("image", ".png"), ("image", ".jpg"), ("image", ".tif")])
        
        #path_image = "/home/vmalarcon/proyectos/PR-00680_HIBA/dataset/Images/Puente_Genil_Olivar_Tradicional.tif"
        if len(path_image) > 0:   
            self.image = cv.imread(path_image)
            self.green = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
            
            upper = np.array([36, 25, 25])
            lower = np.array([86, 255, 255])      
            self.green = cv.inRange(self.green, upper, lower)
            self.morpho = self.green.copy()
            self.rsz = self.green.copy()
            
            width, height = self.calcule_ratio(self.image.shape[1], self.image.shape[0])
            
            im = pilim.fromarray(self.image)
            im = im.resize((width,height),pilim.Resampling.NEAREST)
            img = pilimtk.PhotoImage(image=im)
            self.lblInputImage.configure(image=img)
            self.lblInputImage.image = img
            
            imgray = pilim.fromarray(self.green)
            imgray = imgray.resize((width,height),pilim.Resampling.NEAREST)
            imggray = pilimtk.PhotoImage(image=imgray)
            self.lblInputImageGray.configure(image=imggray)
            self.lblInputImageGray.image = imggray

            imout = pilim.fromarray(self.morpho)
            imout = imout.resize((width,height),pilim.Resampling.NEAREST)
            imgout = pilimtk.PhotoImage(image=imout)
            self.lblOutputImage.configure(image=imgout)
            self.lblOutputImage.image = imgout    

            imrsz = pilim.fromarray(self.rsz)
            imrsz = imrsz.resize((width,height),pilim.Resampling.NEAREST)
            imgrsz = pilimtk.PhotoImage(image=imrsz)
            self.lblRszImage.configure(image=imgrsz)
            self.lblRszImage.image = imgrsz  
            
            self.calculeGSD(path_image)  


    def reset_image(self):
        width, height = self.calcule_ratio(self.image.shape[1], self.image.shape[0])
        self.morpho = self.green.copy()
        self.rsz = self.green.copy()

        imout = pilim.fromarray(self.morpho)
        imout = imout.resize((width,height),pilim.Resampling.NEAREST)
        imgout = pilimtk.PhotoImage(image=imout)
        self.lblOutputImage.configure(image=imgout)
        self.lblOutputImage.image = imgout    
                
        imrsz = pilim.fromarray(self.rsz)
        imrsz = imrsz.resize((width,height),pilim.Resampling.NEAREST)
        imgrsz = pilimtk.PhotoImage(image=imrsz)
        self.lblRszImage.configure(image=imgrsz)
        self.lblRszImage.image = imgrsz    
    
    def calcule_ratio(self, real_width, real_height):
        fixed_height = 800
        height_percent = (fixed_height / real_height)
        width_size = int(real_width * height_percent)
        return(width_size, fixed_height)

   
    def calculeGSD(self, path_image):  
        raster = rasterio.open(path_image)
        gt = raster.transform
        self.gsdX = gt[0]
        self.gsdY =-gt[4]
        self.unit = raster.crs.linear_units
        s = self.gsd_text.get()
        s = "x: {} ; y: {} ; Units: {}".format(gt[0], gt[4], raster.crs.linear_units)
        self.gsd_text.set(s)
