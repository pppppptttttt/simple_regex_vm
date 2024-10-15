class RegexVM:
    def __init__(self, regex):
        self.__instructions = self.compile_regex(regex)
        self.__pc = 0
        self.__input_str = ""
        self.__index = 0

    def run(self, input_str):
        self.__input_str = input_str
        self.__index = 0
        self.__pc = 0
        return self.__execute()

    def __execute(self):
        while self.__pc < len(self.__instructions):
            instruction = self.__instructions[self.__pc]
            command_parts = instruction.split()
            command = command_parts[0]

            if command == "char":
                if self.__index < len(self.__input_str) and\
                   self.__input_str[self.__index] == command_parts[1]:
                    self.__index += 1
                    self.__pc += 1
                else:
                    return False

            elif command == "match":
                return True

            elif command == "jmp":
                self.__pc = int(command_parts[1])

            elif command == "split":
                next_pc = self.__pc + 1
                left_branch = int(command_parts[1])
                right_branch = int(command_parts[2])

                if self.__execute_branch(left_branch):
                    return True
                self.__pc = next_pc
                if self.__execute_branch(right_branch):
                    return True
                return False

        return False

    def __execute_branch(self, branch):
        self.__pc = branch
        return self.__execute()

    @staticmethod
    def compile_regex(regex):
        instructions = []

        for char in regex:
            if char == 'a' or char == 'b':
                instructions.append(f"char {char}")
            elif char == '+':
                if instructions and instructions[-1].startswith("char"):
                    last_char = instructions.pop()
                    instructions.append(last_char)
                    instructions.append(
                        f"split {len(instructions)-1} {len(instructions)+1}")
            elif char == '*':
                if instructions and instructions[-1].startswith('char'):
                    last_char = instructions.pop()
                    instructions.append(
                        f"split {len(instructions)+1} {len(instructions)+3}")
                    instructions.append(last_char)
                    instructions.append(f"jmp {len(instructions)-2}")
            elif char == '?':
                if instructions and instructions[-1].startswith("char"):
                    last_char = instructions.pop()
                    instructions.append(
                        f"split {len(instructions)+1} {len(instructions)+2}")
                    instructions.append(last_char)
            elif char == '|':
                if instructions and instructions[-1].startswith("char"):
                    last_char = instructions.pop()
                    instructions.append(
                        f"split {len(instructions)+1} {len(instructions)+3}"
                    )
                    instructions.append(last_char)
                    instructions.append(f"jmp {len(instructions)+2}")

        instructions.append("match")
        return instructions
