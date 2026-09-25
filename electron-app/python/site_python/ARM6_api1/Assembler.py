from views import counter

# Las animaciones de las lineas seguirian las microoperaciones de ejecucion (Por ejemplo, linea DATA -> MAR)
# El orden de la animacion esta definidio en fetch y decode por un orden establecido, mientras que en execute
# se realizaria siguiendo los pasos de las microoperaciones de cada mnemonico del COP

# Anotacion: En Python se trabajara con valores decimales y binarios, pero luego se traduciran a hexadecimales en JSON
# 1.- Escribir el script (Array de array de lineas de codigo)
# 2.- Extraer las lineas de codigo (Clasificarlos segun estructura de la instruccion por cada linea de codigo)
# 3.- Establecer el SymbolTable (Linked List de los Future Symbols)
# 4.- Realizar las operaciones
# 5.- 
# 6.- 

# Opcion de exportar e importar (object files)

# Estructura de la instruccion:
# Label (Can be Null).
# Directives (Can be Null)
# Mnemonic of OpCode
# Operand 1 (It's obligatory)
#   00 - Absolute Instruction
#   01 - Relocatable instruction
#   10 - Special relocation
#   11 - Loader directives
# Operand 2 (Can be Null)
#   00 - Absolute Instruction
#   01 - Relocatable instruction
#   10 - Special relocation
#   11 - Loader directives
# Operand 3 (Can be Null)
#   00 - Absolute Instruction
#   01 - Relocatable instruction
#   10 - Special relocation
#   11 - Loader directives
# Comment
# Mode (User mode, FIQ mode, IRQ mode, Supervisor mode, Abort mode, Undefined mode)
# Displacement (Offset -> 8-12 bits)
# Relocation bit (True or False: Basicamente si pertenece a el operando a un
#                   Linked List sera True y coloca el LC del nodo siguiente)

mode = ["User mode", "FIQ mode", "IRQ mode", "Supervisor mode", "Abort mode", "Undefined mode"]

def index(dictionary, index):
    new_list = list(dictionary.keys())
    index_position = new_list.index(index)
    return index_position

# Label y directive pueden ser valores nulos
class instruction:
    def __init__(self, LocationCounter, register, operand2, mode):
        self.lc = LocationCounter
        self.label = ""
        self.directive = ""
        self.inmediateOperand = 0b1 # Si self.operand2: self.inmediateOperand = 0b0, indicando que existe
        self.mnemonic = 0b0000
        self.conditionCode = 0b0 # Si set condition code (1000, 1001, 1010, 1011 entonces es 1, de otra manera es 0)
        self.operandRegister = register # Siempre sera un registro de donde provenga el operando 1
        self.destinationRegister = 0b0000 # Siempre sera un registro destino
        if operand2 in registers: # Siempre sera el operando 2
            self.operand2 = {
                'Shift': 0b00000000,
                'operand': bin(index(registers, operand2)),
                'identificationBits': 0b00
            }
        elif bin(operand2) <= 0b11111111: 
            self.operand2 = {
                'Rotate': 0b0000,
                'operand': bin(operand2),
                'identificationBits': 0b00
            }
        # operand2 not in registers permite aplicar una condicional de strings
        elif type(operand2) is type("string") and operand2 not in registers:
            self.operand2 = {
                'operand': operand2,
                'identificationBits': 0b00
            }
        else:
            print("El operando debe ser valido")
        # self.comment = ""
        self.mode = mode
        self.displacement = 0b0000000000

        # Labels normally have a maximum size (typically 6 or 8 characters), must start with a letter,
        # and may only consist of letters, digits, and a few other characters.
        if(len(self.label) >= 8):
            for letra in abecedario:
                if(str(self.label)[0] != letra):
                    print("El label no es valido")
        
        #if(self.displacement > 127 & self.displacement < 0):
        #    print("El displacement no es valido")

    def get_list(self):
        return [self.label, self.directive, self.mnemonic, self.operand1, self.operand2, self.operand3, self.comment, self.mode, self.displacement]

    def get_info(self):
        return f"{self.mnemonic}, {self.operand1}, {self.mode}"

# Linked list
class Node:
    def __init__(self, name, data, type):
        self.name = name
        self.data = data
        self.type = type
        self.next = None

SymbolTable = []

def searchSymbolTable(ins):
    while node:
        if ins.operand2 == node.type:
            
        else:
            node = node.next
    
    # Si fuese un label que no estuviese en el SymbolTable
    if type(ins.label) == type("string"):
        node = Node(ins.operand2["operand"], ins.loc, "D")
        node.next = searchSymbolTable()
    # 
    elif ins.operand2["operand"] == "U":
        node = Node(ins.operand2["operand"], ins.loc, "U")
        node.type = "D"
    else:
        print("Label is doubly defined")
        OnePassAssembler()


def scanSymbolTable():
    for symbol in SymbolTable:
        if symbol.node.type != "U":
            print("Compilacion exitosa")
            break
        else:
            print("Error! Undefined Symbol")
            break

def convertir(script):
    # line_code seria un array bidimensional
    line_code = []

    # Rellenar las filas con 10 valores vacios
    for filas in range(len(script)):
        instruccion = []
        vacio = [""]
        for columnas in range(10):
            instruccion += vacio
        line_code.append(instruccion)

    # Dividir los valores de la linea en una fila de 10 columnas
    if '\r\n' in script:
        pre_line_code = script.split("\r\n")
        for line in pre_line_code:
            if ' ' in line:
                command = line.split(" ")
                line_code.append(command)

    return line_code

