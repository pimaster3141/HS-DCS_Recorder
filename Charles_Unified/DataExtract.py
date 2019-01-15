import sys
sys.path.insert(0, 'PythonLib');

import FlowFit
import G2Calc
import multiprocessing as mp

BYTES_PER_SAMPLE = 2;

def extract(filename, legacy=False, fs=2.5E6, intg=0.05, fsout=200, numProcessors=12):
	fsize = os.stat(filename).st_size;
	windowSize = int(fs*intg);
	windowShift = int(fs/fsout);
	numSamples = math.floor(((fsize/BYTES_PER_SAMPLE)-windowSize)/windowShift)+1;

	startIndexes = np.arange(numSamples, dtype='uint8')*windowShift;

	pool = mp.Pool(processes=numProcessors);

def seekExtract(startIndex, windowSize, fs, levels, legacy, filename):
	f = open(filename, 'rb');
	f.seek(startIndex*BYTES_PER_SAMPLE, os.SEEK_SET);
	data = np.fromfile(f, count=windowSize, dtype='uint16');

	g2Data = G2Calc.mtAuto(data, fs, levels);