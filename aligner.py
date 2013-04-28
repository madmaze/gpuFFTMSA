#!/usr/bin/env python

import dataObj as do
import numpy as np
import pylab
import math
import logging as log

try:
	from pyfft.cuda import Plan
	#from pycuda.tools import make_default_context
	import pycuda.gpuarray as gpuarray
	#import pycuda.driver as cuda
	import pycuda.autoinit
except ImportError:
	cuda_enabled = False


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
		
		if type(H) != type([]):
				H=[H]
		
		for H_t in H: 
			# H is long and G is short
			log.debug("Starting H_ fft...")
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
				res.append({"shift":k[0][0],"corr":f.max()})
	else:
		log.info("Starting GPU based alignment...")
		res = calcCorrShiftGPU(H,G)
		
	return res
	
def calcCorrShiftGPU(H, G):
	#print "not yet implemented"
	#cuda.init()
	#context = make_default_context()
	#stream = cuda.Stream()
	
	H_gpu = gpuarray.to_gpu(H[0].dataTrans)
	
	# plan has to be power of 2
	fftPlan = Plan(len(H[0].dataTrans))
	
	log.debug("Starting H_ fft on GPU...")
	fftPlan.execute(H_gpu)
	res = H_gpu.get()
	log.debug("done and returned H_ fft on GPU...")
	#Context.pop()
	exit()
