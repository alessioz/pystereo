#!/usr/bin/python
#-*- coding: utf-8 -*-

import Image
import ImageFilter
import sys
import numpy
import scipy.misc.pilutil as pilutil

class ShapeFromShading:
	
	def __init__(self, path_left_image="IMG_1376_1.JPG", path_right_image="IMG_1376_1.JPG",
		movingwin_xsize=20, movingwin_ysize=20, win_xsize=340, win_ysize=560,
		steprange = 100):
		
		self.path_left_image = path_left_image
		self.path_right_image = path_right_image
		self.movingwin_xsize = movingwin_xsize
		self.movingwin_ysize = movingwin_ysize
		self.win_xsize = win_xsize
		self.win_ysize = win_ysize
		self.steprange = steprange
		
		self.imL = Image.open(self.path_left_image)
		self.imR = Image.open(self.path_right_image)

		#metto in una stringa i valori dei pixel (da Image)
		#put pixel values in a string 
		self.imL_string = list(self.imL.getdata())
		self.imR_string = list(self.imR.getdata())

		#li ordino in una matrice con la dimensine dell'immagine (da numarray)
		#put them in a matrix with dimensions of image
		self.matrixL = numpy.reshape(self.imL_string, (self.imL.size[1], self.imL.size[0]))
		self.matrixR = numpy.reshape(self.imR_string, (self.imR.size[1], self.imR.size[0]))

		#a list where to put the depth data
		self.depth_list=[]
		
	def getDepthMap(self):
		
		#elaborazione riga per riga (in verticale)
		#elaborate each row whose size is defined by movingwin_ysize
		for riga in range(0, self.win_ysize, self.movingwin_ysize):
				
			#select a reference window
			for finestra in range(0, self.win_xsize, self.movingwin_xsize):
				indici =[]
				univoco =[]
				
				# compare the reference window with near pixels windows
				for step in range(self.steprange):
					somma = 0
					
					# qui sotto calcolo la matrice differenza per ogni step
					matricediff = self.matrixR[riga:riga+self.movingwin_ysize , finestra:finestra+self.movingwin_xsize] - \
					self.matrixL[riga:riga+self.movingwin_ysize , finestra+step:finestra+self.movingwin_xsize+step]
					
					matricediff2 = matricediff**2
					
					# sommo gli elementi della matrice differenza (DA VERIFICARE: li somma tutti o solo prima riga?)
					somma = matricediff2.sum()
					
					# normalizzo la somma e creo una lista con tutti gli indici della riga
					indice = somma/(self.win_ysize*self.win_ysize)
					indici.append(indice)
					
				# l'indice col valore piu basso e' quello che ha minore differenza fra le 2 img		
				distanzapixel = indici.index(min(indici))
				

				# ne annoto la posizione (sequenziale per step)
				self.depth_list.append(distanzapixel)
	

		ydimensione = self.win_ysize/self.movingwin_ysize
		xdimensione = self.win_xsize/self.movingwin_xsize
		
		self.depth_map = numpy.reshape(self.depth_list, (ydimensione, xdimensione))
		
	def saveDepthMap(self, nomefile):
		pilutil.toimage(self.depth_map).filter(ImageFilter.MedianFilter(5)).resize((self.win_xsize, self.win_ysize)).save(nomefile)


#example
test = ShapeFromShading('IMG_1376_1.JPG','IMG_1377_1.JPG', 20, 20, 340, 560, 100)
test.getDepthMap()
test.saveDepthMap('depthmap.jpg')




#dimfiltro = 5
#oggetto = "luna"
#nomefile ="%s_vers%s_xwin%s_ywin%s_step%s_MedianFilter%s.jpg" % (oggetto,versione, xfinestra, yfinestra, steprange, dimfiltro)

#from scipy.misc.pilutil import *

#def salvaimmagine(depthimage):
	#oggetto = "luna"
	#dimfiltro = 5
	#nomefile ="%s_vers%s_xwin%s_ywin%s_step%s_MedianFilter%s.jpg" % (oggetto,versione, xfinestra, yfinestra, steprange, dimfiltro)

	#if dimfiltro == 0:
		#nomefile ="%s_vers%s_xwin%s_ywin%s_step%s_NoFilter_threshold%s.jpg" % (oggetto,versione, xfinestra, yfinestra, steprange, sogliacorr)
		#toimage(depthimage).resize((xregione,yregione)).save(nomefile)
	#else:
		#toimage(depthimage).filter(ImageFilter.MedianFilter(dimfiltro)).save(nomefile)
#salvaimmagine(depthimage)
#salvaimmagine(depthimagemasked)
#nomecorrelazione = "correlazione_"+nomefile
#toimage(correlazioneimage).resize((xregione,yregione)).save(nomecorrelazione)

#depthimage =array(depthimage, dtype=Float32)

#from scipy.signal.signaltools import *
#depthmed = medfilt2d(depthimage, kernel_size = 5)

#namefile = raw_input('insert file name (with extension): ')
#scrivi =  open(namefile,"w")
#scrivi.write("north: 0\n")
#scrivi.write("south:"+str(-yregione)+"\n")
#scrivi.write("east: 0\n")
#scrivi.write("west:"+str(-xregione)+"\n")
#scrivi.write("rows:"+str(yregione/yfinestra)+"\n")
#scrivi.write("cols:"+str(xregione/xfinestra)+"\n")
#for i in depthmed:
	#for a in i:
		#scrivi.write(str(int(a))+" ")
