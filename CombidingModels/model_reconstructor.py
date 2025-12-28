import math
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense, Dropout, Input

# ==================== ФУНКЦИИ ДЛЯ ЧТЕНИЯ ФАЙЛОВ ====================

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
    """Класс для отслеживания состояний"""
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
            DopValue.clear()
            
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

def read_dense_file(filename="outputDense.txt"):
    """Чтение и обработка файла для плотных слоев (Dense)"""
    bias = []
    weights = []
    resArr = []
    biases = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as infile:
            line = ""
            DopValue.clear()
            
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
    
    if bias:
        biases.append(bias.copy())
        bias.clear()
        DopValue.clear()
    
    return resArr, biases

# ==================== ФУНКЦИЯ ДЛЯ СОЗДАНИЯ МОДЕЛИ ====================

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense, Concatenate

from tensorflow.keras.models import save_model

import tensorflow as tf
from tensorflow.keras import layers, models

import numpy as np
from tensorflow.keras import layers, models

def build_model_from_files(conv1_weights, conv1_biases,
                           conv2_weights, conv2_biases,
                           dense_weights, dense_biases):
    import numpy as np
    from tensorflow.keras import layers, models

    # Определяем вход
    input_layer = layers.Input(shape=(224, 224, 3))

    # ===================== Первая ветка Conv =====================
    x1 = input_layer
    for i, (w_list, b_list) in enumerate(zip(conv1_weights, conv1_biases)):
        w = np.array(w_list)
        b = np.array(b_list)
        filters = b.shape[0]
        kernel_size = w.shape[:2]
        x1 = layers.Conv2D(filters=filters, kernel_size=kernel_size,
                           padding='same', activation='relu', name=f'conv1_{i}')(x1)
        x1 = layers.MaxPooling2D()(x1)

    # ===================== Вторая ветка Conv =====================
    x2 = input_layer
    for i, (w_list, b_list) in enumerate(zip(conv2_weights, conv2_biases)):
        w = np.array(w_list)
        b = np.array(b_list)
        filters = b.shape[0]
        kernel_size = w.shape[:2]
        x2 = layers.Conv2D(filters=filters, kernel_size=kernel_size,
                           padding='same', activation='relu', name=f'conv2_{i}')(x2)
        x2 = layers.MaxPooling2D()(x2)

    # ===================== Конкатенация и пуллинг =====================
    x = layers.Concatenate()([x1, x2])
    x = layers.GlobalAveragePooling2D()(x)

    # ===================== Dense слои =====================
    for i, (w_list, b_list) in enumerate(zip(dense_weights, dense_biases)):
        w = np.array(w_list)
        b = np.array(b_list)
        units = b.shape[0]
        x = layers.Dense(units, activation='relu', name=f'dense_{i}')(x)

    # Создаем модель
    model = models.Model(inputs=input_layer, outputs=x)

    # ===================== Установка весов =====================
    # Conv ветка 1
    conv_layers1_model = [layer for layer in model.layers if layer.name.startswith('conv1_')]
    for layer, w_list, b_list in zip(conv_layers1_model, conv1_weights, conv1_biases):
        w = np.array(w_list)
        b = np.array(b_list)
        if layer.weights[0].shape == w.shape and layer.weights[1].shape == b.shape:
            layer.set_weights([w, b])
        else:
            print(f"⚠️ Размеры не совпадают, вес не установлен для слоя {layer.name}")

    # Conv ветка 2
    conv_layers2_model = [layer for layer in model.layers if layer.name.startswith('conv2_')]
    for layer, w_list, b_list in zip(conv_layers2_model, conv2_weights, conv2_biases):
        w = np.array(w_list)
        b = np.array(b_list)
        if layer.weights[0].shape == w.shape and layer.weights[1].shape == b.shape:
            layer.set_weights([w, b])
        else:
            print(f"⚠️ Размеры не совпадают, вес не установлен для слоя {layer.name}")

    # Dense слои
    dense_layers_model = [layer for layer in model.layers if layer.name.startswith('dense_')]
    for layer, w_list, b_list in zip(dense_layers_model, dense_weights, dense_biases):
        w = np.array(w_list)
        b = np.array(b_list)
        if layer.weights[0].shape == w.shape and layer.weights[1].shape == b.shape:
            layer.set_weights([w, b])
        else:
            print(f"⚠️ Размеры не совпадают, вес не установлен для слоя {layer.name}")

    return model




