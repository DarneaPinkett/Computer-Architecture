"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b0101000
ADD = 0b10100000
RET = 0b00010001
SUB = 0b10100001
CMP = 0b10100111
JMP = 0b01010100

SP = 7

LT = 0b00000100
GT = 0b00000010
EQ = 0b00000001

class CPU:
    """Main CPU class."""


    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.halted = False
        self.flag_reg = [0] * 8
        self.SP = 0xf3

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def ram_read(self, mar):
        return self.ram[mar]

    def load(self, filename):
        """Load a program into memory."""

        # For now, we've just hardcoded a program:
        try:
            address = 0

            with open(filename) as f:
                for line in f:
                    comment_split = line.split('#')

                    num = comment_split[0].strip()

                    if num != "":
                        continue
                    val = int(num, 2)

                    self.ram[address] = val

                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        
        elif op == "DIV":
            self.reg[reg_a] //= self.reg[reg_b]

        elif op == "CMP":
            a = self.reg[reg_a]
            b = self.reg[reg_b]

            if a == b:
                self.EQ, self.LT, self.GT = (1, 0, 0)
            elif a < b:
                self.EQ, self.LT, self.GT =(0, 1, 0)
            elif a > b:
                self.EQ, self.LT, self.GT = (0, 0, 1)
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while not self.halted:
            ir = self.ram[self.pc]
            instruct_length = ((ir >> 6) & 0b11) + 1
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                self.halted = True

            elif ir == LDI:
                self.reg[operand_a] = operand_b

            elif ir == PRN:
                print(self.reg[operand_a])

            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)

                self.pc += instruct_length
            
            elif ir == SUB:
                self.alu("SUB", operand_a, operand_b)

            elif ir == ADD:
                self.alu("ADD", operand_a, operand_b)

            elif ir == CALL:
                operand_b = self.ram_read(self.pc + 1)

                self.ram_write(self.SP, self.pc + 2)
                self.SP -= 1

                self.pc = self.reg[operand_a]

            elif ir == RET:
                self.PC = self.ram_read(self.SP + 1)
                self.SP += 1

            elif ir == CMP:
                a = self.reg[operand_a]
                b = self.reg[operand_b]
                self.alu("CMP", a, b)

            elif ir == JMP:
                operand_a = self.ram_read(self.pc +1)

                self.PC = self.reg[operand_a]

            elif ir == PUSH:
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]

                self.reg[SP] -= 1

                self.ram[self.reg[SP]] = val
                self.pc += 2

            elif ir == POP:
                reg = self.ram[self.pc + 1]
                val = self.ram[self.reg[SP]]

                self.reg[reg] = val

                self.reg[SP] += 1
                self.pc += 2
            
            elif ir == HLT:
                sys.exit(0)

            else:
                print(f"I did not understand that command: {ir}")
                sys.exit(1)

        # while not self.running:
        #     ir = self.ram[self.pc]
        #     instruction_len = ((ir >> 6) & 0b11) + \
        #         1
        #     reg_num = self.ram_read(self.pc + 1)
        #     value = self.ram_read(self.pc + 2)

        #     if ir == self.HLT:
        #         self.running = True

        #     elif ir == self.LDI:
        #         self.reg[reg_num] = value

        #     elif ir == self.PRN:
        #         print(self.reg[reg_num])

        #     elif ir == self.MUL:
        #         self.alu("MUL", reg_num, value)
            
        #     self.pc += instruction_len

        # while self.running:
        #     ir = self.ram_read(self.pc)
        #     if ir == self.LDI:
        #         reg_num = self.ram_read(self.pc + 1)
        #         value = self.ram_read(self.pc + 2)
        #         self.ram_write(reg_num, value)
        #         self.pc += 3
        #     elif ir == self.HLT:
        #         self.running = False
        #     elif ir == self.PRN:
        #         reg_num = self.ram[self.pc + 1]
        #         print(self.ram[reg_num])
        #         self.pc += 2
        #     else:
        #         print(f'No instructions')
        #         sys.exit(1) 

