# from views import counter

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

registers = {"R1": 50, "R2": 5, "R3": 10, "R4": 5, "R5": 6, "R6": 3, "R7": 8, "R8": 0, "R9": 0, "R10": 0,
                 "R11": 0, "R12": 0, "R13": 0, "R14": 0}

mode = ["User mode", "FIQ mode", "IRQ mode", "Supervisor mode", "Abort mode", "Undefined mode"]

# Table Search Procedures:
OpCodeTable = {
    # Data Processing: Operaciones logicas
    0 : {
        "AND": {
            "OpCode": bin(0b0000),
            "type": "RR",
            "length": 5,
        }, 
        "EOR": {
            "OpCode": bin(0b0001),
            "type": "RR",
            "length": 5,
        },
        "ORR": {
            "OpCode": bin(0b0010),
            "type": "RR",
            "length": 2,
        },
        "ADC": {
            "OpCode": bin(0b0011),
            "type": "RR",
            "length": 5
        },
        "SBC": {
            "OpCode": bin(0b0100),
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

# Entendible, Enfocarse en la reusabilidad. Mal si son dificiles de modificar
# 1. Definir variables e insertarlo en la clase (permite definir if's, aunque no declarar los tipos)
# Comentario en la documentacion:
# La principal razon por la que se aplica una clase en lugar de un diccionario es debido a que permite declarar
# tipos en cada clase distinta que son instances variables que no comparten el mismo valor, aparte de que permite
# mas funcionalidades tales como poder colocar condicionales

class instructionDataProcessing:
    def __init__(self, LocationCounter, label, directive, mnemonic, operandRegister, destinationRegister, operand2, comment, mode):
        # Data Processing:
        self.lc: int = LocationCounter
        self.label: str = label
        self.directive: str = directive
        self.inmediateOperand: bin = 0b1 # Si self.operand2: self.inmediateOperand = 0b0, indicando que existe
        if mnemonic in OpCodeTable[0]:
            self.mnemonic: bin = bin(index(OpCodeTable[0], mnemonic))
        self.conditionCode: bin = 0b0 # Si set condition code (1000, 1001, 1010, 1011 entonces es 1, de otra manera es 0)
        if operandRegister in registers:
            self.operandRegister: bin = operandRegister # Siempre sera un registro de donde provenga el operando 1
        if destinationRegister:
            self.destinationRegister: bin = destinationRegister # Siempre sera un registro destino
        if operand2 != operandRegister and operand2 != destinationRegister:
            if operand2 in registers: # Siempre sera el operando 2
                self.operand2 = {
                    'Shift': {
                        'Shift amount': 0b00000,
                        'Shift type': 0b00
                    },
                    'operand': operand2,
                    'identificationBits': 0b00
                }
            elif type(operand2) is type(0b0):
                if operand2 <= 0b11111111:
                    self.operand2 = {
                        'Rotate': {
                            'Shift amount': 0b00000,
                            'Shift type': 0b00
                        },
                        'operand': bin(operand2),
                        'identificationBits': 0b00
                    }
            elif "#" in operand2:
                operand2 = int(operand2.split("#")[1])
                if operand2 <= 0b11111111:
                    self.operand2 = {
                        'Rotate': {
                            'Shift amount': 0b00000,
                            'Shift type': 0b00
                        },
                        'operand': bin(operand2),
                        'identificationBits': 0b00
                    }
            # ESTA PARTE ES IMPORTANTE, DEBIDO A QUE SE TRATA DE UN SIMBOLO
            elif type(operand2) is type("string") and operand2 not in registers:
                self.operand2 = {
                    'operand': operand2,
                    'identificationBits': 0b01
                }
            else:
                print("El operando debe ser valido")
        self.comment: str = comment
        self.mode = mode
        self.displacement = 0b0000000000

        for symbol in SymbolTable:
            while symbol:
                if symbol.name == self.operand2['operand']:
                    self.identificationBits = 0b01
                    symbol = symbol.next
            if index(SymbolTable, symbol) == len(range(len(SymbolTable))) - 1:
                    self.identificationBits = 0b00

        # if(len(self.label) >= 8):
        #    for letra in abecedario:
        #        if(str(self.label)[0] != letra):
        #            print("El label no es valido")
                
        # if(self.displacement > 127 & self.displacement < 0):
        # print("El displacement no es valido")

    def get_list(self):
        return {'label': self.label, 'directive': self.directive, 'mnemonic': self.mnemonic, 'operandRegister': self.operandRegister, 'destinationRegister': self.destinationRegister, 'operand2': self.operand2, 'comment': self.comment, 'mode': self.mode, 'displacement': self.displacement}

    def get_info(self):
        return f"Information: {self.label}, {self.directive}, {self.mnemonic}, {self.operandRegister}, {self.destinationRegister}, {self.operand2}, {self.comment}, {self.mode}, {self.displacement}"

# Se tiene que realizar las condicionales
class instructionMultiply:
    def __init__(self, LocationCounter, label, register1, register2, register3, register4, comment, mode):
        # Multiply - Multiply Accumulate:
        self.lc = LocationCounter
        self.label = label
        self.directive = ""
        self.condition = 0b0000
        self.accumulate = 0b1
        self.conditionCode = 0b0 # Si set condition code (1000, 1001, 1010, 1011 entonces es 1, de otra manera es 0)
        self.destinationRegister = register1 # Siempre sera un registro destino
        self.operandRegister1 = register2
        self.operandRegister2 = register3
        self.operandRegister3 = register4
        self.comment = comment
        self.mode = mode
        self.displacement = 0b0000000000
    
    def get_list(self):
        return [self.label, self.directive, self.condition, self.accumulate, self.conditionCode, self.destinationRegister, self.operandRegister1, self.operandRegister2, self.operandRegister3, self.comment, self.mode, self.displacement]

    def get_info(self):
        return f"Information: {self.label}, {self.directive}, {self.condition}, {self.accumulate}, {self.conditionCode}, {self.destinationRegister}, {self.operandRegister1}, {self.operandRegister2}, {self.operandRegister3}, {self.comment}, {self.mode}, {self.displacement}"

# Se tiene que realizar las condicionales
class instructionSingleData:
    def __init__(self, LocationCounter, label, register1, register2, offset, comment, mode):
        # Single Data Transfer:
        self.lc = LocationCounter
        self.label = label
        self.directive = ""
        self.condition = 0b0000
        self.inmediateOffset = 0b1
        self.indexingBit = 0b0
        self.upDownBit = 0b0
        self.byteWordBit = 0b0
        self.writeBackBit = 0b0
        self.loadStoreBit = 0b0
        self.baseRegister = register2
        self.sourceDestinationRegister = register1
        if self.inmediateOffset == 0b0 and offset < 4095:
            self.offset = offset # 0b000000000000
        elif self.inmediateOffset == 0b1 and offset in registers:
            self.offset = {
                "shift": 0b00000000,
                "offsetRegister": offset
            }
        self.comment = comment
        self.mode = mode
        self.displacement = 0b0000000000

    def get_list(self):
        return [self.label, self.directive, self.condition, self.inmediateOffset, self.indexingBit, self.upDownBit, self.byteWordBit, self.writeBackBit, self.loadStoreBit, self.baseRegister, self.sourceDestinationRegister, self.offset, self.comment, self.mode, self.displacement]

    def get_info(self):
        return f"Information: {self.label}, {self.directive}, {self.condition}, {self.inmediateOffset}, {self.indexingBit}, {self.upDownBit}, {self.byteWordBit}, {self.writeBackBit}, {self.loadStoreBit}, {self.baseRegister}, {self.sourceDestinationRegister}, {self.offset}, {self.comment}, {self.mode}, {self.displacement}"

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
                            microoperations, result = assembleLine(ins) # Hace la operacion
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
                else:
                    microoperations, result = assembleLine(ins)

    return microoperations, result    
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
    line_code = []
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
    global type_line
    counter = 0
    LocationCounter = counter
    

    # object_code = [["LOOP:", "AND", "R1"]]

    for line in object_code:
        advert = 0
        advert_MUL = 0
        advert_SDT = 0

        for first_column in line:
            for key in OpCodeTable:
                for operation in OpCodeTable[key]:
                    if first_column == operation and key == 0:
                        type_line = "DATA"
                    elif first_column == operation and key == 1:
                        type_line = "MUL"
                    elif first_column == operation and key == 2:
                        type_line = "SDT"
                    else:
                        Exception("¡Error!")
                     
        line_index = object_code.index(line)

        for column in line:
            column_index = object_code[line_index].index(column)

            def insertLabel():
                if ":" in object_code[line_index][0]:
                    # Buscar el Label en el SymbolTable
                    if len(SymbolTable) > 0:
                        for symbol in SymbolTable:
                            if object_code[line_index][0] in SymbolTable[symbol][0]:
                                print("El Label esta registrado en el Symbol Table")
                                break
                            else:
                                object_code[line_index][0] = object_code[line_index][0].split(":")
                                label = object_code[line_index][0]
                                return label
                    elif len(SymbolTable) == 0:
                        object_code[line_index][0] = object_code[line_index][0].split(":")[0]
                        label = object_code[line_index][0]
                        return label
                else:
                    print("No hay un label en la linea de codigo objetivo")
                    label = None
                    return label
                            
            def insertDirective(label=None):
                for directive in DirectiveTable:
                    if object_code[line_index][column_index] is directive and column_index == 0:
                        directive_line = object_code[line_index][0]
                        return directive_line
                    elif object_code[line_index][column_index] is directive and column_index == 1 and label != None:
                        directive_line = object_code[line_index][1]
                        return directive_line

            def insertOperandRegister(value):
                if value in registers:
                    return value
            
            if type_line == "DATA":
                #Label
                if 'label' not in locals():
                    label = insertLabel()
                    if label != None:
                        if column_index < len(line) - 1:
                            continue
                
                # Directive
                if label == None and 'directive' not in locals():
                    directive = insertDirective()
                    if directive != None:
                        if column_index < len(line) - 1:
                            continue
                else:
                    directive = insertDirective(label)
                                
                # Mnemonic
                if 'mnemonic' not in locals():
                    for operation in OpCodeTable[0]:
                        if column_index >= 0 and column_index <= 3 and column == operation:
                            mnemonic = column
                            break
                    if column_index < len(line) - 1:
                        continue
                
                # OperandRegister
                if 'mnemonic' in locals() and 'operandRegister' not in locals() or operandRegister == None:
                    operandRegister = column
                    if column_index < len(line) - 1:
                        continue
                else:
                    Exception("Mnemonic no ha sido definido")
                
                # destinationRegister
                if 'operandRegister' in locals() and 'destinationRegister' not in locals():
                    destinationRegister = column
                    if column_index < len(line) - 1:
                        continue
                else:
                    Exception("destinationRegister no ha sido definido")
                
                # Operand2
                if 'destinationRegister' in locals() and 'operand2' not in locals():
                    if ";" in column:
                        column = column.split(";")[0]
                        operand2 = column
                        advert = 1
                        continue
                    else:
                        operand2 = column
                        if column_index < len(line) - 1:
                            continue
                else:
                    Exception("operand2 no ha sido definido")

                if advert == 1:
                    comment = column
                else:
                    comment = ""

                if column_index == len(line) - 1:
                    instructionDATA = instructionDataProcessing(LocationCounter + object_code.index(line), label, directive, mnemonic, operandRegister, destinationRegister, operand2, comment, mode[0])
                    instructions.append(instructionDATA)
                    del label, directive, mnemonic, operandRegister, destinationRegister, operand2, comment
                else:
                    print("Calculando...")

            elif type_line == "MUL":
                # Label
                if 'label' not in locals():
                    label = insertLabel()
                    if label != None:
                        continue

                if column_index >= 0 and column_index <= 3 and 'destinationRegister' not in locals() or destinationRegister == None:
                    destinationRegister = insertOperandRegister(column)
                    if column_index < len(line) - 1:
                        continue
                
                if 'destinationRegister' in locals() and 'operandRegister1' not in locals() and destinationRegister != None:
                    operandRegister1 = insertOperandRegister(column)
                    if column_index < len(line) - 1:
                        continue

                if 'operandRegister1' in locals() and 'operandRegister2' not in locals():
                    operandRegister2 = insertOperandRegister(column)
                    if column_index < len(line) - 1:
                        continue
                
                if 'operandRegister2' in locals() and 'operandRegister3' not in locals():
                    if ";" in column:
                        column = column.split(";")[0]
                        operandRegister3 = insertOperandRegister(column)
                        advert_MUL = 1
                        if column_index < len(line) - 1:
                            continue
                        elif operandRegister3 == None:
                            raise TypeError("No existe un operandRegister3")
                    else:
                        operandRegister3 = insertOperandRegister(column)
                        if column_index < len(line) - 1:
                            continue
                else:
                    Exception("No se ha definido un operandRegister3")

                if advert_MUL == 1:
                    comment = column
                else:
                    comment = ""
                
                if column_index == len(line) - 1:
                    instructions.append(instructionMultiply(LocationCounter + object_code.index(line), label, destinationRegister, operandRegister1, operandRegister2, operandRegister3, comment, mode[0]))

            elif type_line == "SDT":
                # Label
                if 'label' not in locals():
                    label = insertLabel()
                    if label != None:
                        continue

                if column_index >= 0 and column_index <= 3 and 'baseRegister' not in locals() or baseRegister == None:
                    baseRegister = insertOperandRegister(column)
                    continue

                if 'baseRegister' in locals() and 'sourceDestinationRegister' not in locals():
                    sourceDestinationRegister = insertOperandRegister(column)
                    continue

                if 'sourceDestinationRegister' in locals() and 'offset' not in locals():
                    if ";" in column:
                        column = column.split(";")[0]
                        offset = insertOperandRegister(column)
                        advert_SDT = 1
                        if column_index < len(line) - 1:
                            continue
                        elif offset == None:
                            raise TypeError("No se ha definido offset")
                    else:
                        offset = insertOperandRegister(column)
                        continue

                if advert_SDT == 1:
                    comment = column
                else:
                    comment = ""

                if column_index == len(line) - 1:
                    instructions.append(instructionSingleData(LocationCounter + object_code.index(line), label, baseRegister, sourceDestinationRegister, offset, comment, mode[0]))
                    break
            else:
                print("¡Error, defina un mnemonic!")
        
        LocationCounter = LocationCounter + 1

# cargar en memoria -> repetir con la siguiente instruccion 

def assembleLine(ins):
    pre_fetch = [["RAM", "MMU"], ["MMU", "CACHE"], ["CACHE", "REGISTER"]]
    fetch = [["IP", "MAR"], ["W", "MDR"], ["MDR", "IR"], ["IP+1", "IP"], ["0", "F"]]

    print("ins2: ", ins.get_info())

    if hasattr(ins, 'operand2'):
        if ins.mnemonic in OpCodeTable[0]['AND']['OpCode']:
            microoperations, result = operationAND(ins)
        elif ins.mnemonic in OpCodeTable[0]['EOR']['OpCode']:
            microoperations, result = operationEOR(ins)
        elif ins.mnemonic in OpCodeTable[0]['ORR']['OpCode']:
            microoperations, result = operationORR(ins)
        elif ins.mnemonic in OpCodeTable[0]['ADC']['OpCode']:
            microoperations, result = operationADC(ins)
        elif ins.mnemonic in OpCodeTable[0]['SBC']['OpCode']:
            microoperations, result = operationSBC(ins)
    elif hasattr(ins, 'accumulate'):
        if ins.accumulate == 0b0:
            microoperations, result = operationMUL(ins)
        elif ins.accumulate == 0b1:
            microoperations, result = operationMLA(ins)
    elif hasattr(ins, 'loadStoreBit'):
        if ins.loadStoreBit == 0b0:
            microoperations, result = operationSTR(ins)
        elif ins.loadStoreBit == 0b1:
            microoperations, result = operationLDR(ins)

    return microoperations, result

def operationAND(ins):
    microoperations = [[f"DATA", f"MAR"], [f"W", f"MDR"], [f"MDR AND {ins.destinationRegister}", f"AC"]]
    
    registers[ins.destinationRegister] = registers[ins.operandRegister] & registers[ins.operand2['operand']]
    
    result = bin(registers[ins.destinationRegister])

    return microoperations, result

def operationEOR(ins):
    microoperations = [[f"DATA", f"MAR"], [f"W", f"MDR"], [f"MDR EOR {ins.destinationRegister}", f"AC"]]

    registers[ins.destinationRegister] = registers[ins.operandRegister] ^ registers[ins.operand2['operand']]

    result = registers[ins.destinationRegister]

    return microoperations, result

def operationORR(ins):
    microoperations = [[f"DATA", f"MAR"], [f"W", f"MDR"], [f"MDR OR {ins.destinationRegister}", f"AC"]]

    registers[ins.destinationRegister] = registers[ins.operandRegister] | registers[ins.operand2['operand']]

    result = registers[ins.destinationRegister]

    return microoperations, result

def operationADC(ins):
    # microoperations = [[f"DATA", f"MAR"], [f"W", f"MDR"], [f"MDR + {ins.destinationRegister} + {Carry}", f"AC"]]
    microoperations = [[f"DATA", f"MAR"], [f"W", f"MDR"], [f"MDR + {ins.destinationRegister} + Carry", f"AC"]]

    """"
    a = int(format(registers[ins.operandRegister], 'b').zfill(32), 2)
    b = int(format(registers[ins.operand2['operand']], 'b').zfill(32), 2)
    while (a != 0 and b != 0):
        withoutcarry = a ^ b
        carry = (a & b) << 1
        a = withoutcarry
        b = carry
    if a > 0:
        sum = bin(a).zfill(32)
    elif b > 0:
        sum = bin(b).zfill(32)
    """

    a = format(registers[ins.operandRegister], 'b').zfill(32)
    b = format(registers[ins.operand2['operand']], 'b').zfill(32)

    a_list = list(a)
    b_list = list(b)
    result_list = []

    iteration = 0
    for bit1, bit2 in reversed(list(zip(a_list, b_list))):
        bit1 = int(bit1, 2)
        bit2 = int(bit2, 2)
        if iteration == 0:
            # Para el primer bit de a y b (Estos bits son del semisumador)
            sum_ss = bit1 ^ bit2
            carry_ss = bit1 & bit2
            result_list.insert(0, str(sum_ss))
        elif iteration == 1:
            # Para el siguiente bit de a y b del carry ss (Estos bits son del sumador completo)
            sum_sc = (bit1 & ~bit2 & ~carry_ss) | (~bit1 & bit2 & ~carry_ss) | (~bit1 & ~bit2 & carry_ss) | (bit1 & bit2 & carry_ss) 
            carry_sc = (bit1 & bit2) | (bit1 & carry_ss) | (bit2 & carry_ss)
            result_list.insert(0, str(sum_sc))
        elif iteration >= 2:
            # Para el siguiente bit de a y b (loop while) del carry_sc (Sumador completo tradicional)
            sum_sc = (bit1 & ~bit2 & ~carry_sc) | (~bit1 & bit2 & ~carry_sc) | (~bit1 & ~bit2 & carry_sc) | (bit1 & bit2 & carry_sc) 
            carry_sc = (bit1 & bit2) | (bit1 & carry_sc) | (bit2 & carry_sc)
            result_list.insert(0, str(sum_sc))
        iteration = iteration + 1
    result_list = "".join(result_list)

    registers[ins.destinationRegister] = result_list

    result = registers[ins.destinationRegister]

    return microoperations, result

def operationSBC(ins):
    # microoperations = [[f"DATA", f"MAR"], [f"W", f"MDR"], [f"MDR - {ins.destinationRegister} + {Carry} - 1", f"AC"]]
    microoperations = [[f"DATA", f"MAR"], [f"W", f"MDR"], [f"MDR - {ins.destinationRegister}", f"AC"]]

    """"
    a = int(format(registers[ins.operandRegister], 'b').zfill(32), 2)
    b = int(format(registers[ins.operand2['operand']], 'b').zfill(32), 2)
    while (b != 0):
        restar = (~a) & b
        a = a ^ b
        b = restar << 1
    """

    a = format(registers[ins.operandRegister], 'b').zfill(32)
    b = format(registers[ins.operand2['operand']], 'b').zfill(32)

    a_list = list(a)
    b_list = list(b)
    result_list = []

    iteration = 0
    for bit1, bit2 in reversed(list(zip(a_list, b_list))):
        bit1 = int(bit1, 2)
        bit2 = int(bit2, 2)
        if iteration == 0:
            diff = bit1 ^ bit2
            borrow_sb = ~(bit1) & bit2
            result_list.insert(0, str(diff))
        if iteration == 1:
            diff_sc = (~(bit1) & ~(bit2) & borrow_sb) | (~(bit1) & (bit2) & ~(borrow_sb)) | (bit1 & ~(bit2) & ~(borrow_sb)) | (bit1 & bit2 & borrow_sb)
            borrow_sc = (~(bit1) & ~(bit2) & borrow_sb) | (~(bit1) & (bit2) & ~(borrow_sb)) | (~(bit1) & (bit2) & borrow_sb) | (bit1 & bit2 & borrow_sb)
            result_list.insert(0, str(diff_sc))
        if iteration >= 2:
            diff_sc = (~(bit1) & ~(bit2) & borrow_sc) | (~(bit1) & (bit2) & ~(borrow_sc)) | (bit1 & ~(bit2) & ~(borrow_sc)) | (bit1 & bit2 & borrow_sc)
            borrow_sc = (~(bit1) & ~(bit2) & borrow_sc) | (~(bit1) & (bit2) & ~(borrow_sc)) | (~(bit1) & (bit2) & borrow_sc) | (bit1 & bit2 & borrow_sc)
            result_list.insert(0, str(diff_sc))
        iteration = iteration + 1
    result_list = "".join(result_list)

    registers[ins.destinationRegister] = result_list

    result = registers[ins.destinationRegister]

    return microoperations, result

def operationMUL(ins):
    microoperations = []
    result = 1

    return microoperations, result

# En el algoritmo de Booth, los negativos se representan con complementos + 1
# El bit mas significativo (signo) no se elimina, sino simplemente se duplica cuando se hace el right shift 

def sumTwo(first, two):
    first_list = list(first)
    two_list = list(two)
    result_list = []

    iteration = 0
    for bit1, bit2 in reversed(list(zip(first_list, two_list))):
        bit1 = int(bit1, 2)
        bit2 = int(bit2, 2)
        if iteration == 0:
            # Para el primer bit de a y b (Estos bits son del semisumador)
            sum_ss = bit1 ^ bit2
            carry_ss = bit1 & bit2
            result_list.insert(0, str(sum_ss))
        elif iteration == 1:
            # Para el siguiente bit de a y b del carry ss (Estos bits son del sumador completo)
            sum_sc = (bit1 & ~bit2 & ~carry_ss) | (~bit1 & bit2 & ~carry_ss) | (~bit1 & ~bit2 & carry_ss) | (bit1 & bit2 & carry_ss)
            carry_sc = (bit1 & bit2) | (bit1 & carry_ss) | (bit2 & carry_ss)
            result_list.insert(0, str(sum_sc))
        elif iteration >= 2:
            # Para el siguiente bit de a y b (loop while) del carry_sc (Sumador completo tradicional)
            sum_sc = (bit1 & ~bit2 & ~carry_sc) | (~bit1 & bit2 & ~carry_sc) | (~bit1 & ~bit2 & carry_sc) | (bit1 & bit2 & carry_sc) 
            carry_sc = (bit1 & bit2) | (bit1 & carry_sc) | (bit2 & carry_sc)
            result_list.insert(0, str(sum_sc))
        iteration = iteration + 1
    result_list = "".join(result_list)

    return result_list

def complement_plus1(m):
    print("m:", m)
    m_list = list(m)
    count = 0
    for bit in m_list:
        if bit == '0':
            m_list[count] = '1'
        elif bit == '1':
            m_list[count] = '0'
        count = count + 1
    m_complement = ''.join(m_list)
    one_bit = format(1, 'b').zfill(32)
    
    m_complement_list = list(m_complement)
    one_bit_list = list(one_bit)
    m_negative = []

    iter1 = 0
    for bit_c, bit_one in reversed(list(zip(m_complement_list, one_bit_list))):
        bit_c = int(bit_c, 2)
        bit_one = int(bit_one, 2)
        if iter1 == 0:
            # Para el primer bit de a y b (Estos bits son del semisumador)
            sum_ss = bit_c ^ bit_one
            carry_ss = bit_c & bit_one
            m_negative.insert(0, str(sum_ss))
        elif iter1 == 1:
            # Para el siguiente bit de a y b del carry ss (Estos bits son del sumador completo)
            sum_sc = (bit_c & ~bit_one & ~carry_ss) | (~bit_c & bit_one & ~carry_ss) | (~bit_c & ~bit_one & carry_ss) | (bit_c & bit_one & carry_ss) 
            carry_sc = (bit_c & bit_one) | (bit_c & carry_ss) | (bit_one & carry_ss)
            m_negative.insert(0, str(sum_sc))
        elif iter1 >= 2:
            # Para el siguiente bit de a y b (loop while) del carry_sc (Sumador completo tradicional)
            sum_sc = (bit_c & ~bit_one & ~carry_sc) | (~bit_c & bit_one & ~carry_sc) | (~bit_c & ~bit_one & carry_sc) | (bit_c & bit_one & carry_sc) 
            carry_sc = (bit_c & bit_one) | (bit_c & carry_sc) | (bit_one & carry_sc)
            m_negative.insert(0, str(sum_sc))
        iter1 = iter1 + 1
    m_negative = "".join(m_negative)

    print("m_negative:", m_negative)
    return m_negative

def minusone_complement(P):
    print("SUCCESS ONE TWO")
    a = P
    b = format(1, 'b').zfill(len(P))

    a_list = list(a)
    b_list = list(b)
    result_list = []

    iteration = 0
    for bit1, bit2 in reversed(list(zip(a_list, b_list))):
        bit1 = int(bit1, 2)
        bit2 = int(bit2, 2)
        if iteration == 0:
            diff = bit1 ^ bit2
            borrow_sb = ~(bit1) & bit2
            result_list.insert(0, str(diff))
        if iteration == 1:
            diff_sc = (~(bit1) & ~(bit2) & borrow_sb) | (~(bit1) & (bit2) & ~(borrow_sb)) | (bit1 & ~(bit2) & ~(borrow_sb)) | (bit1 & bit2 & borrow_sb)
            borrow_sc = (~(bit1) & ~(bit2) & borrow_sb) | (~(bit1) & (bit2) & ~(borrow_sb)) | (~(bit1) & (bit2) & borrow_sb) | (bit1 & bit2 & borrow_sb)
            result_list.insert(0, str(diff_sc))
        if iteration >= 2:
            diff_sc = (~(bit1) & ~(bit2) & borrow_sc) | (~(bit1) & (bit2) & ~(borrow_sc)) | (bit1 & ~(bit2) & ~(borrow_sc)) | (bit1 & bit2 & borrow_sc)
            borrow_sc = (~(bit1) & ~(bit2) & borrow_sc) | (~(bit1) & (bit2) & ~(borrow_sc)) | (~(bit1) & (bit2) & borrow_sc) | (bit1 & bit2 & borrow_sc)
            result_list.insert(0, str(diff_sc))
        iteration = iteration + 1
    result_list = "".join(result_list)

    print("result_list: ", result_list)

    P = ~int(result_list, 2)

    return P

def operationMLA(ins):
    microoperations = [[f"DATA", f"MAR"], [f"W", f"MDR"], [f"MDR * {ins.operandRegister2}", f"AC"]]

    m = format(registers[ins.operandRegister1], 'b').zfill(32)
    m_negative = complement_plus1(m)
    r = format(registers[ins.operandRegister2], 'b').zfill(32)

    x = len(m)
    y = len(r)

    print("Length de x: ", x)

    A = m + format(0, 'b').zfill(32) + format(0, 'b')
    S = m_negative + format(0, 'b').zfill(32) + format(0, 'b')
    P = format(0, 'b').zfill(32) + r + format(0, 'b')
    print("A:", A)
    print("S:", S)
    print("P:", P)

    def shift1P(P):
        # Contar los zeros de un numero hasta que alcance uno
        remaining_MSB_zeroes = 0
        for number in P:
            if number == '0':
                remaining_MSB_zeroes = remaining_MSB_zeroes + 1
            elif number == '1':
                break        
        P = int(P, 2)
        P = P >> 1
        P = format(P, 'b')
        P = P.zfill(remaining_MSB_zeroes + len(P) + 1)
        P_list = list(P)
        P_list[0] = '1'
        P = ''.join(P_list)
        return P
    
    def shift0P(P):
        # Contar los zeros de un numero hasta que alcance uno
        remaining_MSB_zeroes = 0
        for number in P:
            if number == '0':
                remaining_MSB_zeroes = remaining_MSB_zeroes + 1
            elif number == '1':
                break
        P = int(P, 2)
        P = P >> 1
        P = format(P, 'b')
        P = P.zfill(remaining_MSB_zeroes + len(P) + 1)
        return P

    # Bug: Cuando R5 es impar, no tira el numero correcto
    # Correccion: Quitar los 33 bits mas significativos, de manera de tener los 32 bits.
    count = 0
    while(count != x + 1):
        if(P[63:] == '01'):
            P = sumTwo(P, A)
            print("Sum of P and A: ", P)
            if P[0] == '1':
                P = shift1P(P)
            elif P[0] == '0':
                P = shift0P(P)
        elif(P[63:] == '10'):
            P = sumTwo(P, S)
            print("Sum of P and S: ", P)
            if P[0] == '1':
                P = shift1P(P)
            elif P[0] == '0':
                P = shift0P(P)
        elif(P[63:] == '00'):
            if P[0] == '1':
                P = shift1P(P)
            elif P[0] == '0':
                P = shift0P(P)
        elif(P[63:] == '11'):
            if P[0] == '1':
                P = shift1P(P)
                print("shift1P", P)
            elif P[0] == '0':
                P = shift0P(P)
                print("shift0P", P)
        count = count + 1
        print("-------------------")
        print(P)

    P_list = list(P)
    value = 0
    while(value != 33):
        P_list.pop(0)
        value = value + 1
    P = ''.join(P_list)

    result = P

    registers[ins.destinationRegister] = result

    return microoperations, result

def operationSTR(ins):
    pass

def operationLDR(ins):
    ins.

microoperations_list = []
result_list = []
def OnePassAssembler(instructions):
    # Resolucion de multiply-defined labels
    #if(instruction.label == SymbolTable.label):
    #    append("name", NUL, "MTDF")

    for ins in instructions:
        # End of file
        microoperations = 0
        result = 0
        if instructions.index(ins) == len(instructions):
            scanSymbolTable()
        else:
            # Label Defined
            if ins.label != None:
                comando = searchSymbolTable(ins, "D")
            else:
                # A Symbol used?
                if hasattr(ins, 'operand2'):
                    if ins.operand2["operand"] not in registers:
                        print(1)
                        microoperations, result = searchSymbolTable(ins, "S")
                    else:
                        microoperations, result = assembleLine(ins)
                elif hasattr(ins, 'accumulate'):
                    print(2)
                    microoperations, result = assembleLine(ins)
                elif hasattr(ins, 'loadStoreBit'):
                    print(3)
                    microoperations, result = assembleLine(ins)
                else:
                    print(4)
                    microoperations, result = assembleLine(ins)
        microoperations_list.append(microoperations)
        result_list.append(result)

    return microoperations_list, result_list

# OnePassAssembler()
# Lexical Scan Routine
script = "SBC R1 R2 R3\r\nMLA R4 R5 R6 R7; comentario"
object_code = convertir(script)
# print(object_code)
lexicalScanRoutine(object_code)
print(instructions[1].get_info())
OnePassAssembler(instructions)
print(microoperations_list)
print(result_list)