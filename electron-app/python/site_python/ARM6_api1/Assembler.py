from views import counter

# Las animaciones de las lineas seguirian las microoperaciones de ejecucion (Por ejemplo, linea DATA -> MAR)
# El orden de la animacion esta definidio en fetch y decode por un orden establecido, mientras que en execute
# se realizaria siguiendo los pasos de las microoperaciones de cada mnemonico del COP

# Anotacion: En Python se trabajara con valores decimales y binarios, pero luego se traduciran a hexadecimales en JSON
# 1.- Escribir el script (Array de array de lineas de codigo)
# 2.- Extraer las lineas de codigo (Clasificarlos segun estructura de la instruccion por cada linea de codigo)
# 3.- Establecer el SymbolTable (Linked List de los Future Symbols)
# 4.- Realizar las operaciones

# Opcion de exportar e importar (object files)
# Problemas de codigo
# 1. Formato de instrucciones
# 2. Analizador Lexico (Adaptarlo a todos los formatos de instrucciones sin hardcodear)
# 3. Finalizar SearchSymbolTable

mode = ["User mode", "FIQ mode", "IRQ mode", "Supervisor mode", "Abort mode", "Undefined mode"]

def index(dictionary, index):
    new_list = list(dictionary.keys())
    index_position = new_list.index(index)
    return index_position

# Label y directive pueden ser valores nulos
class instruction:
    def __init__(self, LocationCounter, mnemonic, register, operand2, mode):
        # Data Processing:
        for operation in OpCodeTable[0]:
            if mnemonic == operation:
                self.lc = LocationCounter
                self.label = ""
                self.directive = ""
                self.inmediateOperand = 0b1 # Si self.operand2: self.inmediateOperand = 0b0, indicando que existe
                self.mnemonic = bin(index(OpCodeTable, mnemonic)["OpCode"])
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

        # Multiply - Multiply Accumulate:
        for operation in OpCodeTable[1]:
            if mnemonic == operation:
                self.lc = LocationCounter
                self.label = ""
                self.directive = ""
                self.condition = 0b0000
                self.mnemonic = bin(index(OpCodeTable, mnemonic)["OpCode"])
                self.accumulate = 0b0
                self.conditionCode = 0b0 # Si set condition code (1000, 1001, 1010, 1011 entonces es 1, de otra manera es 0)
                self.destinationRegister = 0b0000 # Siempre sera un registro destino
                self.operandRegister1 = register
                self.operandRegister2 = register
                self.operandRegister3 = register
                # self.comment = ""
                self.mode = mode
                self.displacement = 0b0000000000
        
        # Single Data Transfer:
        for operation in OpCodeTable[2]:
            if mnemonic == operation:
                self.lc = LocationCounter
                self.label = ""
                self.directive = ""
                self.inmediateOperand = 0b1 # Si self.operand2: self.inmediateOperand = 0b0, indicando que existe
                self.mnemonic = bin(index(OpCodeTable, mnemonic)["OpCode"])
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
    
    def get_node(self, index):
        count = 0
        if index == 0:
            return self
        else:
            while count != index:
                count = count + 1
                self = self.next
            return self

SymbolTable = []

def searchSymbolTable(ins, state):
    # Primera columna: Nodos Defined
    if state == "D":
        if not SymbolTable:
            nodeD = Node(ins.name, ins.loc, "D")
            SymbolTable.append(nodeD)
        else:
            node = SymbolTable[0]
            while node:
                if node.type != None:
                    node = node.next
                else:
                    nodeD = Node(ins.operand2["operand"], ins.loc, "D")
                    node.next = nodeD

    # Search Symbol Table
    elif state == "S":
        for symbol in SymbolTable:
            indice = SymbolTable.index(symbol)
            node = symbol

            while node:
                if node.type != None:
                    # Continue searching
                    if ins.operand2["operand"] not in node.data:
                        continue
                    # Not found: Nodo Undefined
                    elif indice == len(SymbolTable) - 1 and ins.operand2["operand"] not in node.data:
                        nodeU = Node(ins.operand2["operand"], ins.loc, "U")
                        SymbolTable.append(nodeU)
                    # Found: Esta en Linked List de Nodos Defined
                    elif ins.operand2["operand"] in node.data and node.type == "D":
                        if node.type == "D":
                            assembleLine() # Hace la operacion
                            break
                        else:
                            # Realizar el punto 7
                            pass
                    # Found: Esta en Linked List de Nodos Undefined
                    elif ins.operand2["operand"] in node.data and node.type == "U":
                        # Type = U
                        if node.type == "U":
                            nodoU = Node(ins.operand2["operand"], ins.loc, "U")
                            nodo = SymbolTable[symbol]
                    node = node.next
    
    #else:
    #   print("Label is doubly defined")
    #   OnePassAssembler()

