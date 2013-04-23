#!/usr/bin/env python
import dataObj
import numpy as np
import pylab

def calcCorrShift(H, G):
	f = np.fft.ifft(np.fft.fft(H) * np.conj(np.fft.fft(G)))	
	pylab.plot(f.real)
	pylab.show()
	# find the max peak (should also identify other significant peaks)
	k=np.where(f==f.max())
	
	# Correlation, shift
	return (f.max(), k[0][0])
def genCompareStr(h,g):
	compStr=""
	for x,y in zip(h,g):
		if x==y:
			compStr+="|"
		else:
			compStr+="-"
	return compStr
def calcCorrShift2(H, G, h, g):
	f = np.fft.ifft(np.fft.fft(H) * np.conj(np.fft.fft(G)))
	#print np.mean(f), np.min(f), np.max(f), np.std(f)
	std2=2*np.std(f)
	
	#pylab.plot(f.real)
	#pylab.show()
	# find the max peak (should also identify other significant peaks)
	#k=np.where(f==f.max())
	aligns=np.where(f>std2)
	print aligns
	fout=open("res.txt","w")
	
	for k in aligns[0]:
		print k, f[k].real
		lineA="".join(h)
		lineB="".join(np.roll(g,k))
		'''lineMid=""
		for i in range(len(h)):
			if i>k:
				lineA+=h[i-k]
				lineMid+=" "
			else:
				lineA+=h[k-i]
				lineMid+=" "
			if i==(k-1):
				lineMid+="|"
			lineB+=g[i]
		'''
		lineShift=[" "]*len(lineA)
		print len(lineShift), type(lineShift)
		lineShift[k]='!'
		fout.write("".join(lineShift)+"\n")
		fout.write(lineA+"\n")
		fout.write(genCompareStr(lineA,lineB)+"\n")
		fout.write(lineB+"\n")
		fout.write("".join(lineShift)+"\n===\n\n")
		#print lineA[:150]
		#print lineB[:150]
		
			
	# Correlation, shift
	return (f,None)


f = open("data/samplerna2","r")
name=""
data=[]
done=False
l = f.readline()
while l and done==False:
	l=l.strip()
	if len(l) > 0 and l[0] == ">":
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

print "\ninput:", d.name
print "length:", len(d.dataTrans)
#corr,shift = calcCorrShift2(h, g, np.roll(d.dataRaw,k), d.dataRaw)
corr,shift = calcCorrShift2(g, h, d.dataRaw, np.roll(d.dataRaw,k))
#print "test shift by 20 nucleotides\n\n\nresults:"
#print "\tbest shift:", shift
#print "\tcorrelation:", corr.real
