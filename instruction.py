
from binascii import *


ADDWF_MASK =  0b000111000000
ANDWF_MASK =  0b000101000000
CLRW_MASK =   0b000001000000
MOVWF_MASK =  0b000000100000
######
MOVELW_MASK = 0b110000000000

#####
D_MASK = 0b000000100000
F_MASK = 0b000000011111

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
            # TODO should implement this (if python wasn't dumb about bits)
            # ! ( x xor (x - 1))
            if instr & 0b111111000000 == ADDWF_MASK:
                register = instr & F_MASK
                destination = self._maskDestination(instr)
                instruction.append("ADDWF")
                instruction.append(str(register))
                instruction.append(str(destination))
            elif instr & 0b111111000000 == ANDWF_MASK:
                register = instr & F_MASK
                destination = self._maskDestination(instr)
                instruction.append("ANDWF")
                instruction.append(str(register))
                instruction.append(str(destination))
            elif instr & 0b111111000000 == CLRW_MASK:
                instruction.append("CLRW")
            elif instr & 0b111111100000 == MOVWF_MASK:
                register = instr ^ MOVWF_MASK
                instruction.append("MOVWF")
                instruction.append(str(register))
            elif instr & 0b110000000000 == MOVELW_MASK:
                instruction.append("MOVLW")
                instruction.append(str(byteArray[2:4])[2:4])
            instructionStack.append(instruction)
            byteArray = byteArray[4:]
        return instructionStack[::-1]

    def _makeMask(bits):
        NotImplemented

    def _maskDestination(self, instr):
        destination = instr & D_MASK
        if destination != 0:
            destination = 1
        return destination

                

            

    def disassemble(self):
        for i in self.instructions:
            if len(i) <= 2:
                print(' '.join(i))
            else:
                print(i[0], ', '.join(i[1:]))
            


