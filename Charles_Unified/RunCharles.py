import sys
sys.path.insert(0, 'PythonLib');
import CharlesSystem
import code

charles = None

def start(filename, version=None, sampleClk=None, averages=[[0,3]]):
	global charles;
	charles = CharlesSystem.CharlesSystem(filename, version, sampleClk, averages);
	charles.start();

def stop():
	global charles;
	if(not charles == None):
		charles.stop();
	charles = None;


print("Starting Up...");
code.interact(local = locals());
