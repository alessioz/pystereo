#!/usr/bin/python
from numarray import *
import Image
import ImageFilter
import sys

versione = 0.1

imsx = Image.open("IMG_1376_1.JPG")
imdx = Image.open("IMG_1377_1.JPG")


#metto in una stringa i valori dei pixel (da Image)
#put in a string pixel values
immaginesx = list(imsx.getdata())
immaginedx = list(imdx.getdata())
#print type(immaginesx)

#li ordino in una matrice con la dimensine dell'immagine (da numarray)
#put them in a matrix with dimensions of image
matricesx = reshape(immaginesx, (imsx.size[1],imsx.size[0]))
matricedx = reshape(immaginedx, (imdx.size[1],imdx.size[0]))
#print type(matricedx)

#dimensioni della finestra scorrevole
xfinestra = 20
yfinestra = 20

#dimensioni dell'area su cui si effettua l'elaborazione
xregione = 400
yregione = 600

steprange= 50
#larghezzaimgindx = imdx.size[0]-1
#lunghezzaimgindx = imdx.size[1]-1

depth=[]
correlazione=[]
for riga in range(0,yregione, yfinestra):		# elaborazione riga per riga (in verticale)
	for finestra in range(0, xregione, xfinestra):
		indici =[]
		for step in range(steprange):	# scorrimento della finestra sulla riga
			somma = 0
					# qui sotto calcolo la matrice differenza per ogni step
			matricediff = matricedx[riga:riga+yfinestra , finestra:finestra+xfinestra] - matricesx[riga:riga+yfinestra , finestra+step:finestra+xfinestra+step]
			matricediff2 = matricediff**2
					# sommo gli elementi della matrice differenza (DA VERIFICARE: li somma tutti o solo prima riga?)
			somma = matricediff2.sum()
					# normalizzo la somma e creo una lista con tutti gli indici della riga
			indice = somma/(xfinestra*yfinestra)
			indici.append(indice)
		depth.append(indici.index(min(indici)))  # l'indice col valore pi� passo � quello che ha minore differenza fra le 2 img, ne annoto la posizione (sequenziale per step)
		#correlazione.append(min(indici))
	print riga
	
#print depth
#print len(depth)
ydimensione = yregione/yfinestra
xdimensione = xregione/xfinestra

#correlazioneimage = reshape(correlazione, (ydimensione, xdimensione))
#print correlazioneimage
depthimage = reshape(depth, (ydimensione, xdimensione))
print depthimage

#if correlazioneimage > 1000:
	#correlazioneimage = 0
#print correlazioneimage

#vedi masked e spline_filter

nomefile ="IMG_vers%s_xwin%s_ywin%s_step%s.jpg" % (versione, xfinestra, yfinestra, steprange)

from scipy import *

toimage(depthimage).resize((xregione,yregione)).save(nomefile)
#imsave("correlazione_fungo.jpg", correlazioneimage)

