import os
import sys

FILE_DIR_ABS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, FILE_DIR_ABS)
from util.Util import to_safe_filename
del sys.path[0]

def safeFilename(file, state, args):
    return to_safe_filename(args[0])
