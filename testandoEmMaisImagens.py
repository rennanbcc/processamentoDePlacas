import cv2
import numpy as np 
import matplotlib

def detctar(y):
    imagen = cv2.imread('C:/Users/PC/Desktop/imagem/image_'+y+'.jpg')
    cv2.imshow('Imagen', imagen)

    #################################################################

    imgCinza = cv2.cvtColor(imagen.copy(), cv2.COLOR_RGB2GRAY)
    #cv2.imshow('Cinza', imgCinza)

    Z = imagen.reshape((-1,3))

# convert to np.float32
    Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 2
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_PP_CENTERS)

# Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((imagen.shape))
    cv2.imshow('REs', res2)

    #################################################################

    desfoque = cv2.GaussianBlur(imgCinza, (3, 3), 1)

    mediana = cv2.medianBlur(imgCinza.copy(), 7)

    kernel1 = np.ones((7,7),np.float32)/25

    kernel2 = np.ones((3, 3), np.uint8)

    filter2D = cv2.filter2D(imgCinza,-1,kernel1)

    blur = cv2.blur(imgCinza,(7,7))

    bilateralFilter = cv2.bilateralFilter(imgCinza,15,15*2,15/2)
    
    #cv2.imshow('Desfoque',mediana)

    #################################################################

    #imgCinza =cv2.cvtColor(mediana, cv2.COLOR_RGB2GRAY)

    #################################################################

    #img_erosion = cv2.erode(mediana, kernel2, iterations=2) 

    #img_dilation = cv2.dilate(mediana, kernel2, iterations=2) 

    #cv2.imshow('Dilatacao', img_dilation)
    #cv2.imshow('Erosao', img_erosion)

    #(T, bordas) = cv2.threshold(img_dilation, 140, 255, cv2.THRESH_BINARY)
    
    #cv2.imshow('Bordas', bordas)

    #contornos, hier = cv2.findContours(bordas, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    #cont = cv2.drawContours(imagen.copy(), contornos, -1, (0, 255, 0), 2)
    #cv2.imshow('Contornos', cont)

    imgOut = cv2.adaptiveThreshold(imgCinza,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,2005,2)
 
    contornos, hier = cv2.findContours(imgOut, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cont = cv2.drawContours(imagen.copy(), contornos, -1, (0, 255, 0), 2)
    #cv2.imshow('Contornos', cont)
    
    cv2.imshow('Hougs', imgOut)

    
    for a in contornos:
        
        perimetro = cv2.arcLength(a, True)
        
        if perimetro > 270 and perimetro < 500:
            aproximado = cv2.approxPolyDP(a, 0.09 * perimetro, True)
                
            if len(aproximado) == 4:
                (posX, posY, altura, largura) = cv2.boundingRect(a)
                cv2.rectangle(imagen, (posX, posY), (posX + altura, posY + largura), (0,0,255), 2)
                placa = imagen[posY : posY + largura, posX : posX + altura]
                cv2.imwrite('C:/Users/PC/Desktop/Nova Pasta/Placas/Placa'+y+'.png', placa) 

    cv2.imshow('Quadrados', imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


for a in range(1, 50):
    y = str(a)
    detctar(y)