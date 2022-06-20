import cv2 as cv
import numpy as np
import rasterio
from skimage.draw import line
 
####---------------------------------------------------------------------------###
def show_wait_destroy(winname, img):
    cv.imshow(winname, img)
    cv.moveWindow(winname, 500, 0)
    cv.waitKey(0)
    cv.destroyWindow(winname)

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
def mousePoints(event,x,y,flags,params):
    global counter 
    if event == cv.EVENT_LBUTTONDOWN:
        point_matrix[counter] = x,y
        counter = counter + 1
    



####---------------------------------------------------------------------------###
def draw_line(roi):
    global point_matrix 
    point_matrix = np.zeros((2,2),np.int)
    global counter 
    counter = 0
    roy_copy = roi.copy()
    '''
    while counter<=2:
        for x in range (0,2):
            cv.circle(roi,(point_matrix[x][0],point_matrix[x][1]),1,(0,255,0),cv.FILLED)
    
        if counter == 2:
            starting_x = point_matrix[0][0]
            starting_y = point_matrix[0][1]
            ending_x = point_matrix[1][0]
            ending_y = point_matrix[1][1]
            #cv.rectangle(roy_copy, (starting_x, starting_y), (ending_x, ending_y), (0, 255, 0), 1)
            cv.line(roy_copy, (starting_x, starting_y), (ending_x, ending_y), (0, 255, 0), thickness=1)
            print(starting_x, starting_y, ending_x, ending_y)
            break
        
        cv.imshow("Dibuja la Linea", roi)
        cv.setMouseCallback("Dibuja la Linea", mousePoints)
        cv.waitKey(1)
    '''
    #return [4,    551 ,    458 ,    551]
    return [10 ,102 ,1034 ,72]
    #return [starting_x, starting_y, ending_x, ending_y]


def calcule_lines(roi, pnts, difference, scale_value):     
    lne = line(pnts[0], pnts[1], pnts[2], pnts[3])
    c = np.array(list(zip(lne[0], lne[1])))

    red=0
    blue=0
    last = ""

    green = cv.cvtColor(roi, cv.COLOR_BGR2HSV)        
    upper = np.array([36, 25, 25])
    lower = np.array([86, 255, 255])      
    green = cv.inRange(green, upper, lower)

    ##########
    # Specify size on vertical axis
    # Apply adaptiveThreshold at the bitwise_not of gray, notice the ~ symbol
    # Transform source image to gray if it is not already
    
    gray = cv.bitwise_not(green)
    #bw = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 15, -2)
   
    #Show binary image
    #show_wait_destroy("binary", bw)
   
    # Create the images that will use to extract the horizontal and vertical lines
    '''
    horizontal = np.copy(gray)
    cols = horizontal.shape[1]
    horizontal_size = cols // 30    
    horizontalStructure = cv.getStructuringElement(cv.MORPH_RECT, (horizontal_size, 1))
    horizontal = cv.erode(horizontal, horizontalStructure)
    horizontal = cv.dilate(horizontal, horizontalStructure)
    # Show extracted horizontal lines
    show_wait_destroy("horizontal", horizontal)
    '''
    vertical = np.copy(gray)
    rows = vertical.shape[0]
    verticalsize = rows // 100

    kernel_r = 2*difference
    kernel_c = 2*difference

    kernel = np.ones((kernel_r, kernel_c),np.uint8)
    vertical = cv.dilate(green, kernel)
    vertical = cv.erode(vertical, kernel)
    '''
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv.getStructuringElement(cv.MORPH_RECT, (1, verticalsize))
    # Apply morphology operations
    vertical = cv.erode(vertical, verticalStructure)
    vertical = cv.dilate(vertical, verticalStructure)
    '''
    # Show extracted vertical lines
    show_wait_destroy("vertical", vertical)

    # Inverse vertical image
    #vertical = cv.bitwise_not(vertical)
    #show_wait_destroy("vertical_bit", vertical)
    
    try:
        for (x,y) in c :
            if vertical[y,x].any() > 0:
                #morpho[y,x] = (0, 0, 255)
                if "b" in last : red+=1
                last="r"
            else:
                #morpho[y,x] = (255, 0, 0)
                if "r" in last : blue+=1
                last="b"  
    except:
        pass

    print("PRE-MORPH " + str(scale_value) + " - WHITE: " + str(red))

    #cv.imshow("RESULTS", morpho)
    #cv.waitKey(0)
    #cv.destroyAllWindows()

    return vertical
 
####---------------------------------------------------------------------------###

path = "/home/vmalarcon/proyectos/PR-00680_HIBA/dataset/Images/20211029_olivar_RGB_mask.tif"
#path = "/home/vmalarcon/proyectos/PR-00680_HIBA/dataset/Images/Olivar_Super_intensivo.tif"
#path = "/home/vmalarcon/proyectos/PR-00680_HIBA/dataset/Images/Vinha_espaldera_2.tif"

original = cv.imread(path) 
height = original.shape[0]
width = original.shape[1]
print("Original height: {} , Original width: {}".format(height, width))


############## ESCALA PORCENTAJE
scale_percent = 5
difference_percent = round(100/scale_percent)
escalada_percent = resizeTiff(original, scale_percent)
#points_escalado = [[77  , 137],[4   ,378],[0   ,977],[433   ,989],[465  , 144]]#[]
points_escalado = [[280 ,  597],[320   ,573],[1262   ,581],[1261   ,691],[225   ,687]]#[]
#points_escalado = []

'''
cv.imshow('Imagen escalada', escalada_percent)
cv.setMouseCallback('Imagen escalada', click_event)
cv.waitKey(0)
cv.destroyAllWindows()
'''

roi_percent = selectROI(escalada_percent, points_escalado)

pnts_line_escalado = draw_line(roi_percent)
#morpho_escalado = calcule_lines(roi_percent, pnts_line_escalado, 1, 10)


############## ORIGINAL
points_original = [(x*difference_percent,y*difference_percent) for (x,y) in points_escalado]
roi_original = selectROI(original, points_original)

#cv.imshow("image", roi_original)
#cv.waitKey(0)

pnts_line_original = [x*difference_percent for x in pnts_line_escalado]
#morpho_original = calcule_lines(roi_original, pnts_line_original, difference_percent, 100)



############## GSD
gsdX = calculeGSD(path)
gsd_list = np.linspace(start = 0.1, stop = 2, num=10, endpoint = True)

for gsd_ in gsd_list :
    scale_gsd_x = 100*gsdX/gsd_
    difference_gsd = round(100/scale_gsd_x)
    escalada_gsd = resizeTiff(original, scale_gsd_x)

    points_gsd = [(round(x/difference_gsd),round(y/difference_gsd)) for (x,y) in points_original]
    roi_gsd = selectROI(escalada_gsd, points_gsd)
    
    pnts_line_gsd = [round(x/difference_gsd) for x in pnts_line_original]
    morpho_gsd = calcule_lines(roi_gsd, pnts_line_gsd, 1, gsd_)


############## RESULTADOS

cv.destroyAllWindows()