#!/usr/bin/env python
import dataObj as do
import random
import pyFFTalign

def generateTestSeqs(H_array, n_seq, len_seq):
	
	testSeqs=[]
	
	for H in H_array:
		for n in range(n_seq):
			r = random.randint(1,len(H.dataRaw)-len_seq)
			testSeqs.append([str(len_seq),str(r),H.fname,H.dataRaw[r:r+len_seq]])
	
	fname="./data/n_"+str(n_seq)+".l_"+str(len_seq)+".seq"
	f=open(fname,"w")
	for r in testSeqs:
		#print ",".join(r[0:3])+"|"+"".join(r[3])+"\n"
		f.write(",".join(r[0:2])+"|"+"".join(r[3])+"\n")


if __name__ == "__main__":
	n_seq=1000
	len_seq=64
	H_array = pyFFTalign.readGenome("./data/sampleGenome.fna", False)
	while len_seq <= 524288:
		res = generateTestSeqs(H_array,n_seq,len_seq)
		len_seq=len_seq*2
	
