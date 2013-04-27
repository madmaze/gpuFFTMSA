#!/usr/bin/env python

# sys libs
import argparse
import os
import logging as log

import dataObj as do
import aligner



def readGenome(fname):
	if not os.path.exists(fname):
		print "ERROR: genome input file not found", fname
		exit()
		
	f = open(fname, "r")
	header=f.readline()
	data=[]
	for l in f.readlines():
		data.extend(l.strip())
		
	return do.dataObj(header, list(data))
	
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
	H = readGenome(args.input_genome)
	G_array = readSequences(args.input_seqs)
	
	log.info("read " + str(len(H_array)) + " genome sequences.")
	log.info("read " + str(len(G_array)) + " search sequences.")
		
	#transform
	res = aligner.calcCorrShiftmn(H,G_array,args.gpuflag)
	
	#print res

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description="given a directory of input genomes and sequences it will try to match up each sequence to its genome")
	parser.add_argument("-i","--inputgenome",dest="input_genome", default="./data/sampleGenome.fna", help="Input genome file")
	parser.add_argument("-s","--inputseqs",dest="input_seqs", default="./data/sampleGenome.seq", help="Input sequence file")
	parser.add_argument("-l","--log",dest="logLevel", default="INFO", help="Log level (default: INFO)")
	parser.add_argument("-g","--usegpu",dest="gpuflag", action="store_true", help="gpu option")
	args = parser.parse_args()
	
	verbosity = getattr(log, args.logLevel.upper(), None)
	if verbosity is None:
	    print "Invalid logLevel:", loglevel
	    exit()
	
	# setup logger
	log.basicConfig(level=verbosity, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
	
	main(args)
