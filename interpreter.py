# interpreter.py
import struct
import sys
import csv

class VM:
    def __init__(self):
        self.memory = [0] * 1024
        self.registers = [0] * 8
        
    def load(self, b, c):
        self.registers[c] = b
        
    def read(self, b, c, d):
        addr = self.registers[b] + d
        if 0 <= addr < len(self.memory):
            self.registers[c] = self.memory[addr]
        else:
            raise ValueError(f"Memory access out of bounds: {addr}")
        
    def write(self, b, c):
        addr = self.registers[c]
        if 0 <= addr < len(self.memory):
            self.memory[addr] = self.registers[b]
        else:
            raise ValueError(f"Memory access out of bounds: {addr}")
        
    def not_op(self, b, c, d):
        addr = self.registers[d] + c
        if 0 <= addr < len(self.memory):
            self.registers[b] = ~self.memory[addr] & 0xFFFFFFFF
        else:
            raise ValueError(f"Memory access out of bounds: {addr}")

def interpret(binary_file, result_file, mem_range):
    vm = VM()
    
    with open(binary_file, 'rb') as f:
        code = f.read()
    
    if not code:
        raise ValueError("Empty binary file")
        
    pc = 0
    max_iterations = 1000  # Защита от бесконечного цикла
    iterations = 0
    
    try:
        while pc < len(code) and code[pc] != 0 and iterations < max_iterations:
            iterations += 1
            opcode = code[pc] & 0xF
            
            if opcode == 0:  # LOAD
                if pc + 4 > len(code):
                    break
                instr = struct.unpack('<I', code[pc:pc+4])[0]
                b = (instr >> 4) & 0xFFFFF
                c = (instr >> 24) & 0x7
                vm.load(b, c)
                pc += 4
                
            elif opcode == 1:  # READ
                if pc + 3 > len(code):
                    break
                instr = int.from_bytes(code[pc:pc+3], 'little')
                b = (instr >> 4) & 0x7
                c = (instr >> 7) & 0x7
                d = (instr >> 10) & 0x3FFF
                vm.read(b, c, d)
                pc += 3
                
            elif opcode == 6:  # WRITE
                if pc + 2 > len(code):
                    break
                instr = int.from_bytes(code[pc:pc+2], 'little')
                b = (instr >> 4) & 0x7
                c = (instr >> 7) & 0x7
                vm.write(b, c)
                pc += 2
                
            elif opcode == 3:  # NOT
                if pc + 3 > len(code):
                    break
                instr = int.from_bytes(code[pc:pc+3], 'little')
                b = (instr >> 4) & 0x7
                c = (instr >> 7) & 0x3FFF
                d = (instr >> 21) & 0x7
                vm.not_op(b, c, d)
                pc += 3
            
            else:
                print(f"Unknown opcode {opcode} at position {pc}")
                break
                
        # Отладочный вывод
        #print(f"Команда: {opcode}, Регистры: {registers[:8]}, Память: {memory[:8]}")
                
        if iterations >= max_iterations:
            print("Warning: Maximum number of iterations reached")
            
    except Exception as e:
        print(f"Error during execution: {e}")
        
    try:
        start, end = map(int, mem_range.split('-'))
        if not (0 <= start <= end < len(vm.memory)):
            raise ValueError(f"Invalid memory range: {start}-{end}")
            
        with open(result_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Address', 'Value'])
            for addr in range(start, end + 1):
                writer.writerow([addr, vm.memory[addr]])
                
    except Exception as e:
        print(f"Error writing results: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python interpreter.py <binary_file> <result_file> <memory_range>")
        sys.exit(1)

    #with open("program.bin", "rb") as f:
    #    print(list(f.read()))

    try:
        interpret(sys.argv[1], sys.argv[2], sys.argv[3])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)