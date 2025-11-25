import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

def save_model_weights_to_txt(model, output_path="model_weights_unick.txt"):
    """Сохраняет все веса и коэффициенты модели в текстовый файл."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Модель: {model.name}\n")
        f.write("=" * 80 + "\n\n")

        for layer in model.layers:
            f.write(f"Слой: {layer.name} ({layer.__class__.__name__})\n")
            weights = layer.get_weights()
            if weights:
                for i, w in enumerate(weights):
                    f.write(f"  Параметр #{i+1}, форма: {w.shape}\n")
                    np.set_printoptions(threshold=np.inf, linewidth=200, suppress=True)
                    f.write(f"  Значения: {np.array2string(w, separator=', ')}\n\n")
            else:
                f.write("Нет обучаемых параметров.\n\n")
            f.write("-" * 80 + "\n")

    print(f"[+] Все веса и коэффициенты сохранены в '{output_path}'.")

# Создаем нейронную сеть
model = Sequential([
    Dense(64, activation='relu', input_shape=(20,), name='dense_input_layer'),
    Dense(48, activation='relu', name='dense_hidden_layer_1'),
    Dense(32, activation='relu', name='dense_hidden_layer_2'), 
    Dense(16, activation='relu', name='dense_hidden_layer_3'),
    Dense(1, activation='linear', name='dense_output_layer')
])

# Компилируем модель
model.compile(optimizer='adam', loss='mse')

print("=== РЕАЛИСТИЧНАЯ Нейронная сеть ===")
model.summary()

def set_realistic_weights(model):
    np.random.seed(42)
    
    # СЛОЙ 1: 20 входов -> 64 нейрона
    # Создаем несколько "мощных путей" через всю сеть
    strong_paths = []
    for _ in range(8):  # 8 мощных путей
        path = {
            'input_neuron': np.random.randint(0, 20),
            'layer1_neuron': np.random.randint(0, 64),
            'layer2_neuron': np.random.randint(0, 48), 
            'layer3_neuron': np.random.randint(0, 32),
            'layer4_neuron': np.random.randint(0, 16)
        }
        strong_paths.append(path)
    
    weights_layer1 = np.random.normal(0, 0.3, (20, 64))
    # Усиливаем веса для мощных путей
    for path in strong_paths:
        weights_layer1[path['input_neuron'], path['layer1_neuron']] += np.random.uniform(2.0, 4.0)
    
    biases_layer1 = np.random.normal(0, 0.2, 64)
    
    # СЛОЙ 2: 64 -> 48 нейронов
    weights_layer2 = np.random.normal(0, 0.25, (64, 48))
    # Продолжаем мощные пути
    for path in strong_paths:
        weights_layer2[path['layer1_neuron'], path['layer2_neuron']] += np.random.uniform(1.5, 3.0)
    
    biases_layer2 = np.random.normal(0, 0.15, 48)
    
    # СЛОЙ 3: 48 -> 32 нейрона  
    weights_layer3 = np.random.normal(0, 0.2, (48, 32))
    # Продолжаем мощные пути
    for path in strong_paths:
        weights_layer3[path['layer2_neuron'], path['layer3_neuron']] += np.random.uniform(1.2, 2.5)
    
    biases_layer3 = np.random.normal(0, 0.1, 32)
    
    # СЛОЙ 4: 32 -> 16 нейронов
    weights_layer4 = np.random.normal(0, 0.15, (32, 16))
    # Продолжаем мощные пути
    for path in strong_paths:
        weights_layer4[path['layer3_neuron'], path['layer4_neuron']] += np.random.uniform(1.0, 2.0)
    
    biases_layer4 = np.random.normal(0, 0.08, 16)
    
    # ВЫХОДНОЙ СЛОЙ: 16 -> 1 нейрон
    weights_layer5 = np.random.normal(0, 0.1, (16, 1))
    # Завершаем мощные пути сильными связями к выходу
    for path in strong_paths:
        weights_layer5[path['layer4_neuron'], 0] += np.random.uniform(0.8, 1.5)
    
    biases_layer5 = np.array([0.1])
    
    # Устанавливаем все веса в модель
    model.layers[0].set_weights([weights_layer1, biases_layer1])
    model.layers[1].set_weights([weights_layer2, biases_layer2])
    model.layers[2].set_weights([weights_layer3, biases_layer3])
    model.layers[3].set_weights([weights_layer4, biases_layer4])
    model.layers[4].set_weights([weights_layer5, biases_layer5])
    
    return strong_paths

# "Обучаем" модель - устанавливаем реалистичные веса
strong_paths = set_realistic_weights(model)

# Демонстрационные данные
X_demo = np.array([
    [1.0, 2.0, 3.0, 4.0, 5.0, 1.5, 2.5, 3.5, 4.5, 0.5, 
     0.8, 1.8, 2.8, 3.8, 4.8, 0.2, 1.2, 2.2, 3.2, 4.2],
    [0.5, 1.5, 2.5, 3.5, 4.5, 1.0, 2.0, 3.0, 4.0, 0.0,
     0.3, 1.3, 2.3, 3.3, 4.3, 0.7, 1.7, 2.7, 3.7, 4.7]
])

# Делаем предсказания
predictions = model.predict(X_demo)

# Сохраняем веса в файл
save_model_weights_to_txt(model)

print("\nМОЩНЫЕ ПУТИ через сеть:")
for i, path in enumerate(strong_paths):
    print(f"Путь {i+1}: Вход {path['input_neuron']} -> С1-Н{path['layer1_neuron']} -> "
          f"С2-Н{path['layer2_neuron']} -> С3-Н{path['layer3_neuron']} -> "
          f"С4-Н{path['layer4_neuron']} -> Выход")

print("\nПредсказания модели:")
for i, pred in enumerate(predictions):
    print(f"Вход {i+1}: -> Предсказание: {pred[0]:.6f}")

# Статистика
total_params = 0
for layer in model.layers:
    layer_params = layer.count_params()
    total_params += layer_params

print(f"\nОБЩЕЕ КОЛИЧЕСТВО ПАРАМЕТРОВ: {total_params:,}")