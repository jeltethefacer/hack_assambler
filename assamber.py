import sys
import os

jumpConversionDict = {
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

compConversionTable = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101"
}

compConversionTable1 = {
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

destConversionTable = {
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

# TODO change to local varibles
labels = {
    "R0": "0",
    "R1": "1",
    "R2": "2",
    "R3": "3",
    "R4": "4",
    "R5": "5",
    "R6": "6",
    "R7": "7",
    "R8": "8",
    "R9": "9",
    "R10": "10",
    "R11": "11",
    "R12": "12",
    "R13": "13",
    "R14": "14",
    "R15": "15",
    "SCREEN": "16384",
    "KBD": "24576",
    "SP": "0",
    "LCL": "1",
    "ARG": "2",
    "THIS": "3",
    "THAT": "4"
}

memoryCounter = 16


class Parser():
    def __init__(self, filename, compConversion, destConversion, jumpConversion, labels):
        self.f = open(filename, "r")
        self.lineNumber = 0
        # starts asigning variables from 16 onwards
        self.memoryCounter = 16
        self.compConversion = compConversion
        self.destConversion = destConversion
        self.jumpConversion = jumpConversion
        self.labels = labels

    def makeLabels(self):
        while(True):
            command = self.get_next_command()
            if(command == ""):
                break
            else:
                if(command[0] == "("):
                    string = ""
                    for x in range(1, len(command)-1):
                        string += command[x]
                    self.lineNumber -= 1

                    self.labels[string] = self.lineNumber
        # returns file pointer to begin of file
        self.f.seek(0)

    def get_next_command(self):
        isValidCommand = False

        while(not isValidCommand):
            line = self.f.readline()
            if(line == ""):
                return line
            isValidCommand = False
            command = ""

            for i, c in enumerate(line):
                if(c.isspace()):
                    pass
                elif(c == '/' and line[i+1] == '/'):
                    break
                else:
                    isValidCommand = True
                    command += c
        if(isValidCommand):
            self.lineNumber += 1
        return command

    def isComment(self, line):
        firstSlash = True
        for x in line:
            if(x == '/' and not firstSlash):
                return True
            elif(x == '/'):
                firstSlash = False
            else:
                firstSlash = True
    
    def convert(self):
        print(os.path.splitext(self.f.name))
        fileToSave = open((os.path.splitext(self.f.name)[0] + ".hack"), "w+")
        self.makeLabels()

        while(True):
            command = self.get_next_command()
            if(command == ""):
                break
            else:
                convertedCommand = self.convertCommand(command)
                if(convertedCommand is not None):
                    fileToSave.write(convertedCommand + "\n")



    def convertCommand(self, command):
        if(command[0] == "@"):
            integer = ""
            for x in range(1, len(command)):
                integer += command[x]
            try:
                integer = int(integer)
            except ValueError:
                if integer not in self.labels.keys():
                    self.labels[integer] = str(self.memoryCounter)
                    self.memoryCounter += 1
                integer = int(self.labels[integer])
            return f'0{integer:015b}'
        elif(command[0] != "("):
            splitted = command.split(";")

            jump = "000"
            dest = "000"
            comp = "0101010"

            # fill in jump
            if(len(splitted) == 2):
                jump = self.jumpConversion[splitted[1]]
                leftCommand = splitted[0].split("=")
                if(len(leftCommand) == 2):
                    comp = self.compConversion[leftCommand[1]]
                    dest = self.destConversion[leftCommand[0]]
                elif(len(leftCommand) == 1):
                    comp = self.compConversion[leftCommand[0]]
            elif(len(splitted) == 1):
                leftCommand = splitted[0].split("=")
                if(len(leftCommand) == 2):
                    comp = self.compConversion[leftCommand[1]]
                    dest = self.destConversion[leftCommand[0]]
                elif(len(leftCommand) == 1):
                    comp = self.compConversion[leftCommand[0]]
            return "111" + comp + dest + jump


def decode(filename):
    print(f"filename: {filename}")
    compConversionTableTotal = {**compConversionTable, **compConversionTable1}
    codeParser = Parser(filename, compConversionTableTotal, destConversionTable, jumpConversionDict, labels)
    codeParser.convert()




if __name__ == "__main__":
    decode(sys.argv[1])
