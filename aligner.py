#!/usr/bin/env python

import dataObj as do
import numpy as np
import pylab
import logging as log

def genCompareStr(h,g):
	compStr=""
	for x,y in zip(h,g):
		if x==y:
			compStr+="|"
		else:
			compStr+="-"
	return compStr

def calcCorrShiftmn(H, G, GPUmode=False, plot=False):
	res=[]
	if not GPUmode:
		log.info("Starting CPU based alignment...")
		
		# H is long and G is short
		H_ = np.fft.fft(H.dataTrans)
		
		# check if we have many G
		if type(G) != type([]):
			G=[G]
			
		for G_t in G:
			# pad G with zeros to size of H
			G_ = np.fft.fft(G_t.getTransPadded(len(H.dataTrans)))
			
			f = np.fft.ifft(H_ * np.conj(G_))
			
			k=np.where(f==f.max())
			# debug plotting
			if plot:
				pylab.plot(f[0:2500].real)
				pylab.show()
			log.info(G_t.name+" => shift: "+str(k[0][0])+" corr: "+str(f.max().real))
			res.append({"shift":k[0][0],"corr":f.max()})
	else:
		log.info("Starting GPU based alignment...")
		res = calcCorrShiftGPU(H,G)
		
	return res
	
def calcCorrShiftGPU(H, G):
	print "not yet implemented"
	exit()
