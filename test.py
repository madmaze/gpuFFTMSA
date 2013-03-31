#!/usr/bin/env python
import dataObj
import numpy as np

def calcCorrShift(H, G):
	f = np.fft.ifft(np.fft.fft(H) * np.conj(np.fft.fft(G)))	
	
	# find the max peak (should also identify other significant peaks)
	k=np.where(f==f.max())
	
	# Correlation, shift
	return (f.max(), k[0][0])


f = open("data/samplerna","r")
name=""
data=[]
done=False
l = f.readline()
while l and done==False:
	if l[0] == ">":
		# we have a name
		name=l[1:]
		if len(data)>0:
			# we already have data
			d = dataObj.dataObj(name, data)
			done=True
			
		data=[]
		
	else:
		data.extend(l.strip())
	l = f.readline()

k = 20 # shift
g = d.dataTrans
# shift g by k to get h
h = np.roll(d.dataTrans,k)

print calcCorrShift(h, g)
print len(h)
		

