import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

def save_model_weights_to_txt(model, output_path="model_weights_more.txt"):
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

# Создаем БОЛЬШУЮ нейронную сеть
model = Sequential([
    Dense(64, activation='relu', input_shape=(20,), name='dense_input_layer'),
    Dense(48, activation='relu', name='dense_hidden_layer_1'),
    Dense(32, activation='relu', name='dense_hidden_layer_2'), 
    Dense(16, activation='relu', name='dense_hidden_layer_3'),
    Dense(1, activation='linear', name='dense_output_layer')
])

# Компилируем модель
model.compile(optimizer='adam', loss='mse')

print("=== БОЛЬШАЯ Нейронная сеть ===")
model.summary()

def set_chaotic_weights(model):
    np.random.seed(42)
    
    # СЛОЙ 1: 20 входов -> 64 нейрона
    weights_layer1 = np.zeros((20, 64))
    for i in range(20):
        for j in range(64):
            base = np.random.normal(0, 0.5)
            if np.random.random() < 0.15:
                power = np.random.uniform(2.0, 5.0) * np.random.choice([-1, 1])
                weights_layer1[i, j] = base + power
            elif np.random.random() < 0.3:
                medium = np.random.uniform(0.8, 1.5) * np.random.choice([-1, 1])
                weights_layer1[i, j] = base + medium
            else:
                weights_layer1[i, j] = base + np.random.uniform(-0.3, 0.3)
    
    biases_layer1 = np.array([np.random.normal(0, 0.7) for _ in range(64)])
    
    # СЛОЙ 2: 64 -> 48 нейронов
    weights_layer2 = np.zeros((64, 48))
    for i in range(64):
        for j in range(48):
            base = np.random.normal(0, 0.4)
            if np.random.random() < 0.12:
                power = np.random.uniform(1.8, 4.0) * np.random.choice([-1, 1])
                weights_layer2[i, j] = base + power
            elif np.random.random() < 0.25:
                medium = np.random.uniform(0.7, 1.3) * np.random.choice([-1, 1])
                weights_layer2[i, j] = base + medium
            else:
                weights_layer2[i, j] = base + np.random.uniform(-0.4, 0.4)
    
    biases_layer2 = np.array([np.random.normal(0, 0.6) for _ in range(48)])
    
    # СЛОЙ 3: 48 -> 32 нейрона
    weights_layer3 = np.zeros((48, 32))
    for i in range(48):
        for j in range(32):
            base = np.random.normal(0, 0.3)
            if np.random.random() < 0.1:
                power = np.random.uniform(1.5, 3.0) * np.random.choice([-1, 1])
                weights_layer3[i, j] = base + power
            elif np.random.random() < 0.2:
                medium = np.random.uniform(0.6, 1.2) * np.random.choice([-1, 1])
                weights_layer3[i, j] = base + medium
            else:
                weights_layer3[i, j] = base + np.random.uniform(-0.5, 0.5)
    
    biases_layer3 = np.array([np.random.normal(0, 0.5) for _ in range(32)])
    
    # СЛОЙ 4: 32 -> 16 нейронов
    weights_layer4 = np.zeros((32, 16))
    for i in range(32):
        for j in range(16):
            base = np.random.normal(0, 0.4)
            if np.random.random() < 0.08:
                power = np.random.uniform(1.2, 2.5) * np.random.choice([-1, 1])
                weights_layer4[i, j] = base + power
            elif np.random.random() < 0.15:
                medium = np.random.uniform(0.5, 1.0) * np.random.choice([-1, 1])
                weights_layer4[i, j] = base + medium
            else:
                weights_layer4[i, j] = base + np.random.uniform(-0.6, 0.6)
    
    biases_layer4 = np.array([np.random.normal(0, 0.4) for _ in range(16)])
    
    # ВЫХОДНОЙ СЛОЙ: 16 -> 1 нейрон
    weights_layer5 = np.zeros((16, 1))
    for i in range(16):
        base = np.random.normal(0, 0.5)
        if np.random.random() < 0.2:
            power = np.random.uniform(1.0, 2.0) * np.random.choice([-1, 1])
            weights_layer5[i, 0] = base + power
        else:
            weights_layer5[i, 0] = base + np.random.uniform(-0.8, 0.8)
    
    biases_layer5 = np.array([np.random.normal(0, 0.3)])
    
    # Устанавливаем все веса в модель
    model.layers[0].set_weights([weights_layer1, biases_layer1])
    model.layers[1].set_weights([weights_layer2, biases_layer2])
    model.layers[2].set_weights([weights_layer3, biases_layer3])
    model.layers[3].set_weights([weights_layer4, biases_layer4])
    model.layers[4].set_weights([weights_layer5, biases_layer5])

# "Обучаем" модель - устанавливаем наши веса
set_chaotic_weights(model)

# Демонстрационные данные для большой сети (20 входов!)
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

print("\nПредсказания модели:")
for i, pred in enumerate(predictions):
    print(f"Вход {i+1}: -> Предсказание: {pred[0]:.6f}")

# Простая статистика
total_params = 0
for layer in model.layers:
    layer_params = layer.count_params()
    total_params += layer_params

print(f"\nОБЩЕЕ КОЛИЧЕСТВО ПАРАМЕТРОВ: {total_params:,}")