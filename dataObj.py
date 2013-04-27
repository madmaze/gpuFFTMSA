#!/usr/bin/env python
import numpy as np
import logging as log

class dataObj:
	dataTrans=np.array([])
	
	def __init__(self, name = None, dataRaw = []):
		self.name = name.strip()
		self.dataRaw = dataRaw
		log.debug("starting transcription of " + self.name)
		self.dataTrans = np.array(self.transcribe(self.dataRaw))
		log.debug("done transcription of " + self.name)
	
	def __len__(self):
		return len(self.dataRaw)
	
	def _transcribe(inst,i):
		i=i.lower()
		if i == "a":
			return np.complex(1)
		elif i == "u" or i == "t":
			return np.complex(-1)
		elif i == "c":
			return np.complex(1j)
		elif i == "g":
			return np.complex(-1j)
		else:
			print "ERROR: transcoding."
			print type(i),i
			exit()
		return 0
		
	def getTransPadded(self, padLen):
		padded=np.zeros(padLen,dtype=np.complex)
		padded[0:len(self.dataRaw)]=self.dataTrans
		return padded[:]
	
	def getRawPadded(self, padLen):
		padded=["-"]*padLen
		padded[0:len(self.dataRaw)]=self.dataRaw
		return padded[:]
		
	def transcribe(self, raw):
		v = np.vectorize(self._transcribe)
		tmp = v(raw)
		return tmp 
		
	def __repr__(self):
		s=self.name+"\n"
		return s