def scanSymbolTable():
    for symbol in SymbolTable:
        if symbol.type != "U":
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

def assembleLine():
    pass

instructions = []
def lexicalScanRoutine(object_code): 
    # Almacena la direccion en que la instruccion se cargara. Es decir, la direccion actual, pero no la instruccion
    # Tan solo muestra donde la instruccion sera eventualmente cargada
    # Cada vez que se compila el programa, se reinicia.
    LocationCounter = counter
    
    object_code = [ ["LOOP:", "AND", "R0", "R1", "", "", "", "", "", ""],
                   ["", "", "", "", "", "", "", "", "", ""] ]
    
    for line in range(len(object_code)):
        # Inicializacion de la instruccion
        instructionScan = instruction(LocationCounter + object_code.index(line), "", "", 1)

        for column in range(len(object_code[line])):
            for key in OpCodeTable:
                for operation in OpCodeTable[key]:
                    if object_code[line][column] == operation and key == 0:
                        
                        instructions.append(instructionScan.get_list())
                    elif object_code[line][column] == operation and key == 1:
                        instructions.append(instructionScan.get_list())
                    elif object_code[line][column] == operation and key == 2:
                        instructions.append(instructionScan.get_list())
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

# {/* ARM Instruction set */}
# Data Processing Instruction:
#  1. MOV, MVN
#  2. Operaciones aritmeticas: ADC, SBC
#  3. Operaciones logicas: AND, EOR, ORR
# Multiply and Multiply-Accumulate:
# 1. MUL, MLA
# Single Data Transfer:
# 1. LDR, STR
OpCodeTable = {
    # Data Processing: Operaciones logicas
    0 : {
        "AND": {
            "OpCode": 0b0000,
            "type": "RR",
            "length": 5,
        }, 
        "EOR": {
            "OpCode": 0b0001,
            "type": "RR",
            "length": 5,
        },
        "ORR": {
            "OpCode": 0b0010,
            "type": "RR",
            "length": 2,
        },
        "ADC": {
            "OpCode": 0b0011,
            "type": "RR",
            "length": 5
        },
        "SBC": {
            "OpCode": 0b0100,
            "type": "RR",
            "length": 5
        }
    },
    # Multiply - Multiply Accumulate:
    1 : {
        "MUL": {
            "OpCode": 0b0101,
            "type": "RR",
            "length": 4
        },
        "MLA": {
            "OpCode": 0b0110,
            "type": "RR",
            "length": 2
        }
    },
    # Single Data Transfer:
    2: {
        "LDR": {
            "OpCode": 0b0111,
            "type": "RR",
            "length": 2
        },
        "STR": {
            "OpCode": 0b1000,
            "type": "RR",
            "length": 3
        }
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
def OnePassAssembler():
    # Resolucion de multiply-defined labels
    #if(instruction.label == SymbolTable.label):
    #    append("name", NUL, "MTDF")

    # STR R2, #2
    # ADC R1, R2, #3

    # El puntero sera almacenado en un registro o localizacion de memoria, y sera usado para encontrar la siguiente instruccion incompleta
    for instruction in instructions:
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
            # Label Defined
            if range(len(ins.label)) > range(len("")):
                searchSymbolTable(ins, "D")
            else:
                # A Symbol used
                if ins.operand2["operand"] == type("string"):
                    searchSymbolTable(ins, "S")

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

