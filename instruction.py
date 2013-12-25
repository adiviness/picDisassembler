
# Author: Austin Diviness
#
# TODO need to show literals in hex or decimal, preferably with a flag

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
BCF_MASK =    0b010000000000
BSF_MASK =    0b010100000000
BTFSC_MASK =  0b011000000000
BTFSS_MASK =  0b011100000000
###### Literal and control operations
ANDLW_MASK =  0b111000000000
CALL_MASK =   0b100100000000
CLRWDT_MASK = 0b000000000100
GOTO_MASK =   0b101000000000
IORLW_MASK =  0b110100000000
MOVLW_MASK =  0b110000000000
OPTION_MASK = 0b000000000010
RETLW_MASK =  0b100000000000
SLEEP_MASK =  0b000000000011
TRIS_MASK =   0b000000000000
XORLW_MASK =  0b111100000000
##### Helper masks
D_MASK = 0b000000100000
F_MASK = 0b000000011111
B_MASK = 0b000011100000
K_MASK = 0b000011111111
##### Opcode format masks
BYTE_OPCODE_MASK =    0b111111000000
BIT_OPCODE_MASK =     0b111100000000
LITERAL_OPCODE_MASK = 0b111100000000
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
            # Byte oriented file register operations
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
            # Bit oriented file register operations
            elif instr & BIT_OPCODE_MASK == BCF_MASK:
                instruction = self._createBitOrientedOperation(instr, "BCF")
            elif instr & BIT_OPCODE_MASK == BSF_MASK:
                instruction = self._createBitOrientedOperation(instr, "BSF")
            elif instr & BIT_OPCODE_MASK == BTFSC_MASK:
                instruction = self._createBitOrientedOperation(instr, "BTFSC")
            elif instr & BIT_OPCODE_MASK == BTFSS_MASK:
                instruction = self._createBitOrientedOperation(instr, "BSFSS")
            # Logical and control Operations
            elif instr & LITERAL_OPCODE_MASK == ANDLW_MASK:
                instruction = self._createLiteralOperation(instr, "ANDLW")
            elif instr & LITERAL_OPCODE_MASK == CALL_MASK:
                instruction = self._createLiteralOperation(instr, "CALL")
            elif instr == CLRWDT_MASK:
                instruction.append("CLRWDT")
            elif instr & GOTO_OPCODE_MASK == GOTO_MASK:
                jump = instr & 0b000111111111
                instruction.append("GOTO")
                instruction.append(str(jump))
            elif instr & LITERAL_OPCODE_MASK == IORLW_MASK:
                instruction = self._createLiteralOperation(instr, "IORLW")
            elif instr & 0b110000000000 == MOVLW_MASK:
                instruction = self._createLiteralOperation(instr, "MOVLW")
            elif instr == OPTION_MASK:
                instruction.append("OPTION")
            elif instr & LITERAL_OPCODE_MASK == RETLW_MASK:
                instruction = self._createLiteralOperation(instr, "RETLW")
            elif instr == SLEEP_MASK:
                instruction.append("SLEEP")
            elif (instr | TRIS_MASK) >> 3 == 0:
                instruction.append("TRIS")
                instruction.append(str(instr))
            elif instr & LITERAL_OPCODE_MASK == XORLW_MASK:
                instruction = self._createLiteralOperation(instr, "XORLW")

            instructionStack.append(instruction)
            byteArray = byteArray[4:]
        return instructionStack[::-1]

    def _maskDestination(self, instr):
        destination = instr & D_MASK
        if destination != 0:
            destination = 1
        return destination

    def _maskRegister(self, instr):
        return instr & F_MASK

    def _maskBit(self, instr):
        bit = (instr & B_MASK) >> 5
        return bit

    def _maskLiteral(self, instr):
        literal = instr & K_MASK
        return literal

    def _createByteOrientedOperation(self, instr, name):
        register = self._maskRegister(instr)
        destination = self._maskDestination(instr)
        instruction = [name, str(register), str(destination)]
        return instruction

    def _createBitOrientedOperation(self, instr, name):
        register = self._maskRegister(instr)
        bit = self._maskBit(instr)
        instruction = [name, str(register), str(bit)]
        return instruction

    def _createLiteralOperation(self, instr, name):
        literal = self._maskLiteral(instr)
        instruction = [name, str(literal)]
        return instruction

    def disassemble(self):
        address = 0
        for i in self.instructions:
            addressText = "%.4d" % address
            if len(i) <= 2:
                print(addressText, '\t'.join(i), sep='\t')
            else:
                print(addressText, i[0], ',\t'.join(i[1:]), sep='\t')
            address += 3
            


