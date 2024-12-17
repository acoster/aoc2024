from enum import Enum
from typing import List

class OpCode(Enum):
    ADV = 0  # A / (2 ** operand) -> A
    BXL = 1  # reg B ˆ literal -> reg B
    BST = 2  # Module 8 to register B
    JNZ = 3  # Jump-not-Zero (register A)
    BXC = 4  # B ^ C -> B
    OUT = 5  # Output operand % 8
    BDV = 6  # A / (2 ** operand) -> B
    CDV = 7  # A / (2 ** operand) -> C

class Machine(object):
    def __init__(self, memory: List[int], reg_a: int, reg_b: int, reg_c: int):
        self.memory = memory
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.pc = 0

    def run(self) -> List[int]:
        output = []
        while self.pc < len(self.memory):
            op_code = OpCode(self.memory[self.pc])
            operand = self.memory[self.pc + 1]

            if op_code == OpCode.ADV:
                self.reg_a = self.reg_a // (1 << self.resolve_operand(operand))
            elif op_code == OpCode.BXL:
                self.reg_b ^= operand
            elif op_code == OpCode.BST:
                self.reg_b = self.resolve_operand(operand) % 8
            elif op_code == OpCode.JNZ:
                if self.reg_a != 0:
                    self.pc = operand
                    continue
            elif op_code == OpCode.BXC:
                self.reg_b ^= self.reg_c
            elif op_code == OpCode.OUT:
                output.append(self.resolve_operand(operand) % 8)
            elif op_code == OpCode.BDV:
                self.reg_b = self.reg_a // (1 << self.resolve_operand(operand))
            elif op_code == OpCode.CDV:
                self.reg_c = self.reg_a // (1 << self.resolve_operand(operand))
            else:
                raise Exception('Invalid opcode')
            self.pc += 2

        return output

    def resolve_operand(self, value: int) -> int:
        if value <= 3: return value
        if value == 4: return self.reg_a
        if value == 5: return self.reg_b
        if value == 6: return self.reg_c
        raise Exception('Invalid operand')