instructions = []
def lexicalScanRoutine(object_code): 
    # Almacena la direccion en que la instruccion se cargara. Es decir, la direccion actual, pero no la instruccion
    # Tan solo muestra donde la instruccion sera eventualmente cargada
    # Cada vez que se compila el programa, se reinicia.
    LocationCounter = counter
    
    object_code = [ ["LOOP", "AND", "R0", "R1", "", "", "", "", "", ""],
                   ["", "", "", "", "", "", "", "", "", ""] ]
    
    for line in range(len(object_code)):
        # Inicializacion de la instruccion
        instructionScan = instruction(LocationCounter + object_code.index(line), "", "", 1)

        for column in range(len(object_code[line])):
            # Label
            if ":" in object_code[line][0]:
                # Buscar el Label en el SymbolTable
                for Symbol in SymbolTable:
                    if object_code[line][0] in SymbolTable[Symbol][0]:
                        print("El Label esta registrado en el Symbol Table")
                        break
                    else:
                        object_code[line][0] = object_code[line][0].split(":")
                        instructionScan.label = object_code[line][0]

            # Directive
            for directive in DirectiveTable:
                instructionScan.directive = object_code[line][1]

            # Mnemonic
            for mnemonic in OpCodeTable:
                if column >= 0 & column <= 3:
                    instructionScan.mnemonic = object_code[line][2]

            # Operand1
            if column >= 1 & column <= 4:
                for register in registers:
                    # Inmediate mode
                    if object_code[line][column] < 4292967294 & "#" in object_code[line][column]:
                        object_code[line][column] = object_code[line][column].split("#")
                        instructionScan.operand1 = object_code[line][column]
                        index_operand1 = column
                    # Obtain value from register
                    elif object_code[line][column] == registers[register]:
                        instructionScan.operand1 = object_code[line][column]
                        index_operand1 = column
                    # Busqueda del simbolo en la Symbol Table
                    else:
                        pass
            # Relocation bit
            if instructionScan.label in SymbolTable:
                instructionScan.relocationBit = True
            else:
                instructionScan.relocationBit = False

            # Operand2
            if instructionScan.operand1:
                if object_code[line][index_operand1 + 1] < 4292967294 & "#" in object_code[line][index_operand1 + 1] & object_code[line][index_operand1 + 1] != instruction.operand1:
                    instructionScan.operand2 = object_code[line][index_operand1 + 1]
                    index_operand2 = column
                elif object_code[line][index_operand1 + 1] == registers[register]:
                    instructionScan.operand2 = object_code[line][index_operand1 + 1]
                    index_operand2 = column
                else:
                    pass

            # Comment
            if ";" in object_code[line][column]:
                object_code[line][column] = object_code[line][column].split(";")
                instructionScan.comment = object_code[line][column]

            # Mode (Activado mediante opciones del software del simulador)
            instructionScan.mode = mode

            # Displacement
        
        instructions.append(instructionScan.get_list())
        LocationCounter = 

# Table Search Procedures:

# El OpCodeTable es una static data structure: se aplicara un nested dictionary
# Cada source line tendra cuatro campos: mnemonic, OpCode, type, length
# {/* ARM Instruction set */}
# {/* Branch and Branch with Link: B, BL */}
# {/* Single Data transfer: LDR, STR */}
# {/* Arithmetic Operations: ADC, ADD, MUL, SBC, SUB */}
# {/* Logic Operations: AND, EOR, ORR */}
# {/* XOR de manera de obtener el complemento de un numero */}
OpCodeTable = {
    "AND": {
        "OpCode": "0",
        "type": "RR",
        "length": 5,
    }, 
    "EOR": {
        "OpCode": "1",
        "type": "RR",
        "length": 5,
    },
    "ORR": {
        "OpCode": "1",
        "type": "RR",
        "length": 2,
    }
}

# DirectiveTable es una static data structure: se aplicara un nested dictionary
DirectiveTable = {
    "COMMENT",
    "FUNCTION",
    "IMPORT"
}

# Este es un one-pass assembler que lee el source file una vez. Unicamente que tambien funciona como si fuese
# un two-pass assembler, puesto que genera un relocatable object file que sera cargado en memoria por Loader.
mode = [1, 2, 3, 4, 5, 6]
def OnePassAssembler():
    # Resolucion de multiply-defined labels
    #if(instruction.label == SymbolTable.label):
    #    append("name", NUL, "MTDF")

    # El puntero sera almacenado en un registro o localizacion de memoria, y sera usado para encontrar la siguiente instruccion incompleta
    # register()
    for index in instructions:
        if instructions[index.mnemonic] == "AND":
            operationAND()
        elif instruction.mnemonic == "EOR":
            operationEOR()
        elif instruction.mnemonic == "ORR":
            operationORR()
        else: 

    # Lexical Scan Routine     
    script = "MOV AH\r\nDEL FE"
    object_code = convertir(script)
    
    for ins in instructions:
        # End of file
        if instructions.index(ins) == len(instructions):
            scanSymbolTable()
        else:
            if range(len(ins.label)) > range(len("")):
                searchSymbolTable()
            else:
                if ins.operand2 != 
        

    return command

# Esta compuesto de 31 general 32-bit registers: esta compuesto de 32 biestables, lo que podra contar
# de 0 a 2^32 - 1.
registers = {"R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0, "R7": 0, "R8": 0, "R9": 0, "R10": 0,
                 "R11": 0, "R12": 0, "R13": 0, "R14": 0}

def changeRegisterValue(register, value):
    if(value <= 4294967295 & value >= 0):
        registers[register] = value
    else:
        print("El valor del registro no es valido")
    
    return registers[register]

def Loader():
    # Loader: Se podria considerar el codigo de script de python de Django como si fuese el Loader,
    # puesto que cargara el resultado al simulador
    pass

