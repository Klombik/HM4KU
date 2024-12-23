# test.py
import unittest
import os
from assembler import assemble
from interpreter import interpret

class TestVM(unittest.TestCase):
    def setUp(self):
        self.asm_file = "test.asm"
        self.bin_file = "test.bin"
        self.log_file = "test.log"
        self.res_file = "test.res"
        
    def tearDown(self):
        for f in [self.asm_file, self.bin_file, self.log_file, self.res_file]:
            if os.path.exists(f):
                os.remove(f)
                
    def test_load(self):
        # Test from specification: A=0, B=736, C=0
        with open(self.asm_file, 'w') as f:
            f.write("LOAD 736 0")
            
        assemble(self.asm_file, self.bin_file, self.log_file)
        
        with open(self.bin_file, 'rb') as f:
            data = f.read()
            self.assertEqual(data, bytes([0x00, 0x2E, 0x00, 0x00, 0x00]))
            
    def test_read(self):
        # Test from specification: A=1, B=4, C=5, D=876
        with open(self.asm_file, 'w') as f:
            f.write("READ 4 5 876")
            
        assemble(self.asm_file, self.bin_file, self.log_file)
        
        with open(self.bin_file, 'rb') as f:
            data = f.read()
            self.assertEqual(data, bytes([0xC1, 0xB2, 0x0D, 0x00]))
            
    def test_write(self):
        # Test from specification: A=6, B=2, C=2
        with open(self.asm_file, 'w') as f:
            f.write("WRITE 2 2")
            
        assemble(self.asm_file, self.bin_file, self.log_file)
        
        with open(self.bin_file, 'rb') as f:
            data = f.read()
            self.assertEqual(data, bytes([0x26, 0x01, 0x00]))
            
    def test_not(self):
        # Test from specification: A=3, B=6, C=400, D=4
        with open(self.asm_file, 'w') as f:
            f.write("NOT 6 400 4")
            
        assemble(self.asm_file, self.bin_file, self.log_file)
        
        with open(self.bin_file, 'rb') as f:
            data = f.read()
            self.assertEqual(data, bytes([0x63, 0xC8, 0x80, 0x00]))
            
    def test_program(self):
        # Test program: NOT operation on vector of length 8
        program = """
        LOAD 0 0    ; Initialize counter
        LOAD 8 1    ; Vector length
        LOAD 100 2  ; Vector base address
        READ 2 3 0  ; Read value from memory
        NOT 4 0 3   ; NOT operation
        WRITE 4 2   ; Write result back
        LOAD 1 5    ; Increment
        ADD 0 5 0   ; Increment counter
        JLT 0 1 -6  ; Loop if counter < length
        """
        
        with open(self.asm_file, 'w') as f:
            f.write(program)
            
        assemble(self.asm_file, self.bin_file, self.log_file)
        interpret(self.bin_file, self.res_file, "100-107")
        
        # Check results
        with open(self.res_file) as f:
            lines = f.readlines()[1:]  # Skip header
            for line in lines:
                addr, value = map(int, line.strip().split(','))
                self.assertEqual(value, ~0)  # All values should be NOT of initial 0

if __name__ == '__main__':
    unittest.main()