gpuFFTMSA
=========

GPU accelerated FFT-based multiple sequence alinger


Usage:
-----
```
usage: pyFFTalign.py [-h] [-i INPUT_GENOME] [-s INPUT_SEQS]
                     [--logFile LOGFILE] [-l LOGLEVEL] [-g] [-e] [--verify]

given a directory of input genomes and sequences it will try to match up each
sequence to its genome

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_GENOME, --inputgenome INPUT_GENOME
                        Input genome file or dir of fna files
  -s INPUT_SEQS, --inputseqs INPUT_SEQS
                        Input sequence file
  --logFile LOGFILE     output to log file
  -l LOGLEVEL, --log LOGLEVEL
                        Log level (default: INFO)
  -g, --usegpu          gpu option
  -e, --chopefficient   chop efficiently
  --verify              verify successfull transcription
```

More information:
----
- [pyFFTalign description and writeup]()