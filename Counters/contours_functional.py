import cv2 as cv
import numpy as np
import rasterio

####---------------------------------------------------------------------------###

def calculeGSD(img):

    raster = rasterio.open(img)
    gt = raster.transform
    gsdX = gt[0]
    gsdY =-gt[4]
    unit = raster.crs.linear_units   

    print("GSD: " , gsdX)
    
    return gsdX  

####---------------------------------------------------------------------------###

def resizeTiff(img, scale):
    width = round(img.shape[1] * scale / 100)
    height = round(img.shape[0] * scale / 100)
    dim = (width, height)
    rsz = cv.resize(img, dim)
    return rsz



####---------------------------------------------------------------------------###

def selectROI(img, points_list):
    
    pts = np.array(points_list) 
    pts = pts.reshape((-1, 1, 2))
  
    cv.polylines(img=img, pts=[pts], isClosed=True, color=(255,0,0), thickness=2)

    ## (1) Crop the bounding rect
    rect = cv.boundingRect(pts)
    x,y,w,h = rect
    croped = img[y:y+h, x:x+w].copy()

    ## (2) make mask
    pts = pts - pts.min(axis=0) 
    mask = np.zeros(croped.shape[:2], np.uint8)
    cv.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv.LINE_AA)

    ## (3) do bit-op
    dst = cv.bitwise_and(croped, croped, mask=mask)
    return dst


####---------------------------------------------------------------------------###

def click_event(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        print(x, ' ', y)
        points_escalado.append([x,y])

 ####---------------------------------------------------------------------------###

def executeMorpho(img, difference):
    
    morpho = cv.cvtColor(img, cv.COLOR_BGR2HSV)        
    upper = np.array([36, 25, 25])
    lower = np.array([86, 255, 255])      
    morpho = cv.inRange(morpho, upper, lower)
   
    r = difference
    c = difference
    
    ksize = 21 if difference > 1 else 1
    kernel = np.ones((r,c),np.uint8)
    
     
    morpho = cv.dilate(morpho, kernel)
    morpho = cv.erode(morpho, kernel)
    morpho = cv.medianBlur(morpho, ksize)
    

    return morpho


####---------------------------------------------------------------------------###

path = "/home/vmalarcon/proyectos/PR-00680_HIBA/dataset/Images/Almendro_RGB.tif"
#path = "/home/vmalarcon/proyectos/PR-00680_HIBA/dataset/Images/Puente_Genil_Olivar_Tradicional.tif"

original = cv.imread(path) 
height = original.shape[0]
width = original.shape[1]
print("Original height: {} , Original width: {}".format(height, width))


############## ESCALA PORCENTAJE
scale_percent = 10
difference_percent = round(100/scale_percent)
escalada_percent = resizeTiff(original, scale_percent)
points_escalado = []

cv.imshow('Imagen escalada', escalada_percent)
cv.setMouseCallback('Imagen escalada', click_event)
cv.waitKey(0)
cv.destroyAllWindows()

roi_percent = selectROI(escalada_percent, points_escalado)
morpho_percent = executeMorpho(roi_percent, 0)

cv.imshow("image", morpho_percent)
cv.waitKey(0)

contours, hierarchy1 = cv.findContours(morpho_percent, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
drawCont1 = cv.drawContours(roi_percent, contours, -1, (0, 0, 255), 2)

print("PERCENT - Number: ", len(contours))

############## ORIGINAL
points_original = [(x*difference_percent,y*difference_percent) for (x,y) in points_escalado]
roi_original = selectROI(original, points_original)
morpho_original = executeMorpho(roi_original, difference_percent)

cv.imshow("image", morpho_original)
cv.waitKey(0)

cv.imshow('DRAW CONT',drawCont1)
cv.waitKey(0)

contours3, hierarchy3 = cv.findContours(morpho_original, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
drawCont3 = cv.drawContours(roi_original, contours3, -1, (0, 0, 255), 2)
cv.imshow('DRAW CONT',drawCont3)
cv.waitKey(0)

print("ORIGINAL - Number: ", len(contours3))

############## GSD
gsdX = calculeGSD(path)
gsd_list = np.linspace(start = gsdX, stop = 2, num=10, endpoint = True)

for gsd_ in gsd_list :
    scale_gsd_x = 100*gsdX/gsd_
    difference_gsd = round(100/scale_gsd_x)
    escalada_gsd = resizeTiff(original, scale_gsd_x)
    points_gsd = [(round(x/difference_gsd),round(y/difference_gsd)) for (x,y) in points_original]
    roi_gsd = selectROI(escalada_gsd, points_gsd)
    morpho_gsd = executeMorpho(roi_gsd, 0)

    cv.imshow('roi gsd', roi_gsd)
    cv.waitKey(0)
    cv.destroyAllWindows()   

    cv.imshow("image", morpho_gsd)
    cv.waitKey(0)

    contours2, hierarchy2 = cv.findContours(morpho_gsd, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    drawCont2 = cv.drawContours(roi_gsd, contours2, -1, (0, 0, 255), 2)
    cv.imshow('DRAW CONT',drawCont2)
    cv.waitKey(0)

    print("GSD: " , gsd_, " - Number: ", len(contours2))

############## RESULTADOS


cv.destroyAllWindows()