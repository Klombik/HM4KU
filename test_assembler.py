import unittest
import os
import struct
import csv
from assembler import assemble


class TestAssembler(unittest.TestCase):
    def setUp(self):
        self.input_file = "test_program.txt"
        self.output_file = "test_program.bin"
        self.log_file = "test_program_log.csv"

    def tearDown(self):
        # Удаляем тестовые файлы после выполнения тестов
        for file in [self.input_file, self.output_file, self.log_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_load(self):
        # Запись программы с командой LOAD 1 100
        with open(self.input_file, 'w') as f:
            f.write("LOAD 1 100\n")  # Заменили LOAD_CONST на LOAD

        assemble(self.input_file, self.output_file, self.log_file)
        
    def test_invalid_command(self):
        # Запись программы с недопустимой командой
        with open(self.input_file, 'w') as f:
            f.write("INVALID_CMD 1 100\n")

        assemble(self.input_file, self.output_file, self.log_file)

        # Проверяем, что бинарный файл пуст
        with open(self.output_file, 'rb') as f:
            data = f.read()
            self.assertEqual(len(data), 1)  # Только байт окончания

        # Проверяем, что лог-файл пуст (кроме заголовка)
        with open(self.log_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(len(rows), 0)
