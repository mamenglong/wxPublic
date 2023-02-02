import os.path
import sys


sys.path.append(os.path.dirname(os.path.dirname(__file__))+"/dd")
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(os.path.dirname(os.path.dirname(__file__)))
print("path:" + sys.path.__str__())

import tools.bingtools

if __name__ == '__main__':
    print("cs:" + tools.bingtools.getPicUrl())
