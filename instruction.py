
from binascii import *


ADDWF_MASK =  0b000111000000
ANDWF_MASK =  0b000101000000
CLRF_MASK =   0b000001100000
CLRW_MASK =   0b000001000000
COMF_MASK =   0b001001000000
DECF_MASK =   0b000011000000
DECFSZ_MASK = 0b001011000000
INCF_MASK =   0b001010000000
INCFSZ_MASK = 0
IORWF_MASK = 0
MOVF_MASK = 0
MOVWF_MASK =  0b000000100000
NOP_MASK = 0
RLF_MASK = 0
RRF_MASK = 0
SUBWF_MASK = 0
SWAPF_MASK = 0
XORWF_MASK = 0
###### Bit oriented file register operations
BCF_MASK = 0
BSF_MASK = 0
BTFSC_MASK = 0
BTFSS_MASK = 0
###### Literal and control operations
ANDLW_MASK = 0
CALL_MASK = 0
CLRWDT_MASK = 0
GOTO_MASK = 0
IORLW_MASK = 0
MOVELW_MASK = 0b110000000000
OPTION_MASK = 0
RETLW_MASK = 0
SLEEP_MASK = 0
TRIS_MASK = 0
XORLW_MASK = 0
##### Helper masks
D_MASK = 0b000000100000
F_MASK = 0b000000011111
B_MASK = 0b000011100000
K_MASK = 0b000011111111

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
                register = self._maskRegister(instr)
                destination = self._maskDestination(instr)
                instruction.append("ADDWF")
                instruction.append(str(register))
                instruction.append(str(destination))
            elif instr & 0b111111000000 == ANDWF_MASK:
                register = self._maskRegister(instr)
                destination = self._maskDestination(instr)
                instruction.append("ANDWF")
                instruction.append(str(register))
                instruction.append(str(destination))
            elif instr & 0b111111100000 == CLRF_MASK:
                register = self._maskRegister(instr)
                instruction.append("CLRF")
                instruction.append(str(register))
            elif instr & 0b111111000000 == CLRW_MASK:
                instruction.append("CLRW")
            elif instr & 0b111111000000 == COMF_MASK:
                register = self._maskRegister(instr)
                destination = self._maskDestination(instr)
                instruction.append("COMF")
                instruction.append(str(register))
                instruction.append(str(destination))
            elif instr & 0b111111000000 == DECF_MASK:
                register = self._maskRegister(instr)
                destination = self._maskDestination(instr)
                instruction.append("DECF")
                instruction.append(str(register))
                instruction.append(str(destination))
            elif instr & 0b111111000000 == DECFSZ_MASK:
                instruction = self._createByteOrientedOperation(instr, "DECFSZ")
            elif instr & 0b111111000000 == INCF_MASK:
                instruction = self._createByteOrientedOperation(instr, "INCF")

#            elif instr & 0b == INCFSZ_MASK:
#            elif instr & 0b == IORWF_MASK:
#            elif instr & 0b == MOVF_MASK:
            elif instr & 0b111111100000 == MOVWF_MASK:
                register = instr ^ MOVWF_MASK
                instruction.append("MOVWF")
                instruction.append(str(register))
#            elif instr & 0b == NOP_MASK:
#            elif instr & 0b == RLF_MASK:
#            elif instr & 0b == RRF_MASK:
#            elif instr & 0b == SUBWF_MASK:
#            elif instr & 0b == SWAPF_MASK:
#            elif instr & 0b == XORWF_MASK:
#            elif instr & 0b == BCF_MASK:
#            elif instr & 0b == BSF_MASK:
#            elif instr & 0b == BTFSC_MASK:
#            elif instr & 0b == BTFSS_MASK:
#            elif instr & 0b == ANDLW_MASK:
#            elif instr & 0b == CALL_MASK:
#            elif instr & 0b == CLRWDT_MASK:
#            elif instr & 0b == GOTO_MASK:
#            elif instr & 0b == IORLW_MASK:
            elif instr & 0b110000000000 == MOVELW_MASK:
                instruction.append("MOVLW")
                instruction.append(str(byteArray[2:4])[2:4])
#            elif instr & 0b == OPTION_MASK:
#            elif instr & 0b == RETLW_MASK:
#            elif instr & 0b == SLEEP_MASK:
#            elif instr & 0b == TRIS_MASK:
#            elif instr & 0b == XORLW_MASK:
            instructionStack.append(instruction)
            byteArray = byteArray[4:]
        return instructionStack[::-1]

    def _maskDestination(self, instr):
        destination = instr & D_MASK
        if destination != 0:
            destination = 1
        return destination

    def _makeMask(bits):
        NotImplemented

    def _maskRegister(self, instr):
        return instr & F_MASK

    def _createByteOrientedOperation(self, instr, name):
        register = self._maskRegister(instr)
        destination = self._maskDestination(instr)
        instruction = [name, str(register), str(destination)]
        return instruction

                

            

    def disassemble(self):
        for i in self.instructions:
            if len(i) <= 2:
                print(' '.join(i))
            else:
                print(i[0], ', '.join(i[1:]))
            


