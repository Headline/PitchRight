import sys
from multiprocessing import freeze_support

from spleeter.separator import Separator

if __name__ == '__main__':
    freeze_support()

    separator = Separator("stemsconfig.json")
    separator.separate_to_file(sys.argv[1], 'songs', filename_format=sys.argv[2]+'/{instrument}.{codec}')
