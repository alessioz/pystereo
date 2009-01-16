#!/usr/bin/python
import Image
import ImageFilter
import sys
import time
import datetime
from pylab import *
from numpy import *

versione = 0.2

imsx = Image.open("lunaleft.jpg")
imdx = Image.open("lunaright.jpg")


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
xfinestra = 50
yfinestra = 50

#dimensioni dell'area su cui si effettua l'elaborazione
xregione = 2300
yregione = 2400

sogliacorr = 0.2

steprange= 75
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
		distanzapixel = indici.index(min(indici))
		
		univoco = indici
		univoco2 = array(indici)
		derivata = diff(univoco2)
		#print derivata
		posizioneminimo =[]
		posizione=0
		segnoprec = -1
		for segno in derivata:
			if segnoprec <=0 and segno>=0:
				posizioneminimo.append(posizione)
			else:
				pass
			segnoprec = segno
			posizione+=1
		univoco3 = univoco2[posizioneminimo].tolist()
		listaminimi = univoco3
		if univoco3 != []:
			minimoassoluto = float(min(univoco3))+0.1
			minimoassolutopulito = min(univoco3)
			univoco3.remove(min(univoco3))
		else:
			minimoassoluto = float(max(indici))
			minimoassolutopulito = max(indici)
		
		if univoco3 != []:
			minimorelativo = float(min(univoco3))+0.1
			minimorelativopulito = min(univoco3)
		else:
			minimorelativo = float(max(indici))
			minimorelativopulito = max(indici)
		#print indici
		#print "minimoassolutopulito: ",minimoassolutopulito
		#print "minimorelativopulito ", minimorelativopulito, minimorelativo
		
		if indici.index(min(indici))==0:
			distanzapixel = indici.index(minimorelativopulito)
			
		if abs(indici.index(minimorelativopulito) - indici.index(minimoassolutopulito)) < 6 and abs(minimorelativopulito-minimoassolutopulito) < 3:
			rapportominimi = 5
		else:			
			rapportominimi = minimorelativo/minimoassoluto
		#print minimorelativo, minimoassoluto, rapportominimi
		
		
		
		
		if rapportominimi > sogliacorr and indici.index(min(indici)) < len(derivata):
			continuita = (derivata[indici.index(min(indici))])/min(indici)
			if continuita < 2:
				numerodati += 1
				correlazione.append(1)
				validita = "valid"
				
			else:
				correlazione.append(0)
				validita = "invalid"
			#print indici
		
		else:
			correlazione.append(0)
			validita="invalid"
			#depth.append(0)
			#depth.append("None")
			numeronull +=1
			
		#print indici.index(min(indici))
		#if distanzapixel==0:
			#plot(arange(len(indici)),indici,'k',[indici.index(min(indici))], [min(indici)], 'ro', [indici.index(minimorelativopulito)], [minimorelativo], 'go',)
		
			#title(validita)
			##show()
			##time.sleep(3)
			#nomegrafico = "riga%s_finestra%s.png" % (riga,finestra)
			#savefig(nomegrafico)
			#close()
			
		depth.append(distanzapixel)  # l'indice col valore piu basso e' quello che ha minore differenza fra le 2 img, ne annoto la posizione (sequenziale per step)
		
	stimato = (time.clock()-inizio)/(riga+yfinestra)*(yregione)+inizio
	print riga, datetime.timedelta(seconds = stimato), datetime.timedelta( seconds = (stimato -time.clock()))
print numerodati, numeronull
#print depth
#print len(depth)
ydimensione = yregione/yfinestra
xdimensione = xregione/xfinestra


print len(correlazione)
print ydimensione*xdimensione
correlazioneimage = reshape(correlazione, (ydimensione, xdimensione))
print correlazioneimage
depthimage = reshape(depth, (ydimensione, xdimensione))
print depthimage
depthimagemasked = correlazioneimage*depthimage
#from scipy.interpolate.interpolate import interp2d
#print interp2d(390,500,depthimage)

#if correlazioneimage > 1000:
	#correlazioneimage = 0
#print correlazioneimage

#vedi masked e spline_filter
dimfiltro = 5
oggetto = "luna"
nomefile ="%s_vers%s_xwin%s_ywin%s_step%s_MedianFilter%s.jpg" % (oggetto,versione, xfinestra, yfinestra, steprange, dimfiltro)

from scipy.misc.pilutil import *

def salvaimmagine(depthimage):
	oggetto = "luna"
	dimfiltro = 5
	nomefile ="%s_vers%s_xwin%s_ywin%s_step%s_MedianFilter%s.jpg" % (oggetto,versione, xfinestra, yfinestra, steprange, dimfiltro)

	if dimfiltro == 0:
		nomefile ="%s_vers%s_xwin%s_ywin%s_step%s_NoFilter_threshold%s.jpg" % (oggetto,versione, xfinestra, yfinestra, steprange, sogliacorr)
		toimage(depthimage).resize((xregione,yregione)).save(nomefile)
	else:
		toimage(depthimage).filter(ImageFilter.MedianFilter(dimfiltro)).save(nomefile)
salvaimmagine(depthimage)
#salvaimmagine(depthimagemasked)
nomecorrelazione = "correlazione_"+nomefile
toimage(correlazioneimage).resize((xregione,yregione)).save(nomecorrelazione)

depthimage =array(depthimage, dtype=Float32)

from scipy.signal.signaltools import *
depthmed = medfilt2d(depthimage, kernel_size = 5)

namefile = raw_input('insert file name (with extension): ')
scrivi =  open(namefile,"w")
scrivi.write("north: 0\n")
scrivi.write("south:"+str(-yregione)+"\n")
scrivi.write("east: 0\n")
scrivi.write("west:"+str(-xregione)+"\n")
scrivi.write("rows:"+str(yregione/yfinestra)+"\n")
scrivi.write("cols:"+str(xregione/xfinestra)+"\n")
for i in depthmed:
	for a in i:
		scrivi.write(str(int(a))+" ")
