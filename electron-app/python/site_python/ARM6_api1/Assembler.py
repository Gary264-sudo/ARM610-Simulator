from views import counter

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

# Principio de codigo:
# 

registers = {"R1": 0, "R2": 0, "R3": 0, "R4": 0, "R5": 0, "R6": 0, "R7": 0, "R8": 0, "R9": 0, "R10": 0,
                 "R11": 0, "R12": 0, "R13": 0, "R14": 0}

mode = ["User mode", "FIQ mode", "IRQ mode", "Supervisor mode", "Abort mode", "Undefined mode"]

# Table Search Procedures:
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

DirectiveTable = {
    "COMMENT",
    "FUNCTION",
    "IMPORT"
}

def index(dictionary, index):
    new_list = list(dictionary.keys())
    index_position = new_list.index(index)
    return index_position

class instructionDataProcessing:
    def __init__(self, LocationCounter, mnemonic, register1, register2, operand2, mode):
        # Data Processing:
        self.lc = LocationCounter
        self.label = ""
        self.directive = ""
        self.inmediateOperand = 0b1 # Si self.operand2: self.inmediateOperand = 0b0, indicando que existe
        self.mnemonic = bin(index(OpCodeTable[0], mnemonic))
        self.conditionCode = 0b0 # Si set condition code (1000, 1001, 1010, 1011 entonces es 1, de otra manera es 0)
        self.operandRegister = register1 # Siempre sera un registro de donde provenga el operando 1
        self.destinationRegister = register2 # Siempre sera un registro destino
        if operand2 in registers: # Siempre sera el operando 2
            self.operand2 = {
                'Shift': {
                    'Shift amount': 0b00000,
                    'Shift type': 0b00
                },
                'operand': bin(index(registers, operand2)),
                'identificationBits': 0b00
            }
        elif type(operand2) is type(0b0) and bin(operand2) <= 0b11111111:
            self.operand2 = {
                'Rotate': {
                    'Shift amount': 0b00000,
                    'Shift type': 0b00
                },
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
        self.comment = ""
        self.mode = mode
        self.displacement = 0b0000000000

        if(len(self.label) >= 8):
            for letra in abecedario:
                if(str(self.label)[0] != letra):
                    print("El label no es valido")
                
        # if(self.displacement > 127 & self.displacement < 0):
        # print("El displacement no es valido")

    def get_list(self):
        return {'label': self.label, 'directive': self.directive, 'mnemonic': self.mnemonic, 'operandRegister': self.operandRegister, 'destinationRegister': self.destinationRegister, 'operand2': self.operand2, 'comment': self.comment, 'mode': self.mode, 'displacement': self.displacement}

    def get_info(self):
        return f"Information: {self.label}, {self.directive}, {self.mnemonic}, {self.operandRegister}, {self.destinationRegister}, {self.operand2}, {self.comment}, {self.mode}, {self.displacement}"

# Se tiene que realizar las condicionales
class instructionMultiply:
    def __init__(self, LocationCounter, register1, register2, register3, register4, mode):
        # Multiply - Multiply Accumulate:
        self.lc = LocationCounter
        self.label = ""
        self.directive = ""
        self.condition = 0b0000
        self.accumulate = 0b0
        self.conditionCode = 0b0 # Si set condition code (1000, 1001, 1010, 1011 entonces es 1, de otra manera es 0)
        self.destinationRegister = register1 # Siempre sera un registro destino
        self.operandRegister1 = register2
        self.operandRegister2 = register3
        self.operandRegister3 = register4
        self.comment = ""
        self.mode = mode
        self.displacement = 0b0000000000
    
    def get_list(self):
        return [self.label, self.directive, self.condition, self.accumulate, self.conditionCode, self.destinationRegister, self.operandRegister1, self.operandRegister2, self.operandRegister3, self.comment, self.mode, self.displacement]

    def get_info(self):
        return f"Information: {self.label}, {self.directive}, {self.condition}, {self.accumulate}, {self.conditionCode}, {self.destinationRegister}, {self.operandRegister1}, {self.operandRegister2}, {self.operandRegister3}, {self.comment}, {self.mode}, {self.displacement}"

# Se tiene que realizar las condicionales
class instructionSingleData:
    def __init__(self, LocationCounter, register1, register2, offset, mode):
        # Single Data Transfer:
        self.lc = LocationCounter
        self.label = ""
        self.directive = ""
        self.condition = 0b0000
        self.inmediateOffset = 0b1
        self.indexingBit = 0b0
        self.upDownBit = 0b0
        self.byteWordBit = 0b0
        self.writeBackBit = 0b0
        self.loadStoreBit = 0b0
        self.baseRegister = register1
        self.sourceDestinationRegister = register2
        if self.inmediateOffset == 0b0 and offset < 4095:
            self.offset = offset # 0b000000000000
        elif self.inmediateOffset == 0b1 and offset in registers:
            self.offset = {
                "shift": 0b00000000,
                "offsetRegister": offset
            }
        # self.comment = ""
        self.mode = mode
        self.displacement = 0b0000000000

    def get_list(self):
        return [self.label, self.directive, self.condition, self.inmediateOffset, self.indexingBit, self.upDownBit, self.byteWordBit, self.writeBackBit, self.loadStoreBit, self.baseRegister, self.sourceDestinationRegister, self.offset, self.mode, self.displacement]

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
    # ['LOOP', '', 0, 1, 0, 0, 0, 0, 0, 'R7', 'R3', 'R4', 'User mode', 0]
    # ['VAR', '', 'EOR', 'R5', 'R6', {'operand': 'R7', 'identificationBits': 0}, '', 'User mode', 0]
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
                            resultado = assembleLine() # Hace la operacion
                            return resultado
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

def changeRegisterValue(register, value):
    if(value <= 4294967295 & value >= 0):
        registers[register] = value
    else:
        print("El valor del registro no es valido")
    
    return registers[register]

instructions = []
def lexicalScanRoutine(object_code): 
    counter = 0
    LocationCounter = counter

    # object_code = [["LOOP:", "AND", "R1"]]

    for line in object_code:
        for first_column in line:
            for key in OpCodeTable:
                for operation in OpCodeTable[key]:
                    if first_column == operation and key == 0:
                        type = "DATA"
                    elif first_column == operation and key == 1:
                        type = "MUL"
                    elif first_column == operation and key == 2:
                        type = "SDT"
                    
                                
        line_index = object_code.index(line)
        # Inicializacion de la instruccion
        # self, LocationCounter, mnemonic, register1, register2, operand2, mode
        instructionDATA = instructionDataProcessing(LocationCounter + object_code.index(line), "AND", "", "", "", mode[0])
        # LocationCounter, register1, register2, register3, register4, mode
        instructionMUL = instructionMultiply(LocationCounter + object_code.index(line), "R1", "", "", "", mode[0])
        # self, LocationCounter, register1, register2, offset, mode
        instructionSDT = instructionSingleData(LocationCounter + object_code.index(line), "", "", "R3", mode[0])

        for column in line:
            column_index = object_code[line_index].index(column)
            # Label
            if ":" in object_code[line_index][0]:
                # Buscar el Label en el SymbolTable
                if len(SymbolTable) > 0:
                    for symbol in SymbolTable:
                        if object_code[line_index][0] in SymbolTable[symbol][0]:
                            print("El Label esta registrado en el Symbol Table")
                            break
                        else:
                            object_code[line_index][0] = object_code[line_index][0].split(":")
                            instructionDATA.label = object_code[line_index][0]
                            instructionMUL.label = object_code[line_index][0]
                            instructionSDT.label = object_code[line_index][0]
                elif len(SymbolTable) == 0:
                    object_code[line_index][0] = object_code[line_index][0].split(":")[0]
                    instructionDATA.label = object_code[line_index][0]
                    instructionMUL.label = object_code[line_index][0]
                    instructionSDT.label = object_code[line_index][0]
            
            # Directive: Realizar modificaciones
            for directive in DirectiveTable:
                if object_code[line_index][column_index] is directive and column_index == 0:
                    instructionDATA.directive = object_code[line_index][0]
                    instructionMUL.directive = object_code[line_index][0]
                    instructionSDT.directive = object_code[line_index][0]
                elif object_code[line_index][column_index] is directive and column_index == 1 and instructionDATA.label:
                    instructionDATA.directive = object_code[line_index][1]
                    instructionMUL.directive = object_code[line_index][1]
                    instructionSDT.directive = object_code[line_index][1]

            def insertOperandRegister(register, value):
                if value in registers:
                    register = value
                    return register
            
            if type == "DATA":
                # Mnemonic
                for operation in OpCodeTable[0]:
                    if column_index >= 0 and column_index <= 3 and object_code[line_index][column_index] == operation:
                        instructionDATA.mnemonic = object_code[line_index][column_index]

                # OperandRegister
                # Se bugea porque ya tiene un valor asignado y se camia por el siguiente registro
                if len(instructionDATA.mnemonic) > len("") and object_code[line_index][column_index] in registers and len(instructionDATA.operandRegister) == len(""):
                    instructionDATA.operandRegister = object_code[line_index][column_index]
                    print(instructionDATA.operandRegister)
                    index_operand1 = column_index
                
                # destinationRegister
                if instructionDATA.operandRegister and index_operand1 + 1 != None:
                    if object_code[line_index][index_operand1 + 1] in registers:
                        instructionDATA.destinationRegister = object_code[line_index][index_operand1 + 1]
                        index_destinationRegister = index_operand1 + 1
                
                # Operand2
                if instructionDATA.destinationRegister and index_destinationRegister + 1 != None:
                    if object_code[line_index][index_destinationRegister + 1] in registers and "#" in object_code[line_index][index_destinationRegister + 1] and object_code[line][index_destinationRegister + 1] != instructionDATA.operand1 and object_code[line][index_destinationRegister + 1] != instructionDATA.destinationRegister:
                        instructionDATA.operand2["operand"] = object_code[line_index][index_destinationRegister + 1]

                    elif object_code[line_index][index_destinationRegister + 1] in registers:
                        instructionDATA.operand2["operand"] = object_code[line_index][index_destinationRegister + 1]
                    
                    # Identificacion bit
                    for symbol in SymbolTable:
                        while symbol:
                            if symbol.name == object_code[line_index][index_destinationRegister + 1]:
                                instructionDATA.operand2["identificacionBits"] = 0b01
                            symbol = symbol.next

                # Comment
                if ";" in object_code[line_index][column_index]:
                    object_code[line_index][column_index] = object_code[line_index][column_index].split(";")
                    instructionDATA.comment = object_code[line_index][column_index + 1]

                # Mode (Activado mediante opciones del software del simulador)
                instructionDATA.mode = mode[0]
                        
                LocationCounter = LocationCounter + 1
                print(instructionDATA.get_info())
                print(column_index)
                print(len(range(len(line))))


                if instructionDATA.destinationRegister in registers:
                    instructions.append(instructionDATA.get_list())
                    break
                else:
                    print("Hubo un error")

            elif type == "MUL":

                if column_index >= 0 and column_index <= 3:
                    instructionMUL.destinationRegister = insertOperandRegister(instructionMUL.destinationRegister, object_code[line_index][column_index])

                if instructionMUL.destinationRegister:
                    instructionMUL.operandRegister1 = insertOperandRegister(instructionMUL.operandRegister1, object_code[line_index][column_index + 1])

                if instructionMUL.operandRegister1:
                    instructionMUL.operandRegister2 = insertOperandRegister(instructionMUL.operandRegister2, object_code[line_index][column_index + 2])
                
                if instructionMUL.operandRegister2:
                    instructionMUL.operandRegister3 = insertOperandRegister(instructionMUL.operandRegister3, object_code[line_index][column_index + 4])

                # Comment
                if ";" in object_code[line_index][column_index]:
                    object_code[line_index][column_index] = object_code[line_index][column_index].split(";")
                    instructionMUL.comment = object_code[line_index][column_index + 1]

                print(instructionMUL.get_info())

                if instructionMUL.destinationRegister in registers:
                    instructions.append(instructionMUL.get_list())
                    break

            elif type == "SDT":
                if column_index >= 0 and column_index <= 3:
                    instructionSDT.baseRegister = insertOperandRegister(instructionSDT.baseRegister, object_code[line_index][column_index])

                if instructionSDT.baseRegister:
                    instructionSDT.sourceDestinationRegister = insertOperandRegister(instructionSDT.sourceDestinationRegister, object_code[line_index][column_index + 1])

                if instructionSDT.sourceDestinationRegister:
                    instructionSDT.offset = insertOperandRegister(instructionSDT.offset, object_code[line_index][column_index + 2])

                if instructionSDT.baseRegister in registers:
                    instructions.append(instructionSDT.get_list())
                    break
            else:
                print("¡Error, defina un mnemonic!")

# 1. Realizar el ensamblaje de cada instruccion
# 2. Realizar el ensamblaje de una instruccion en cada simbolo
# 3.- Microoperaciones y respuesta en un diccionario en un array bidimensional
# cargar en memoria -> repetir con la siguiente instruccion
# 

def assembleLine(ins):
    pre_fetch = [["RAM", "MMU"], ["MMU", "CACHE"], ["CACHE", "REGISTER"]]
    fetch = [["IP", "MAR"], ["W", "MDR"], ["MDR", "IR"], ["IP+1", "IP"], ["0", "F"]]

    if ins[index.mnemonic] == "AND":
        operationAND()
    elif ins.mnemonic == "EOR":
        operationEOR()
    elif ins.mnemonic == "ORR":
        operationORR()
    else:
        pass

def operationAND(instruction):
    execute = [["DATA", "MAR"]]
    # 1101
    # 1011
    # 1001
    result = instruction[4] & instruction[6]
    return microoperations, result

def operationEOR():
    return microoperations, result

def operationORR():
    return microoperations, result

def OnePassAssembler():
    # Resolucion de multiply-defined labels
    #if(instruction.label == SymbolTable.label):
    #    append("name", NUL, "MTDF")
    
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
                comando = searchSymbolTable(ins, "D")
            else:
                # A Symbol used
                if ins.operand2["operand"] == type("string"):
                    comando = searchSymbolTable(ins, "S")



    return commandos

OnePassAssembler()
