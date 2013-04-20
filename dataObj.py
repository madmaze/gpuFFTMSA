#!/usr/bin/env python
import numpy as np

class dataObj:
	dataTrans=np.array([])
	
	def __init__(self, name=None, dataRaw=[]):
		self.name=name
		self.dataRaw=dataRaw
		self.dataTrans=np.array(self.transcribe(self.dataRaw))
	
	def _transcribe(inst,i):
		i=i.lower()
		if i == "a":
			return 1
		elif i == "u":
			return -1
		elif i == "c":
			return 1j
		elif i == "g":
			return -1j
		return 0
	
	def transcribe(self, raw):
		v = np.vectorize(self._transcribe)
		return v(raw)
		
	def __repr__(self):
		s=self.name+"\n"
		return s
