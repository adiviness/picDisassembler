
import sys
from instruction import *

data = 1
eof = 2
extendedAddress = 3
other = 4




def getType(line):
    string = line[7:9]
    if string == '00':
        return data
    elif string == '01':
        return eof
    elif string == '04':
        return extendedAddress
    else:
        return other
    


def main():
    if len(sys.argv) < 2:
        print("need a file")
        exit()
    filename = sys.argv[1]
    fp = open(filename, 'r')
    for line in fp:
        line = line.strip()
        instruction = Instruction(line)
        if instruction.isData():
            instruction.disassemble()
            i = 1
    fp.close()






if __name__ == "__main__":
    main()

