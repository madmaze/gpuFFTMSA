#!/usr/bin/env python

import dataObj as do
import numpy as np
import pylab
import math
import logging as log

# check if cuda is available
try:
	from pyfft.cuda import Plan
	import pycuda.gpuarray as gpuarray
	import pycuda.autoinit
	dev=pycuda.autoinit.device
except ImportError:
	cuda_enabled = False


def genCompareStr(h,g):
	# returns a sting of the alignments
	compStr=""
	for x,y in zip(h,g):
		if x==y:
			compStr+="|"
		else:
			compStr+="-"
	return compStr

def calcCorrShiftmn(H, G, prctMatch=75,GPUmode=False, plot=False):
	res=[]
	if not GPUmode:
		log.info("Starting CPU based alignment...")
		
		if type(H) != type([]):
				H=[H]
		
		for H_t in H: 
			# H is long and G is short
			log.debug("Starting H_ fft...")
			
			# already zero padded from reading in
			H_ = np.fft.fft(H_t.dataTrans)
			
			# check if we have many G
			if type(G) != type([]):
				G=[G]
				
			for G_t in G:
				# pad G with zeros to size of H
				log.debug("Starting G_ fft...")
				G_ = np.fft.fft(G_t.getTransPadded(len(H_t.dataTrans)))
				
				log.debug("Starting cross-correlation and ifft...")
				f = np.fft.ifft(H_ * np.conj(G_))
				
				k=np.where(f==f.max())
				# debug plotting
				if plot:
					pylab.plot(f[0:2500].real)
					pylab.show()
				log.info(H_t.name + "vs " + G_t.name+" => shift: "+str(k[0][0])+" corr: "+str(f.max().real))
				
				res.append({"H":H_t,"G":G_t, "shift":k[0][0], "corr":f.max()})
	else:
		log.info("Starting GPU based alignment...")
		res = calcCorrShiftGPU(H,G)
		log.info("done GPU based alignment...")
		
	return res
	
def calcCorrShiftGPU(H, G):
	log.info("Using: "+dev.name())
	res=[]
	# make sure we get arrays of items
	if type(G) != type([]):
		G=[G]
	if type(H) != type([]):
		H=[H]
	for H_t in H:
		# Setup plan has to be power of 2
		fftPlan = Plan(len(H_t.dataTrans), wait_for_finish=True)
		
		# H is long and G is short
		log.debug("Starting H_ fft on GPU...")
		
		# push to GPU
		H_gpu = gpuarray.to_gpu(H_t.dataTrans)
		
		# do forwards FFT in place
		fftPlan.execute(H_gpu)
		
		for G_t in G:
			# pad G with zeros to size of H
			log.debug("Starting G_ fft on GPU...")
			G_gpu = gpuarray.to_gpu(G_t.getTransPadded(len(H_t.dataTrans)))
			
			# do forwards FFT in place
			fftPlan.execute(G_gpu)
			
			F_gpu = H_gpu * G_gpu.conj()
			
			fftPlan.execute(F_gpu, inverse=True)
			
			f_host = F_gpu.get()
			
			maxVal = f_host.max()
			k=np.where(f_host==maxVal)
			
			res.append({"H":H_t, "G":G_t, "shift":k[0][0], "corr":maxVal.real})
			#maxVal = gpuarray.max(F_gpu.real)
			#print maxVal
	return res