# ==================== ОСНОВНОЙ КОД ====================

# ==================== ОСНОВНОЙ КОД ====================

if __name__ == "__main__":
    # 1️⃣ Загружаем веса свёрточных слоев и смещений
    conv_layers1, conv_biases1 = read_conv_file("output.txt")      # Первая ветка
    conv_layers2, conv_biases2 = read_conv_file("output1.txt")     # Вторая ветка

    # 2️⃣ Загружаем Dense слои и смещения
    dense_weights, dense_biases = read_dense_file("outputDense.txt")

    # 3️⃣ Проверяем, что данные загружены
    if conv_layers1 and conv_layers2 and dense_weights:
        print("📊 Данные загружены успешно:")
        print(f"   Conv ветка 1: {len(conv_layers1)} слоев")
        print(f"   Conv ветка 2: {len(conv_layers2)} слоев")
        print(f"   Dense слоев: {len(dense_weights)}")

        # 4️⃣ Создаём модель с "пустыми" весами
        model = build_model_from_files(
            conv_layers1, conv_biases1,
            conv_layers2, conv_biases2,
            dense_weights, dense_biases,
        )

        # 5️⃣ Ставим веса вручную с проверкой формы
        conv_layers_model = [layer for layer in model.layers if isinstance(layer, layers.Conv2D)]
        dense_layers_model = [layer for layer in model.layers if isinstance(layer, layers.Dense)]

        # Conv ветка 1
        for i, (layer, w_list, b_list) in enumerate(zip(conv_layers_model[:len(conv_layers1)], conv_layers1, conv_biases1)):
            w_array = np.array(w_list)
            b_array = np.array(b_list)
            print(f"[Conv1 Layer {i}] Ожидаемая форма: {layer.weights[0].shape}, Форма из файла: {w_array.shape}")
            print(f"[Conv1 Layer {i}] Bias форма: {b_array.shape}")
            if layer.weights[0].shape == w_array.shape and layer.weights[1].shape == b_array.shape:
                layer.set_weights([w_array, b_array])
            else:
                print(f"⚠️ Размеры не совпадают, вес не установлен для слоя {i}")

        # Conv ветка 2
        for i, (layer, w_list, b_list) in enumerate(zip(conv_layers_model[len(conv_layers1):], conv_layers2, conv_biases2)):
            w_array = np.array(w_list)
            b_array = np.array(b_list)
            print(f"[Conv2 Layer {i}] Ожидаемая форма: {layer.weights[0].shape}, Форма из файла: {w_array.shape}")
            print(f"[Conv2 Layer {i}] Bias форма: {b_array.shape}")
            if layer.weights[0].shape == w_array.shape and layer.weights[1].shape == b_array.shape:
                layer.set_weights([w_array, b_array])
            else:
                print(f"⚠️ Размеры не совпадают, вес не установлен для слоя {i}")

        # Dense слои
        for i, (layer, w_list, b_list) in enumerate(zip(dense_layers_model, dense_weights, dense_biases)):
            w_array = np.array(w_list)
            b_array = np.array(b_list)
            print(f"[Dense Layer {i}] Ожидаемая форма: {layer.weights[0].shape}, Форма из файла: {w_array.shape}")
            print(f"[Dense Layer {i}] Bias форма: {b_array.shape}")
            if layer.weights[0].shape == w_array.shape and layer.weights[1].shape == b_array.shape:
                layer.set_weights([w_array, b_array])
            else:
                print(f"⚠️ Размеры не совпадают, вес не установлен для Dense слоя {i}")

        # 6️⃣ Сохраняем модель
        model.save("reconstructed_model.h5")
        print("✅ Модель успешно создана и сохранена!")

        # 7️⃣ Структура модели
        print("\n📊 Структура модели:")
        model.summary()

        # 8️⃣ Быстрый тест модели
        print("\n🧪 Быстрый тест:")
        test_input = np.random.randn(1, 224, 224, 3).astype(np.float32)
        output = model.predict(test_input, verbose=0)
        print(f"   Вход: {test_input.shape}")
        print(f"   Выход: {output[0]}")

    else:
        print("❌ Ошибка: не удалось загрузить все необходимые данные для создания модели")
