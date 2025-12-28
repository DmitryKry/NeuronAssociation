import math
import re

class DopValue:
    features = False
    matrix = False
    input_tensor = False
    conv_filters = False
    biases = False
    
    @staticmethod
    def clear():
        DopValue.features = False
        DopValue.matrix = False
        DopValue.input_tensor = False
        DopValue.conv_filters = False

def is_number(char):
    return char.isdigit()

def in_number(another):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    temp = 0
    size = len(another)
    
    # Убираем '-' и '.' из подсчета размера
    size -= another.count('-')
    size -= another.count('.')
    
    negativ = False
    drob = False
    part = 0
    
    for i, elem in enumerate(another):
        if elem == '-':
            negativ = True
            continue
        if elem == '.':
            drob = True
            continue
            
        for j, num in enumerate(numbers):
            if elem == num:
                if drob:
                    temp += math.pow(10, -(part + 1)) * j
                    part += 1
                    break
                else:
                    # Исправляем индексацию для позиции числа
                    pos = size - (len([c for c in another[:i] if c not in ['-', '.']]))
                    temp += math.pow(10, pos) * j
                    break
    
    return -temp if negativ else temp

def main():
    # Структуры данных аналогичные C++
    features = []
    matrix = []
    biases = []
    input_tensor = []
    conv_filters = []
    conv_layers = []
    
    source = "outputConv2D.txt"
    
    try:
        with open(source, 'r', encoding='utf-8') as infile:
            all_text = ""
            line = ""
            
            for byte in infile.read():
                all_text += byte
                
                if byte == ' ':
                    if line:
                        features.append(in_number(line))
                        if not DopValue.biases:
                            DopValue.clear()
                        line = ""
                        
                elif byte == '\n':
                    if not DopValue.features and not DopValue.biases:
                        if features:
                            matrix.append(features.copy())
                            features.clear()
                        DopValue.features = True
                        
                    elif DopValue.features and not DopValue.matrix:
                        if matrix:
                            input_tensor.append(matrix.copy())
                            matrix.clear()
                        DopValue.matrix = True
                        
                    elif DopValue.matrix and not DopValue.input_tensor:
                        if input_tensor:
                            conv_filters.append(input_tensor.copy())
                            input_tensor.clear()
                        DopValue.input_tensor = True
                        
                    elif DopValue.input_tensor and not DopValue.conv_filters:
                        if conv_filters:
                            conv_layers.append(conv_filters.copy())
                            conv_filters.clear()
                        DopValue.conv_filters = True
                        DopValue.biases = True
                        DopValue.features = False
                        
                    elif DopValue.biases and features:
                        biases.append(features.copy())
                        features.clear()
                        DopValue.clear()
                        
                    elif DopValue.biases and not features:
                        DopValue.biases = False
                        
                elif byte == '-' or byte == '.' or is_number(byte):
                    line += byte
                    
    except FileNotFoundError:
        print("Ошибка открытия файла!")
        return -1
    
    # Вывод результатов (аналогично C++ коду)
    for i in range(len(conv_layers)):
        for elem_conv_filters in conv_layers[i]:
            for elem_input_tensor in elem_conv_filters:
                for elem_matrix in elem_input_tensor:
                    for item in elem_matrix:
                        print(f"{item} ", end='')
                    print()
                print()
            print()
        print()
        
        if i < len(biases):
            for item in biases[i]:
                print(f"{item} ", end='')
            print()
        
        print()

if __name__ == "__main__":
    main()