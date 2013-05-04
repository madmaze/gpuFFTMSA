#!/usr/bin/env python

# sys libs
import argparse
import os
import logging as log
import glob
import numpy as np
import time
import math

import dataObj as do
import aligner

def readGenome(fname, verify=True, chopEfficiently=False):
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
		
		if chopEfficiently:
			n=int(2**math.floor(math.log(len(data),2)))
			
			tmp1 = do.dataObj(name=header,fname=f+"_part1", dataRaw=list(data[:n]))
			tmp2 = do.dataObj(name=header,fname=f+"_part2", dataRaw=list(data[n:]))
			G.append(tmp1)
			G.append(tmp2)
		else:
			tmp = do.dataObj(name=header,fname=f, dataRaw=list(data))
			
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
	# read every line of input file
	for l in f.readlines():
		if l.strip() != "":
			name,data = l.strip().split("|")
			seqs.append(do.dataObj(name=name, fname=fname, dataRaw=list(data)))
	return seqs
	

def main(args):
	# read input
	log.info("reading input files..")
	H_array = readGenome(args.input_genome, args.verify, chopEfficiently=args.chopefficient)
	G_array = readSequences(args.input_seqs)
	
	log.info("read " + str(len(H_array)) + " genome sequences.")
	log.info("read " + str(len(G_array)) + " search sequences.")
		
	#transform
	stime=time.clock()
	res = aligner.calcCorrShiftmn(H_array, G_array, GPUmode=args.gpuflag)
	etime=time.clock()

	for r in res:
		print r["H"].name, r["G"].name
	
	log.info("Time to alignment: "+str(etime-stime)+"s")

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="given a directory of input genomes and sequences it will try to match up each sequence to its genome")
	parser.add_argument("-i","--inputgenome",dest="input_genome", default="./data/sampleGenome.fna", help="Input genome file or dir of fna files (Default: ./data/sampleGenome.fna)")
	parser.add_argument("-s","--inputseqs",dest="input_seqs", default="./data/sampleGenome.seq", help="Input sequence file (Default: ./data/sampleGenome.seq)")
	parser.add_argument("--logFile",dest="logFile", default="", help="output to log file (Default: False)")
	parser.add_argument("-l","--log",dest="logLevel", default="INFO", help="Log level, use DEBUG of more output (Default: INFO)")
	parser.add_argument("-g","--usegpu",dest="gpuflag", action="store_true", help="gpu option (Default: False)")
	parser.add_argument("-e","--chopefficient",dest="chopefficient", action="store_true", help="chop efficiently (Default: False)")
	parser.add_argument("--verify",dest="verify", action="store_true", help="verify successfull transcription (Default: False)")
	args = parser.parse_args()
	
	verbosity = getattr(log, args.logLevel.upper(), None)
	if verbosity is None:
	    print "Invalid logLevel:", loglevel
	    exit()
	
	# setup logger
	if args.logFile != "":
		print "logging to", args.logFile
		log.basicConfig(level=verbosity, filename=args.logFile, filemode='w', format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
	else:
		log.basicConfig(level=verbosity, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
	
	# check if cuda is available
	try:
		import pycuda
		from pyfft.cuda import Plan
	except ImportError:
		cuda_enabled = False
		log.warning("No pyCUDA or pyFFT found, disableing GPU support.")
		
	main(args)
