import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
import cv2

import numpy as np

# Параметры
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 5

# Генератор синтетических данных
def generate_synthetic_data(num_samples=100):
    X = np.zeros((num_samples, IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)
    y = np.zeros((num_samples,), dtype=np.int32)
    
    for i in range(num_samples):
        shape_type = i % 3  # 0=circle, 1=square, 2=triangle
        y[i] = shape_type
        
        # простая генерация фигуры на фоне
        img = np.ones((IMG_SIZE, IMG_SIZE, 3), dtype=np.float32)  # белый фон
        if shape_type == 0:  # circle
            cv2.circle(img, (IMG_SIZE//2, IMG_SIZE//2), IMG_SIZE//3, (0,0,0), -1)
        elif shape_type == 1:  # square
            cv2.rectangle(img, (IMG_SIZE//4, IMG_SIZE//4), (3*IMG_SIZE//4, 3*IMG_SIZE//4), (0,0,0), -1)
        else:  # triangle
            pts = np.array([[IMG_SIZE//2, IMG_SIZE//4], [IMG_SIZE//4, 3*IMG_SIZE//4], [3*IMG_SIZE//4, 3*IMG_SIZE//4]])
            cv2.fillPoly(img, [pts], (0,0,0))
        
        X[i] = img / 255.0
    y_cat = to_categorical(y, num_classes=3)
    return X, y_cat

# Загружаем существующую модель
model = load_model('reconstructed_model.h5')
print("Модель загружена.")

# Изменяем последнюю Dense-слой на 3 нейрона для 3 классов
x = model.layers[-2].output
output = Dense(3, activation='softmax')(x)
model = tf.keras.Model(inputs=model.input, outputs=output)

# Компилируем модель
model.compile(optimizer=Adam(1e-4), loss='categorical_crossentropy', metrics=['accuracy'])

# Создаем синтетический датасет
X_train, y_train = generate_synthetic_data(150)
X_val, y_val = generate_synthetic_data(30)

# Дообучаем модель
model.fit(X_train, y_train, validation_data=(X_val, y_val), batch_size=BATCH_SIZE, epochs=EPOCHS)

# Сохраняем дообученную модель
model.save('reconstructed_model_upgraded.h5')
print("Модель дообучена и сохранена как reconstructed_model_upgraded.h5")
