import cv2
import numpy as np 
import matplotlib

def detctar(y):
    imagen = cv2.imread('C:/Users/PC/Desktop/Nova Pasta/Imagem/download'+y+'.jpg')
    cv2.imshow('Imagen', imagen)

    #################################################################

    imgCinza = cv2.cvtColor(imagen.copy(), cv2.COLOR_RGB2GRAY)
    #cv2.imshow('Cinza', imgCinza)

    #################################################################

    desfoque = cv2.GaussianBlur(imgCinza, (3, 3), 1)

    mediana = cv2.medianBlur(imagen.copy(), 9)

    kernel1 = np.ones((7,7),np.float32)/25

    kernel2 = np.ones((5, 5), np.uint8)

    filter2D = cv2.filter2D(imgCinza,-1,kernel1)

    blur = cv2.blur(imgCinza,(7,7))

    bilateralFilter = cv2.bilateralFilter(imgCinza,15,15*2,15/2)
    
    cv2.imshow('Desfoque',mediana)

    #################################################################

    imgCinza =cv2.cvtColor(mediana, cv2.COLOR_RGB2GRAY)

    #################################################################

    img_erosion = cv2.erode(mediana, kernel2, iterations=1) 

    img_dilation = cv2.dilate(imgCinza, kernel2, iterations=2) 

    cv2.imshow('Dilatacao', img_dilation)

    #################################################################
                                        #blur 130 P
    (T, bordas) = cv2.threshold(img_dilation, 160, 255, cv2.THRESH_BINARY)
    cv2.imshow('Bordas', bordas)

    #################################################################

    contornos, hier = cv2.findContours(bordas, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cont = cv2.drawContours(imagen.copy(), contornos, -1, (0, 255, 0), 2)
    cv2.imshow('Contornos', cont)

    #################################################################

    for a in contornos:
        
        perimetro = cv2.arcLength(a, True)
        
        if perimetro > 180 and perimetro < 400 :
            aproximado = cv2.approxPolyDP(a, 0.04 * perimetro, True)
                
            if len(aproximado) == 4:
                (posX, posY, altura, largura) = cv2.boundingRect(a)
                if (altura*largura)>2500 and (altura*largura)<7000:
                    print(altura*largura)
                    print(posX, posY)
                    cv2.rectangle(imagen, (posX, posY), (posX + altura, posY + largura), (0,0,255), 2)
                    placa = imagen[posY : posY + largura, posX : posX + altura]
                    cv2.imwrite('C:/Users/PC/Desktop/Nova Pasta/Placas/Placa'+y+'.png', placa) 



    cv2.imshow('Quadrados', imagen)
    #cv2.imshow('Placas', placa)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


for a in range(0, 17):
    y = str(a)
    detctar(y)