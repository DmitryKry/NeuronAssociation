import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import plot_model
import numpy as np

def save_model_weights_to_txt(model, output_path="model_weights.txt"):
    """Сохраняет все веса и коэффициенты модели в текстовый файл."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Модель: {model.name}\n")
        f.write("=" * 60 + "\n\n")

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
            f.write("-" * 60 + "\n")

    print(f"[+] Все веса и коэффициенты сохранены в '{output_path}'.")

# Создаем нейронную сеть
model = Sequential([
    Dense(15, activation='relu', input_shape=(5,), name='dense_input_layer'),
    Dense(10, activation='relu', name='dense_hidden_layer_1'),
    Dense(5, activation='relu', name='dense_hidden_layer_2'),
    Dense(1, activation='linear', name='dense_output_layer')
])

# Компилируем модель
model.compile(optimizer='adam', loss='mse')


print("=== Нейронная сеть ДО псевдо-обучения ===")
model.summary()

# Функция для установки конкретных весов
def set_custom_weights(model):
    # Устанавливаем конкретные значения весов для каждого слоя
    
    # Слой 1: входной -> 15 нейронов
    # Веса: 5 входов × 15 нейронов
    weights_layer1 = np.array([
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5],
        [1.5, 1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        [0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 1.5, 1.5, 1.5],
        [2.0, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.2, 0.0, -0.2, -0.4, -0.6, -0.8],
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]
    ])
    biases_layer1 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5])
    
    # Слой 2: 15 -> 10 нейронов
    weights_layer2 = np.array([
        [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
        [1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2],
        [0.8, 0.8, 0.8, 0.8, 0.8, 1.2, 1.2, 1.2, 1.2, 1.2],
        [1.5, 1.3, 1.1, 0.9, 0.7, 0.5, 0.3, 0.1, -0.1, -0.3],
        [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1],
        [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
        [1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
        [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2],
        [1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3],
        [0.7, 0.7, 0.7, 0.7, 0.7, 1.1, 1.1, 1.1, 1.1, 1.1],
        [1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4],
        [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3],
        [1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2],
        [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
    ])
    biases_layer2 = np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1])
    
    # Слой 3: 10 -> 5 нейронов
    weights_layer3 = np.array([
        [0.3, 0.4, 0.5, 0.6, 0.7],
        [0.7, 0.6, 0.5, 0.4, 0.3],
        [1.0, 1.0, 1.0, 1.0, 1.0],
        [0.5, 0.6, 0.7, 0.8, 0.9],
        [0.9, 0.8, 0.7, 0.6, 0.5],
        [1.2, 1.1, 1.0, 0.9, 0.8],
        [0.8, 0.9, 1.0, 1.1, 1.2],
        [0.4, 0.5, 0.6, 0.7, 0.8],
        [0.6, 0.7, 0.8, 0.9, 1.0],
        [1.1, 1.0, 0.9, 0.8, 0.7]
    ])
    biases_layer3 = np.array([0.3, 0.4, 0.5, 0.6, 0.7])
    
    # Слой 4: 5 -> 1 нейрон
    weights_layer4 = np.array([
        [0.8],
        [1.2],
        [0.5],
        [1.0],
        [0.3]
    ])
    biases_layer4 = np.array([0.5])
    
    # Устанавливаем все веса в модель
    model.layers[0].set_weights([weights_layer1, biases_layer1])
    model.layers[1].set_weights([weights_layer2, biases_layer2])
    model.layers[2].set_weights([weights_layer3, biases_layer3])
    model.layers[3].set_weights([weights_layer4, biases_layer4])

# "Обучаем" модель - устанавливаем наши кастомные веса
set_custom_weights(model)

print("\n=== Нейронная сеть ПОСЛЕ псевдо-обучения ===")

# Демонстрационные данные
X_demo = np.array([
    [1.0, 2.0, 3.0, 4.0, 5.0],
    [0.5, 1.5, 2.5, 3.5, 4.5],
    [2.0, 1.0, 0.5, 1.5, 2.5]
])

print("\nДемонстрационные входные данные:")

# Делаем предсказания
predictions = model.predict(X_demo)
save_model_weights_to_txt(model)

try:
    plot_model(model, 
               to_file='model_architecture.png',
               show_shapes=True,
               show_layer_names=True,
               dpi=96,
               rankdir='TB')  # TB - сверху вниз, LR - слева направо
    print("✅ Архитектура модели сохранена в 'model_architecture.png'")
except Exception as e:
    print(f"❌ Ошибка при создании изображения: {e}")

print("\nПредсказания модели с установленными весами:")
for i, pred in enumerate(predictions):
    print(f"Вход {i+1}: {X_demo[i]} -> Предсказание: {pred[0]:.4f}")

# Показываем некоторые веса
print("\n=== Примеры установленных весов ===")
print("Входной слой (первые 5 весов первого нейрона):", model.layers[0].get_weights()[0][:, 0][:5])
print("Смещения входного слоя (первые 5):", model.layers[0].get_weights()[1][:5])
print("Выходной слой веса:", model.layers[3].get_weights()[0].flatten())
print("Выходной слой смещение:", model.layers[3].get_weights()[1][0])