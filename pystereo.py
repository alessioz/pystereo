#!/usr/bin/python
from numpy import *
import Image
import ImageFilter
import sys
import time
import datetime
from pylab import *

versione = 0.2

imsx = Image.open("wopmay2sx.jpg")
imdx = Image.open("wopmay2dx.jpg")


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
xfinestra = 10
yfinestra = 10

#dimensioni dell'area su cui si effettua l'elaborazione
xregione = 400
yregione = 500

sogliacorr = 1.05

steprange= 70
#larghezzaimgindx = imdx.size[0]-1
#lunghezzaimgindx = imdx.size[1]-1
depth=[]
correlazione=[]

#from scipy.misc.pilutil import *
numeronull = 0
numerodati = 0
inizio = time.clock()
for riga in range(0,yregione, yfinestra):		# elaborazione riga per riga (in verticale)
	for finestra in range(0, xregione, xfinestra):
		indici =[]
		univoco =[]
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
		#print mean(indici)/min(indici)
		depth.append(indici.index(min(indici)))  # l'indice col valore piu basso e' quello che ha minore differenza fra le 2 img, ne annoto la posizione (sequenziale per step)
		#matricediff = matricedx[riga:riga+yfinestra , finestra:finestra+xfinestra] - matricesx[riga:riga+yfinestra , finestra+indici.index(min(indici)):finestra+xfinestra+indici.index(min(indici))]
		#nomematricediff = "matrixdiff_row%s_coloumn%s.jpg" % (riga, finestra)
		#toimage(matricediff).resize((50,50)).save(nomematricediff)
		univoco = indici
		minimoassoluto = float(min(univoco))
		univoco.remove(min(univoco))
		minimorelativo = float(min(univoco))
		rapportominimi = minimorelativo/minimoassoluto
		#print minimorelativo, minimoassoluto, rapportominimi
		
		if rapportominimi > sogliacorr:
			numerodati += 1
			correlazione.append(1)
			#plot(indici)
			#legend()
			#show()
			#nomegrafico = "riga%s_finestra%s.png" % (riga,finestra)
			#savefig(nomegrafico)
			#close()
		
		else:
			correlazione.append(0)
			#depth.append(0)
			#depth.append("None")
			numeronull +=1
		#plot(indici)
		#legend()
		#show()
		#nomegrafico = "riga%s_finestra%s.png" % (riga,finestra)
		#savefig(nomegrafico)
		#close()
	stimato = (time.clock()-inizio)/(riga+yfinestra)*(yregione)+inizio
	print riga, datetime.timedelta(seconds = stimato), datetime.timedelta( seconds = (stimato -time.clock()))
print numerodati, numeronull
#print depth
#print len(depth)
ydimensione = yregione/yfinestra
xdimensione = xregione/xfinestra


	
correlazioneimage = reshape(correlazione, (ydimensione, xdimensione))
print correlazioneimage
depthimage = reshape(depth, (ydimensione, xdimensione))
print depthimage
depthimage = correlazioneimage*depthimage
#from scipy.interpolate.interpolate import interp2d
#print interp2d(390,500,depthimage)

#if correlazioneimage > 1000:
	#correlazioneimage = 0
#print correlazioneimage

#vedi masked e spline_filter

oggetto = "wopmay3"
dimfiltro = 0
nomefile ="%s_vers%s_xwin%s_ywin%s_step%s_MedianFilter%s.jpg" % (oggetto,versione, xfinestra, yfinestra, steprange, dimfiltro)
nomecorrelazione = "correlazione_"+nomefile

from scipy.misc.pilutil import *
if dimfiltro == 0:
	nomefile ="%s_vers%s_xwin%s_ywin%s_step%s_NoFilter_threshold%s.jpg" % (oggetto,versione, xfinestra, yfinestra, steprange, sogliacorr)
	toimage(depthimage).resize((xregione,yregione)).save(nomefile)
else:
	toimage(depthimage).filter(ImageFilter.MedianFilter(dimfiltro)).resize((xregione,yregione)).save(nomefile)
toimage(correlazioneimage).resize((xregione,yregione)).save(nomecorrelazione)
