import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import sys

IMG_SIZE = (224, 224)

def create_test_image(shape_type='circle'):
    img = np.zeros((IMG_SIZE[0], IMG_SIZE[1], 3), dtype=np.float32)

    if shape_type == 'circle':
        center = (IMG_SIZE[0]//2, IMG_SIZE[1]//2)
        radius = np.random.randint(IMG_SIZE[0]//3, IMG_SIZE[0]//2)
        color = (np.random.random(), np.random.random(), np.random.random())
        cv2.circle(img, center, radius, color, -1)

    elif shape_type == 'square':
        start = np.random.randint(10, IMG_SIZE[0]//4, size=2)
        end = (start[0] + np.random.randint(IMG_SIZE[0]//2, int(IMG_SIZE[0]*0.8)),
               start[1] + np.random.randint(IMG_SIZE[1]//2, int(IMG_SIZE[1]*0.8)))
        color = (np.random.random(), np.random.random(), np.random.random())
        cv2.rectangle(img, tuple(start), tuple(end), color, -1)

    elif shape_type == 'triangle':
        margin = 10
        pts = np.array([
            [np.random.randint(margin, IMG_SIZE[0]-margin), np.random.randint(margin, IMG_SIZE[1]-margin)],
            [np.random.randint(margin, IMG_SIZE[0]-margin), np.random.randint(margin, IMG_SIZE[1]-margin)],
            [np.random.randint(margin, IMG_SIZE[0]-margin), np.random.randint(margin, IMG_SIZE[1]-margin)]
        ], np.int32)
        color = (np.random.random(), np.random.random(), np.random.random())
        cv2.fillPoly(img, [pts], color)

    noise = np.random.normal(0, 0.05, img.shape)
    img = np.clip(img + noise, 0, 1)
    return img

def test_model(model, num_tests=5):
    shapes = ["circle", "square", "triangle"]
    class_names = ["unknown", "circle", "square", "triangle"]

    for shape_name in shapes:
        print(f"\n📌 Тестируем {shape_name}s:")
        for i in range(num_tests):
            img = create_test_image(shape_name)

            # --- предсказание модели без прогресс-бара ---
            img_batch = np.expand_dims(img, axis=0)
            probabilities = model.predict(img_batch, verbose=0)[0]  # verbose=0 убирает лишнее

            probs_2class = probabilities[:2]  # только circle/square
            pred_index = np.argmax(probs_2class)
            pred_name = class_names[pred_index+1]

            # --- вывод изображения с предсказанием ---
            plt.imshow(img)
            plt.title(f"{shape_name.capitalize()} → Predicted: {pred_name}")
            plt.axis('off')
            plt.show()

            # --- вывод в консоль ---
            print(f"  {i+1}/{num_tests}: Предсказание для {shape_name}: {pred_name}")
            print(f"       Вероятности: {probs_2class.round(3)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python testModel.py путь_к_модели.h5")
        sys.exit(1)

    model_path = sys.argv[1]
    model = tf.keras.models.load_model(model_path)
    print("📊 Структура модели:")
    model.summary()

    test_model(model, num_tests=5)
