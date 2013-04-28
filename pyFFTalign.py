#!/usr/bin/env python

# sys libs
import argparse
import os
import logging as log
import glob
import numpy as np

import dataObj as do
import aligner

def readGenome(fname, verify=True):
	flist=[]
	if not os.path.exists(fname):
		print "ERROR: genome input file not found", fname
		exit()
		
	if os.path.isdir(fname):
		# glob all .fna files
		flist = glob.glob(fname+"/*.fna")
	else:
		flist.append(fname)
	
	G=[]
	# read in every genome file
	for f in flist:
		fin = open(f, "r")
		header=fin.readline()
		data=[]
		for l in fin.readlines():
			data.extend(l.strip())
		
		tmp = do.dataObj(header, list(data))
		if verify and tmp.verifyTranscription() == False:
			# perhaps we should fail here
			log.warning(tmp.name + " failed transcription.")
		G.append(tmp)
		
	return G
	
def readSequences(fname):
	if not os.path.exists(fname):
		print "ERROR: genome input file not found", fname
		exit()
		
	f = open(fname, "r")
	seqs=[]
	for l in f.readlines():
		if l.strip() != "":
			name,data = l.strip().split("|")
			seqs.append(do.dataObj(name, list(data)))
	return seqs
	

def main(args):
	# read input
	log.info("reading input files..")
	H_array = readGenome(args.input_genome, args.verify)
	G_array = readSequences(args.input_seqs)
	
	log.info("read " + str(len(H_array)) + " genome sequences.")
	log.info("read " + str(len(G_array)) + " search sequences.")
		
	#transform
	res = aligner.calcCorrShiftmn(H_array, G_array, args.gpuflag)
	
	#print res

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="given a directory of input genomes and sequences it will try to match up each sequence to its genome")
	parser.add_argument("-i","--inputgenome",dest="input_genome", default="./data/sampleGenome.fna", help="Input genome file or dir of fna files")
	parser.add_argument("-s","--inputseqs",dest="input_seqs", default="./data/sampleGenome.seq", help="Input sequence file")
	parser.add_argument("-l","--log",dest="logLevel", default="INFO", help="Log level (default: INFO)")
	parser.add_argument("-g","--usegpu",dest="gpuflag", action="store_true", help="gpu option")
	parser.add_argument("--verify",dest="verify", action="store_true", help="verify successfull transcription")
	args = parser.parse_args()
	
	verbosity = getattr(log, args.logLevel.upper(), None)
	if verbosity is None:
	    print "Invalid logLevel:", loglevel
	    exit()
	
	# setup logger
	log.basicConfig(level=verbosity, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
	try:
		import pycuda
		from pyfft.cuda import Plan
	except ImportError:
		cuda_enabled = False
		log.warning("No pyCUDA or pyFFT found, disableing GPU support.")
		
	main(args)
