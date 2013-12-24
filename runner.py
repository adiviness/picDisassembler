
import sys

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
    
def parseInstruction(line):
    instruction = line[9:-2]
    if instruction[-2:] == '0C':
        print('movlw', int(instruction[0:2], 16))


def main():
    if len(sys.argv) < 2:
        print("need a file")
        exit()
    filename = sys.argv[1]
    fp = open(filename, 'r')
    for line in fp:
        line = line.strip()
        lineType = getType(line)
        if lineType == data:
            parseInstruction(line)
    fp.close()






if __name__ == "__main__":
    main()

