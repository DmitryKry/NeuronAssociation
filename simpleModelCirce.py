import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
from sklearn.model_selection import train_test_split

# Параметры
IMG_SIZE = (64, 64)
BATCH_SIZE = 32
EPOCHS = 30
NUM_SAMPLES = 2000  # Общее количество изображений

# === СОЗДАНИЕ ДАТАСЕТА ===
def create_circle_dataset(num_samples=1000, img_size=IMG_SIZE):
    """Создает датасет с кругами и без кругов"""
    images = []
    labels = []
    
    for i in range(num_samples):
        # Создаем черное изображение
        img = np.zeros((img_size[0], img_size[1], 3), dtype=np.float32)
        
        if i % 2 == 0:  # 50% с кругами
            # Случайные параметры круга
            center = (np.random.randint(20, img_size[0]-20), 
                     np.random.randint(20, img_size[1]-20))
            radius = np.random.randint(10, 25)
            color = (np.random.random(), np.random.random(), np.random.random())  # Случайный цвет
            thickness = -1 if np.random.random() > 0.5 else 2  # Заполненный или контур
            
            # Рисуем круг
            cv2.circle(img, center, radius, color, thickness)
            labels.append(1)  # Класс "круг"
        else:
            # Изображение без кругов (шум или другие фигуры)
            if np.random.random() > 0.5:
                # Прямоугольник
                pt1 = (np.random.randint(10, img_size[0]-30), 
                       np.random.randint(10, img_size[1]-30))
                pt2 = (pt1[0] + np.random.randint(15, 40), 
                       pt1[1] + np.random.randint(15, 40))
                color = (np.random.random(), np.random.random(), np.random.random())
                cv2.rectangle(img, pt1, pt2, color, -1)
            else:
                # Треугольник
                pts = np.array([
                    [np.random.randint(10, img_size[0]-10), np.random.randint(10, img_size[1]-10)],
                    [np.random.randint(10, img_size[0]-10), np.random.randint(10, img_size[1]-10)],
                    [np.random.randint(10, img_size[0]-10), np.random.randint(10, img_size[1]-10)]
                ], np.int32)
                color = (np.random.random(), np.random.random(), np.random.random())
                cv2.fillPoly(img, [pts], color)
            
            labels.append(0)  # Класс "не круг"
        
        # Добавляем немного шума для реалистичности
        noise = np.random.normal(0, 0.1, img.shape)
        img = np.clip(img + noise, 0, 1)
        
        images.append(img)
    
    return np.array(images), np.array(labels)

# Создаем датасет
print("Создание датасета...")
X, y = create_circle_dataset(NUM_SAMPLES)

# Визуализируем несколько примеров
plt.figure(figsize=(12, 6))
for i in range(8):
    plt.subplot(2, 4, i+1)
    plt.imshow(X[i])
    plt.title(f'Class: {"Circle" if y[i] == 1 else "No circle"}')
    plt.axis('off')
plt.tight_layout()
plt.show()

# Разделяем на тренировочную и валидационную выборки
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Тренировочные данные: {X_train.shape[0]} изображений")
print(f"Валидационные данные: {X_val.shape[0]} изображений")
print(f"Баланс классов в тренировочной выборке: {np.sum(y_train)} кругов из {len(y_train)}")

# === АУГМЕНТАЦИЯ ДАННЫХ ===
train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

val_datagen = ImageDataGenerator()  # Без аугментации для валидации

train_generator = train_datagen.flow(X_train, y_train, batch_size=BATCH_SIZE)
val_generator = val_datagen.flow(X_val, y_val, batch_size=BATCH_SIZE)

# === МОДЕЛЬ ===
model = Sequential([
    Conv2D(16, (3, 3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
    MaxPooling2D((2, 2)),
    
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    
    GlobalAveragePooling2D(),
    
    Dense(32, activation='relu'),
    Dropout(0.25),
    
    Dense(16, activation='relu'),
    Dropout(0.2),
    
    Dense(8, activation='relu'),
    Dropout(0.15),
    
    Dense(4, activation='relu'),
    
    Dense(1, activation='sigmoid')
])
model.compile(
    optimizer=Adam(1e-4),
    loss='binary_crossentropy',
    metrics=['accuracy',
             tf.keras.metrics.Precision(name='precision'),
             tf.keras.metrics.Recall(name='recall')]
)

model.summary()

# === КОЛБЭКИ ===
checkpoint = ModelCheckpoint(
    "circle_detector_model_{epoch:02d}.h5",
    save_freq='epoch',
    save_weights_only=False,
    verbose=1
)

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# === ОБУЧЕНИЕ ===
print("Начало обучения...")
history = model.fit(
    train_generator,
    steps_per_epoch=len(X_train) // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=val_generator,
    validation_steps=len(X_val) // BATCH_SIZE,
    callbacks=[checkpoint, early_stop]
)

# === ОЦЕНКА ===
loss, acc, prec, rec = model.evaluate(val_generator)
print(f"\nValidation accuracy: {acc:.3f}")
print(f"Precision: {prec:.3f}")
print(f"Recall: {rec:.3f}")
print(f"Loss: {loss:.4f}")

# === ГРАФИКИ ===
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train acc')
plt.plot(history.history['val_accuracy'], label='Val acc')
plt.title('Accuracy')
plt.legend()
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train loss')
plt.plot(history.history['val_loss'], label='Val loss')
plt.title('Loss')
plt.legend()
plt.tight_layout()
plt.show()

# === ТЕСТ НА НОВЫХ ДАННЫХ ===
print("\nТест на новых данных:")
test_images, test_labels = create_circle_dataset(10)
predictions = model.predict(test_images)

plt.figure(figsize=(15, 6))
for i in range(10):
    plt.subplot(2, 5, i+1)
    plt.imshow(test_images[i])
    pred_prob = predictions[i][0]
    pred_class = 1 if pred_prob > 0.5 else 0
    true_class = test_labels[i]
    color = 'green' if pred_class == true_class else 'red'
    plt.title(f'True: {true_class}, Pred: {pred_class}\nProb: {pred_prob:.3f}', color=color)
    plt.axis('off')
plt.tight_layout()
plt.show()