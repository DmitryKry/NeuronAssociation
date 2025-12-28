import math
import os

def isNumber(other):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    i = 0
    while i < 10:
        if other == numbers[i]:
            i += 1
            return True
        i += 1
    return False

def inNumber(another):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    temp = 0.0
    size = len(another)
    negativ = False
    drob = False
    part = 0
    
    for elem in another:
        if elem == '-':
            size -= 1
        if elem == '.':
            size -= 1
    
    for i in range(len(another)):
        if another[i] == '-':
            negativ = True
            continue
        
        for j in range(10):
            if another[i] == '.':
                drob = True
                break
            if another[i] == numbers[j]:
                if drob:
                    temp += math.pow(10, - (part + 1)) * j
                    part += 1
                    break
                else:
                    temp += math.pow(10, (size - 2) - i) * j
                    break
    
    return temp - (temp * 2) if negativ else temp

class DopValue:
    features = False
    matrix = False
    input_tensor = False
    conv_filters = False
    biases = False
    exit = False
    
    @staticmethod
    def clear():
        DopValue.features = False
        DopValue.matrix = False
        DopValue.input_tensor = False
        DopValue.conv_filters = False

if __name__ == "__main__":
    # Настройка кодировки для Windows (аналог SetConsoleCP)
    # В Python это делается по-другому, но для совместимости оставим заглушки
    try:
        import sys
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass
    
    bias = []
    weights = []
    
    resArr = []
    biases = []
    tempArr = []
    
    source = "outputDense.txt"
    line = ""
    all_text = ""
    Dense = ""
    index = 0
    sizeDense = 5
    dense = ['D', 'e', 'n', 's', 'e']
    
    addArray = False
    roolListener = False
    cheakD = False
    degree = 0
    res = 0
    
    try:
        with open(source, 'r', encoding='utf-8') as infile:
            # Читаем побайтно (в Python читаем посимвольно)
            while True:
                byte = infile.read(1)
                if not byte:
                    break
                
                all_text += byte
                
                if byte == ' ':
                    bias.append(inNumber(line))
                    line = ""
                elif byte == '\n' and bias and not DopValue.matrix:
                    weights.append(bias.copy())
                    bias.clear()
                    DopValue.features = True
                elif byte == '\n' and weights:
                    resArr.append(weights.copy())
                    weights.clear()
                    DopValue.matrix = True
                elif byte == '\n' and bias and DopValue.matrix:
                    biases.append(bias.copy())
                    bias.clear()
                    DopValue.clear()
                elif byte == '-' or byte == '.' or isNumber(byte):
                    line += byte
                    
    except FileNotFoundError:
        print("Ошибка открытия файла!")
        exit(-1)
    
    # Добавляем последний bias, если он есть
    if bias:
        biases.append(bias.copy())
        bias.clear()
        DopValue.clear()
    
    # Вывод результатов (аналогично C++ коду)
    for i in range(len(resArr)):
        for elem in resArr[i]:
            for item in elem:
                print(item, end=' ')
            print()
        print()
        
        for item in biases[i]:
            print(item, end=' ')
        print()
        print()