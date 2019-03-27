import glob
import os

def list_all_files(path):
	print(os.path.join(path, '**'))
	for filename in glob.iglob(os.path.join(path, '**'),  recursive=True):
		yield filename
