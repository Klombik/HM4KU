import struct
import csv
import sys

COMMANDS = {
    "LOAD": 0,
    "READ": 1,
    "WRITE": 6,
    "NOT": 3,
}

def assemble(input_file, output_file, log_file):
    binary_data = []
    log_data = []

    # Чтение текстового файла с программой с явным указанием кодировки
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    for line in lines:
        # Удаляем комментарии и лишние пробелы
        line = line.split(';')[0].strip()  # Удаляем всё после ';'
        if not line:  # Пропускаем пустые строки
            continue

        parts = line.split()
        cmd = parts[0]
        # Извлекаем только числовые аргументы, игнорируя нечисловые (например, метки)
        args = []
        for part in parts[1:]:
            try:
                args.append(int(part))
            except ValueError:
                # Если не удалось преобразовать в int, пропускаем этот аргумент
                continue
        
        if cmd not in COMMANDS:
            print(f"Unknown command: {cmd}")
            continue

        opcode = COMMANDS[cmd]

        if cmd == 'LOAD':
            b = args[0]  # Константа
            c = args[1]  # Адрес регистра
            instruction = (opcode & 0xF) | ((b & 0xFFFFF) << 4) | ((c & 0x7) << 24)
            binary_data.append(struct.pack('<I', instruction))
            log_data.append({'A': opcode, 'B': b, 'C': c, 'D': ''})

        elif cmd == 'READ':
            b = args[0]  # Адрес регистра базы
            c = args[1]  # Адрес регистра результата
            d = args[2]  # Смещение
            instruction = (opcode & 0xF) | ((b & 0x7) << 4) | ((c & 0x7) << 7) | ((d & 0x3FFF) << 10)
            binary_data.append(struct.pack('<I', instruction)[:3])
            log_data.append({'A': opcode, 'B': b, 'C': c, 'D': d})

        elif cmd == 'WRITE':
            b = args[0]  # Адрес регистра значения
            c = args[1]  # Адрес регистра адреса
            instruction = (opcode & 0xF) | ((b & 0x7) << 4) | ((c & 0x7) << 7)
            binary_data.append(struct.pack('<H', instruction))
            log_data.append({'A': opcode, 'B': b, 'C': c, 'D': ''})

        elif cmd == 'NOT':
            b = args[0]  # Адрес регистра результата
            c = args[1]  # Смещение
            d = args[2]  # Адрес регистра базы
            instruction = (opcode & 0xF) | ((b & 0x7) << 4) | ((c & 0x3FFF) << 7) | ((d & 0x7) << 21)
            binary_data.append(struct.pack('<I', instruction)[:3])
            log_data.append({'A': opcode, 'B': b, 'C': c, 'D': d})

    # Добавление завершающего байта
    binary_data.append(struct.pack('B', 0))

    # Сохранение в бинарный файл
    with open(output_file, 'wb') as outfile:
        for data in binary_data:
            outfile.write(data)

    # Сохранение лога
    with open(log_file, 'w', newline='', encoding='utf-8') as logfile:
        fieldnames = ['A', 'B', 'C', 'D']
        writer = csv.DictWriter(logfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(log_data)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Использование: python assembler.py <входной_файл> <выходной_файл> <лог_файл>")
        sys.exit(1)
    assemble(sys.argv[1], sys.argv[2], sys.argv[3])