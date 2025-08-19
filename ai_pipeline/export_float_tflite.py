import tensorflow as tf

model = tf.keras.models.load_model('model_float.h5')

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = []

tflite_model_float = converter.convert()
with open('model_float.tflite', 'wb') as f:
    f.write(tflite_model_float)

print("Float TFLite model exported: model_float.tflite")
