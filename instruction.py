
from binascii import *


ADDWF_MASK =  0b000111000000
ANDWF_MASK =  0b000101000000
CLRF_MASK =   0b000001100000
CLRW_MASK =   0b000001000000
COMF_MASK =   0b001001000000
DECF_MASK =   0b000011000000
DECFSZ_MASK = 0b001011000000
INCF_MASK =   0b001010000000
INCFSZ_MASK = 0b001111000000
IORWF_MASK =  0b000100000000
MOVF_MASK =   0b001000000000
MOVWF_MASK =  0b000000100000
NOP_MASK =    0b000000000000
RLF_MASK =    0b001101000000
RRF_MASK =    0b001100000000
SUBWF_MASK =  0b000010000000
SWAPF_MASK =  0b001110000000
XORWF_MASK =  0b000110000000
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
##### Opcode format masks
BYTE_OPCODE_MASK =    0b111111000000
BIT_OPCODE_MASK =     0b111100000000
CONTROL_OPCODE_MASK = 0b111100000000
GOTO_OPCODE_MASK =    0b111000000000

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
            if instr & BYTE_OPCODE_MASK == ADDWF_MASK:
                instruction = self._createByteOrientedOperation(instr, "ADDWF")
            elif instr & BYTE_OPCODE_MASK == ANDWF_MASK:
                instruction = self._createByteOrientedOperation(instr, "ANDWF")
            elif instr & 0b111111100000 == CLRF_MASK:
                register = self._maskRegister(instr)
                instruction.append("CLRF")
                instruction.append(str(register))
            elif instr & 0b111111000000 == CLRW_MASK:
                instruction.append("CLRW")
            elif instr & BYTE_OPCODE_MASK == COMF_MASK:
                instruction = self._createByteOrientedOperation(instr, "COMF")
            elif instr & BYTE_OPCODE_MASK == DECF_MASK:
                instruction = self._createByteOrientedOperation(instr, "DECF")
            elif instr & BYTE_OPCODE_MASK == DECFSZ_MASK:
                instruction = self._createByteOrientedOperation(instr, "DECFSZ")
            elif instr & BYTE_OPCODE_MASK == INCF_MASK:
                instruction = self._createByteOrientedOperation(instr, "INCF")
            elif instr & BYTE_OPCODE_MASK == INCFSZ_MASK:
                instruction = self._createByteOrientedOperation(instr, "INCFSZ")
            elif instr & BYTE_OPCODE_MASK == IORWF_MASK:
                instruction = self._createByteOrientedOperation(instr, "IORWF")
            elif instr & BYTE_OPCODE_MASK == MOVF_MASK:
                instruction = self._createByteOrientedOperation(instr, "MOVF")
            elif instr & 0b111111100000 == MOVWF_MASK:
                register = instr ^ MOVWF_MASK
                instruction.append("MOVWF")
                instruction.append(str(register))
            elif instr == NOP_MASK:
                instruction.append("NOP")
            elif instr & BYTE_OPCODE_MASK == RLF_MASK:
                instruction = self._createByteOrientedOperation(instr, "RLF")
            elif instr & BYTE_OPCODE_MASK == RRF_MASK:
                instruction = self._createByteOrientedOperation(instr, "RRF")
            elif instr & BYTE_OPCODE_MASK == SUBWF_MASK:
                instruction = self._createByteOrientedOperation(instr, "SUBWF")
            elif instr & BYTE_OPCODE_MASK == SWAPF_MASK:
                instruction = self._createByteOrientedOperation(instr, "SWAPF")
            elif instr & BYTE_OPCODE_MASK == XORWF_MASK:
                instruction = self._createByteOrientedOperation(instr, "XORWF")
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
            


