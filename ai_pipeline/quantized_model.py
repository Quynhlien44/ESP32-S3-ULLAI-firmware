import tensorflow as tf
import numpy as np
import os

# 1. Create a simple model for demonstration
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(5,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dense(3)  # Linear,  not softmax
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
x = np.random.rand(1000, 5).astype(np.float32)
y = np.random.randint(0, 3, (1000,))
model.fit(x, y, epochs=10)

# 2. Convert using ONLY post-training quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS_INT8, tf.lite.OpsSet.TFLITE_BUILTINS
]
def representative_dataset():
    for _ in range(100):
        yield [np.random.rand(1, 5).astype(np.float32)]
converter.representative_dataset = representative_dataset
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

if os.path.exists("quantized_model.tflite"):
    os.remove("quantized_model.tflite")
tflite_model = converter.convert()
with open("quantized_model.tflite", "wb") as f:
    f.write(tflite_model)
os.system("xxd -i quantized_model.tflite > model.h")
print("Exported model.h using post-training quantization, NOT using tfmot/qat.")

