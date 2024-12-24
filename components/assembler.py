class Assembler:
    def __init__(self):
        self.label_table = {}  # Таблица меток
        self.unresolved_labels = []  # Неразрешённые метки
        self.reg_table = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4}

    def compile(self, instructions):
        machine_code = []
        command_index = 0

        # Первый проход: анализ меток и команд
        for line in instructions:
            trimmed_line = line.strip()
            
            #Игнорировать пустые строки и строки с комментариями
            if not trimmed_line or trimmed_line.startswith("#"):
                continue

            # Лексический анализ: распознавание меток
            if trimmed_line.endswith(":"):
                label = trimmed_line[:-1]
                if label in self.label_table:
                    raise ValueError(f"Метка {label} уже определена.")
                self.label_table[label] = command_index
                continue
            
            command_part = trimmed_line.split("#")[0].strip()

            # Синтаксический анализ команды
            parts = command_part.split()
            cmd_type = parts[0].upper()

            if not self.is_valid_command(cmd_type):
                raise ValueError(f"Неизвестная команда: {cmd_type}")

            # Обработка операндов с метками
            operand1 = self.parse_operand(parts[1], command_index, 0) if len(parts) > 1 else 0
            operand2 = self.parse_operand(parts[2], command_index, 1) if len(parts) > 2 else 0
            operand3 = self.parse_operand(parts[3], command_index, 2) if len(parts) > 3 else 0
            binary_instruction = self.generate_instruction(cmd_type, operand1, operand2, operand3)
            machine_code.append(binary_instruction)
            command_index += 1

        # Второй проход: разрешение меток
        self.resolve_labels(machine_code)

        return machine_code

    def is_valid_command(self, cmd_type):
        return cmd_type in ["LOAD", "STORE", "ADD", "JUMP_IF_EQ", "JUMP", "TERMINATE", "CMP", "INC", "MOV"]

    def generate_instruction(self, cmd_type, operand1, operand2, operand3):
        if cmd_type == "LOAD":
            binary_instruction = ((0 << 28) | (operand1 << 25) | (operand2 << 22))
        elif cmd_type == "STORE":
            binary_instruction = ((1 << 28) | (operand1 << 25) | (operand2))
        elif cmd_type == "ADD":
            binary_instruction = ((2 << 28) | (operand1 << 25) | (operand2 << 22) | (operand3 << 19))
        elif cmd_type == "JUMP_IF_EQ":
            binary_instruction = ((3 << 28) | (operand1)) 
        elif cmd_type == "JUMP":
            binary_instruction = ((4 << 28) | (operand1)) 
        elif cmd_type == "TERMINATE":
            binary_instruction = (5 << 28) 
        elif cmd_type == "CMP":
            binary_instruction = ((6 << 28) | (operand1 << 25) | (operand2 << 22))
        elif cmd_type == "INC":
            binary_instruction = ((7 << 28) | (operand1 << 25))
        elif cmd_type == "MOV":
            binary_instruction = ((8 << 28) | (operand1 << 25) | (operand2))
        else:
            raise ValueError(f"Неизвестная команда: {cmd_type}")

        return binary_instruction
    

    def parse_operand(self, operand, command_index, operand_index):
        # Если операнд является числом
        try:
            if operand.isdigit():
                return int(operand)
            value = self.reg_table[operand]
            return value
        except Exception:
            pass

        # Если операнд является меткой
        if operand in self.label_table:
            resolved_address = self.label_table[operand]
            return resolved_address

        # Если метка ещё не определена, добавляем в нерешённые метки
        self.unresolved_labels.append((operand, command_index, operand_index))
        return 0  # Временно

    def resolve_labels(self, machine_code):
        for unresolved in self.unresolved_labels:
            label, command_index, operand_index = unresolved

            if label not in self.label_table:
                raise ValueError(f"Неразрешённая метка: {label}")

            resolved_address = self.label_table[label]

            # Обновляем нужный операнд
            instruction = machine_code[command_index]
            if operand_index == 0:  # Для JUMP
                machine_code[command_index] = (instruction & 0b11111111111110000000000000000000) | (resolved_address)
            elif operand_index == 1:  # Для JUMP_IF
                machine_code[command_index] = (instruction & 0b11111111111110000000000000000000) | (resolved_address)

