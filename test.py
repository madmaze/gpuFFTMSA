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

def calcCorrShiftmn(H,G):
	# H is long and G is short
	H_ = np.fft.fft(H.dataTrans)
	
	#padded=np.zeros_like(H.dataTrans)
	#padded[0:len(G.dataTrans)]=G.dataTrans
	
	# pad G with zeros to size of H
	G_ = np.fft.fft(G.getTransPadded(len(H.dataTrans)))
	f = np.fft.ifft(H_ * np.conj(G_))
	
	k=np.where(f==f.max())
	return (f.max(), k[0][0])
	
def calcCorrShiftmn_efficient(H,G,m,n):
	# H is long and G is short
	H_ = np.fft.fft(H.dataTrans)
	
	#padded=np.zeros_like(H.dataTrans)
	#padded[0:len(G.dataTrans)]=G.dataTrans
	
	# pad G with zeros to size of H
	G_ = np.fft.fft(G.getTransPadded(len(H.dataTrans)))
	G__ = np.fft.fft(G.dataTrans)
	print np.fft.fft(G.getTransPadded(len(H.dataTrans)))
	print n, len(G_), len(G__)
	
	f_ = np.zeros_like(H_)
	#f_ = H_.copy()
	for i in range(n):
		f_[i] = H_[i] * np.conj(G__[i])
	
	f = np.fft.ifft(f_)
	
	#pylab.plot(f_.real)
	#pylab.plot(H_.real)
	#pylab.show()
	k=np.where(f==f.max())
	return (f.max(), k[0][0])

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
h = d.dataTrans
# shift g by k to get h
#g = np.roll(d.dataTrans,k)

#g = dataObj.dataObj("test", list("cugcggaaccggugaguacaccggaa"))
g = dataObj.dataObj("test", list("ccauggcguuaguau"))
print "\ninput:", d.name
print "length H:", len(d.dataTrans)
print "length G:", len(g.dataTrans)

#corr,shift = calcCorrShiftmn(d, g)

corr,shift = calcCorrShiftmn_efficient(d, g, len(d),len(g))

print "shift:",shift
print "corr:",corr.real

shifted = np.roll(g.getRawPadded(len(d)),shift)
comp = genCompareStr(d.dataRaw, shifted)

fout=open("res.txt","w")
fout.write("".join(d.dataRaw)+"\n")
fout.write(comp+"\n")
fout.write("".join(shifted)+"\n")
fout.close()


#corr,shift = calcCorrShift2(h, g, np.roll(d.dataRaw,k), d.dataRaw)
#corr,shift = calcCorrShift2(g, h, d.dataRaw, np.roll(d.dataRaw,k))
#print "test shift by 20 nucleotides\n\n\nresults:"
#print "\tbest shift:", shift
#print "\tcorrelation:", corr.real
