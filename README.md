# Конфигурационное управление

## Домашнее задание №4

**Вариант №23**

  Разработать ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Система команд УВМ представлена далее.
  Для ассемблера необходимо разработать читаемое представление команд УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к которой задается из командной строки. Результатом работы ассемблера является бинарный файл в виде последовательности байт, путь к которому задается из командной строки. Дополнительный ключ командной строки задает путь к файлу-логу, в котором хранятся ассемблированные инструкции в духе списков “ключ=значение”, как в приведенных далее тестах.
  Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон также указывается из командной строки.
  Форматом для файла-лога и файла-результата является csv.
  Необходимо реализовать приведенные тесты для всех команд, а также написать и отладить тестовую программу.

**Загрузка константы**

| A | B | C |
|---|---|---|
| Биты 0—3 | Биты 4—23 | Биты 24—26 |
| 0 | Константа | Адрес |

Размер команды: 4 байт. Операнд: поле B. Результат: регистр по адресу, которым является поле C.

Тест (A=0, B=736, C=0):

0x00, 0x2E, 0x00, 0x00


**Чтение значения из памяти**

| A | B | C | D |
|---|---|---|---|
| Биты 0—3 | Биты 4—6 | Биты 7-9 | Биты 10—23 |
| 57 | Адрес | Адрес | Смещение |

Размер команды: 3 байт. Операнд: значение в памяти по адресу, которым является сумма адреса (регистр по адресу, которым является поле B) и смещения (поле D). Результат: регистр по адресу, которым является поле C.

Тест (A=1, B=4, C=5, D=876):

0xC1, 0xB2, 0x0D


**Запись значения в память**

| A | B | C |
|---|---|---|
| Биты 0—7 | Биты 8—12 | Биты 13—17 |
| 27 | Адрес | Адрес |

Размер команды: 2 байт. Операнд: регистр по адресу, которым является поле B. Результат: значение в памяти по адресу, которым является регистр по адресу, которым является поле C.

Тест (A=6, B=2, C=2):

0x26, 0x01


**Унарная операция: побитовое "не"**

| A | B | C | D |
|---|---|---|---|
| Биты 0—3 | Биты 4—6 | Биты 7—20 | Биты 21—23 |
| 3 | Адрес | Смещение | Адрес |

Размер команды: 3 байт. Операнд: значение в памяти по адресу, которым является сумма адреса (регистр по адресу, которым является поле D) и смещения (поле C). Результат: регистр по адресу, которым является поле B.

Тест (A=3, B=6, C=400, D=4):

0x63, 0xC8, 0x80

Тестовая программа: Выполнить поэлементно операцию побитовое "не" над вектором длины 8.
Результат записать в исходный вектор.


## Описание работы программы программы

Данная программа реализует ассемблер и интерпретатор для учебной виртуальной машины. В ассемблер подаётся программа на обработку и на выходе программы создаётся файл логов и бинарное представление программы. В интерпретаторе производится обработка программы в бинарном представлении и на выходе создаётся файл в формате CSV.


## Запуск программы

Запуск программы осуществляется из командной строки:
```
python assembler.py test_program.asm program.bin program.log
python interpreter.py program.bin result.csv 100-107
```
где:
* test_program.asm - файл с программой для обработки
* program.bin - файл с бинарным представлением программы
* program.log - файл логов работы программы-ассемблера
* result.csv - файл результата работы программы в CSV формате
* 100-107 - байты, используемые для интерпретации бинарного файла

Для запуска юнит-тестов в коммандной строке необходимо написать:
```
python -m unittest test_assembler.py test_interpreter.py
```


## Результат юнит-тестов программы


![photo_2024-12-23_14-06-18](https://github.com/user-attachments/assets/0b230aeb-5c86-4595-b2d4-a5f7d55a64ed)


## Результат работы программы


![photo_2024-12-23_14-05-24](https://github.com/user-attachments/assets/2a57f1c4-623b-4d43-8c1c-6d3174167eac)
