import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import random
import sys
import os

def save_model_weights_to_txt(model, output_path="model_weights_non_unick.txt"):
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

def main():
    # Проверяем аргументы командной строки
    
    model_path = sys.argv[1]
    
    # Проверяем существование файла
    if not os.path.exists(model_path):
        print(f"Ошибка: Файл '{model_path}' не существует!")
        sys.exit(1)
    
    try:
        # Загружаем модель
        print(f"[+] Загружаем модель из: {model_path}")
        model = tf.keras.models.load_model(model_path)
        print(f"[+] Модель '{model.name}' успешно загружена!")
        output_file = f"{model_path}_weights.txt"
        # Сохраняем веса
        save_model_weights_to_txt(model, output_file)
        
    except Exception as e:
        print(f"Ошибка при загрузке модели: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()