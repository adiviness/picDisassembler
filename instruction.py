
from binascii import *


MOVELW_MASK = 0b110000000000

class Instruction():


    def __init__(self, line):
        line = line[1:]
        self.dataByteCount = int(line[0:2], 16)
        self.address = int(line[2:6], 16)
        self.instrType = int(line[6:8], 16)
        self.instructions = self.parse(line[8:-2])
        self.checksum = int(line[-2:], 16)

    def isData(self):
        return self.instrType == 0

    def parse(self, text):
        instructionStack = []
        byteArray = hexlify(unhexlify(text)[::-1])
        while len(byteArray) != 0:
            instruction = []
            instr = int(byteArray[0:4], 16)
            if instr & MOVELW_MASK == MOVELW_MASK:
                instruction.append("MOVELW")
                instruction.append(str(byteArray[2:4])[2:4])
            instructionStack.append(instruction)
            byteArray = byteArray[4:]
        return instructionStack
                

            

    def disassemble(self):
        for i in self.instructions:
            print(' '.join(i))
            


