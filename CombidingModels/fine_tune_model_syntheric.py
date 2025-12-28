import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 5
NUM_CLASSES = 2  # Подставь нужное количество классов
OUTPUT_MODEL_PATH = "reconstructed_model_upgraded.h5"

# --- Функция для генерации изображений ---
def create_image(shape_type='circle'):
    img = np.zeros((IMG_SIZE[0], IMG_SIZE[1], 3), dtype=np.float32)

    if shape_type == 'circle':
        radius = np.random.randint(60, 100)
        center = (IMG_SIZE[0]//2, IMG_SIZE[1]//2)
        color = (np.random.random(), np.random.random(), np.random.random())
        cv2.circle(img, center, radius, color, -1)

    elif shape_type == 'square':
        start = 40
        end = IMG_SIZE[0] - 40
        color = (np.random.random(), np.random.random(), np.random.random())
        cv2.rectangle(img, (start, start), (end, end), color, -1)

    elif shape_type == 'triangle':
        pts = np.array([[IMG_SIZE[0]//2, 30], [30, IMG_SIZE[1]-30], [IMG_SIZE[0]-30, IMG_SIZE[1]-30]], np.int32)
        color = (np.random.random(), np.random.random(), np.random.random())
        cv2.fillPoly(img, [pts], color)

    # добавляем шум
    noise = np.random.normal(0, 0.05, img.shape)
    img = np.clip(img + noise, 0, 1)
    return img

# --- Генератор данных ---
def data_generator(batch_size=BATCH_SIZE):
    shapes = ['circle', 'square', 'triangle']
    while True:
        X = []
        y = []
        for _ in range(batch_size):
            shape = np.random.choice(shapes)
            img = create_image(shape)
            X.append(img)

            # метки: circle=0, square=1, triangle=ignored/unknown
            if shape == 'circle':
                label = [1, 0]
            elif shape == 'square':
                label = [0, 1]
            else:  # треугольник — unknown
                label = [0, 0]  # модель не должна сильно уверенно предсказывать
            y.append(label)
        yield np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)

# --- Загружаем модель ---
model = load_model("reconstructed_model.h5")
print("Модель загружена.")

# Замораживаем старые слои кроме последних 3
for layer in model.layers[:-3]:
    layer.trainable = False

model.compile(optimizer=Adam(1e-4),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# --- Дообучение ---
steps_per_epoch = 20
val_steps = 5

train_gen = data_generator(batch_size=BATCH_SIZE)
val_gen = data_generator(batch_size=BATCH_SIZE)

history = model.fit(
    train_gen,
    validation_data=val_gen,
    steps_per_epoch=steps_per_epoch,
    validation_steps=val_steps,
    epochs=EPOCHS
)

# --- Сохраняем модель ---
model.save(OUTPUT_MODEL_PATH)
print(f"Модель дообучена и сохранена как {OUTPUT_MODEL_PATH}")

