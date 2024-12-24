class Processor:
    LOAD = 0      # 000
    STORE = 1     # 001
    ADD = 2       # 010
    JUMP_IF = 3   # 011
    JUMP = 4      # 100
    TERMINATE = 5 # 101
    CMP = 6       # 110
    INC = 7       # 111
    MOVE = 8      # 1000

    def __init__(self, RAM_size = 2048, SSD_size = 2048):
        self.reg = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0}
        self.pc = 0  # Счетчик команд (Program Counter)
        self.cmp_flag = 0  # Начальное значение флага сравнения
        self.data_memory = [0] * SSD_size # Инициализация массива данных
        self.command_memory = [0] * RAM_size # Инициализация списка команд

    def load_data(self, initial_data):
        if len(initial_data) > len(self.data_memory):
            raise ValueError(f"Размер загружемых данных больше размера постоянных данных")
        self.data_memory[:len(initial_data)] = initial_data

    def load_program(self, program):
        if len(program) > len(self.command_memory):
            raise ValueError(f"Размер программы больше размера оперативной памяти")
        for i in range(len(program)):
            self.command_memory[i] = program[i]

    def fetch_instruction(self, pc):
        # Извлечение инструкции по адресу программы
        binary_instruction = self.command_memory[pc]
        instruction = []
        instruction.append((binary_instruction & 0b11110000000000000000000000000000) >> 28)
        instruction.append((binary_instruction & 0b00001110000000000000000000000000) >> 25)
        instruction.append((binary_instruction & 0b00000001110000000000000000000000) >> 22)
        instruction.append((binary_instruction & 0b00000000001110000000000000000000) >> 19)
        instruction.append((binary_instruction & 0b00000000000001111111111111111111))
        return instruction

    def execute_program(self):
        running = True
        while running:
            instruction = self.fetch_instruction(self.pc)  # Извлечение команды
            running = self.decode_and_execute(instruction)  # Декодирование и выполнение команды
            self.pc += 1  # Переход к следующей команде
            print()

    def decode_register(self, code):
        return {
            0: 'R0',
            1: 'R1',
            2: 'R2',
            3: 'R3',
            4: 'R4'
        }[code]

    def decode_and_execute(self, instruction):
        cmd_type = instruction[0]
        op1 = instruction[1]
        op2 = instruction[2]
        op3 = instruction[3]
        literal = instruction[4]

        if cmd_type == self.LOAD:
            self.reg[self.decode_register(op1)] = self.data_memory[self.reg[self.decode_register(op2)]]  # Загрузка данных из памяти в регистр
        elif cmd_type == self.STORE:
            self.data_memory[literal] = self.reg[self.decode_register(op1)] 
        elif cmd_type == self.ADD:
            self.reg[self.decode_register(op1)] = self.reg[self.decode_register(op2)] + self.reg[self.decode_register(op3)]
        elif cmd_type == self.MOVE:
            self.reg[self.decode_register(op1)] = literal
        elif cmd_type == self.TERMINATE:
            return False
        elif cmd_type == self.JUMP:
            self.pc = literal -1 # Переход к указанному адресу
        elif cmd_type == self.JUMP_IF:
            if self.cmp_flag == 0:
                self.pc = literal-1   # Переход к метке завершения
                #return True # Не увеличивать PC, т.к. прыжок
        elif cmd_type == self.INC:
            self.reg[self.decode_register(op1)] += 1  # Увеличение значения регистра на 1
        elif cmd_type == self.CMP:
            if self.reg[self.decode_register(op1)] > self.reg[self.decode_register(op2)]:
                self.cmp_flag = 1  # Первый регистр больше второго
            elif self.reg[self.decode_register(op1)] < self.reg[self.decode_register(op2)]:
                self.cmp_flag = -1  # Первый регистр меньше второго
            else:
                self.cmp_flag = 0  # Регистр равны
            


        # Вывод текущего состояния процессора
        print(f"PC: {self.pc}")
        print("Регистры: " + str(self.reg))
        print("Память данных: " + ", ".join(map(str, self.data_memory)))

        return True
