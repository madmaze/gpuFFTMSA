gpuFFTMSA
=========

GPU accelerated FFT-based multiple sequence alinger.

Requirements:
-----
For the CPU portion of the code to work, only python, numpy, pylab(for debug) need to be installed.

For GPU portion, the above need to be available, as well as pyCUDA and pyFFT.CUDA


Usage:
-----
- if pyFFTalign.py is run without arguments it will gather default values out of ./data

```
usage: pyFFTalign.py [-h] [-i INPUT_GENOME] [-s INPUT_SEQS]
                     [--logFile LOGFILE] [-l LOGLEVEL] [-g] [-e] [--verify]

given a directory of input genomes and sequences it will try to match up each
sequence to its genome

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_GENOME, --inputgenome INPUT_GENOME
                        Input genome file or dir of fna files (Default:
                        ./data/sampleGenome.fna)
  -s INPUT_SEQS, --inputseqs INPUT_SEQS
                        Input sequence file (Default: ./data/sampleGenome.seq)
  --logFile LOGFILE     output to log file (Default: False)
  -l LOGLEVEL, --log LOGLEVEL
                        Log level, use DEBUG of more output (Default: INFO)
  -g, --usegpu          gpu option (Default: False)
  -e, --chopefficient   chop efficiently (Default: False)
  --verify              verify successfull transcription (Default: False)
```

Code layout:
-----
- pyFFTalign.py
  - Provides basic command-line parsing and provides a wrapper for the other two.
  - Reads in Genome(long sequence)
  - Reads in Sequences(shorter sequences)
- dataObj.py
  - Data container for raw and transcribed sequences
  - transcribes sequences on object creation
  - methods for returning padded raw and transcribed sequences
- aligner.py
  - CPU and GPU correlation functions

More information:
-----
- [pyFFTalign description and writeup](https://raw.github.com/madmaze/gpuFFTMSA/master/doc/pyFFTalignWriteup.pdf)
- [pyFFTalign presentation slides](https://raw.github.com/madmaze/gpuFFTMSA/master/doc/presentationSlides.pdf)