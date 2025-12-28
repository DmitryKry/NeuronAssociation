import math

# Общие функции
def isNumber(char):
    """Проверяет, является ли символ цифрой"""
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return char in numbers

def inNumber(another):
    """Преобразует строку в число (аналог C++ функции)"""
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    temp = 0.0
    size = len(another)
    negativ = False
    drob = False
    part = 0
    
    # Убираем '-' и '.' из подсчета размера
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
                    temp += math.pow(10, -(part + 1)) * j
                    part += 1
                    break
                else:
                    temp += math.pow(10, (size - 2) - i) * j
                    break
    
    return -temp if negativ else temp

class DopValue:
    """Класс для отслеживания состояний (аналог struct dopValue из C++)"""
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

def read_dense_file(filename="outputDense.txt"):
    """Чтение и обработка файла для плотных слоев (Dense)"""
    bias = []
    weights = []
    resArr = []
    biases = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as infile:
            line = ""
            DopValue.clear()  # Сброс состояния
            
            while True:
                byte = infile.read(1)
                if not byte:
                    break
                
                if byte == ' ':
                    if line:
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
        print(f"Ошибка открытия файла {filename}!")
        return None, None
    
    # Добавляем последний bias, если он есть
    if bias:
        biases.append(bias.copy())
        bias.clear()
        DopValue.clear()
    
    return resArr, biases

def read_conv_file(filename="outputConv2D.txt"):
    """Чтение и обработка файла для сверточных слоев (Conv2D)"""
    features = []
    matrix = []
    biases = []
    input_tensor = []
    conv_filters = []
    conv_layers = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as infile:
            line = ""
            DopValue.clear()  # Сброс состояния
            
            for byte in infile.read():
                if byte == ' ':
                    if line:
                        features.append(inNumber(line))
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
                elif byte == '-' or byte == '.' or isNumber(byte):
                    line += byte
                    
    except FileNotFoundError:
        print(f"Ошибка открытия файла {filename}!")
        return None, None
    
    return conv_layers, biases

def print_dense_results(resArr, biases):
    """Вывод результатов для плотных слоев"""
    for i in range(len(resArr)):
        for elem in resArr[i]:
            for item in elem:
                print(f"{item} ", end='')
            print()
        print()
        
        if i < len(biases):
            for item in biases[i]:
                print(f"{item} ", end='')
            print()
        print()

def print_conv_results(conv_layers, biases):
    """Вывод результатов для сверточных слоев"""
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

def main():
    """Главная функция для тестирования обеих реализаций"""
    print("\n=== Тестирование Conv2D ===")
    conv_layers, conv_biases = read_conv_file("outputConv2D.txt")
    if conv_layers is not None:
        print_conv_results(conv_layers, conv_biases)
        
    print("=== Тестирование Dense ===")
    resArr, biases = read_dense_file("outputDense.txt")
    if resArr is not None:
        print_dense_results(resArr, biases)
    

if __name__ == "__main__":
    # Настройка кодировки для Windows
    try:
        import sys
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass
    
    main()