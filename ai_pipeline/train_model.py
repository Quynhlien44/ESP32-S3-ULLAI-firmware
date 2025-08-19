import tensorflow as tf
import pandas as pd
import numpy as np
import json

df = pd.read_csv('data/dataset_real_clean.csv')
with open('scaler.json') as f:
    scaler = json.load(f)

# (1) CLEAN scenario labels — replace empty/redundant values
valid_scenarios = ['normal', 'high_temp', 'high_humidity', 'low_light', 'anomaly'] 
df['scenario'] = df['scenario'].fillna('normal')
df.loc[df['scenario'] == '', 'scenario'] = 'normal'
df = df[df['scenario'].isin(valid_scenarios)] 

# (2) INPUT STANDARDIZATION
x = np.stack([
    (df['ldr_v'] - scaler['ldr_min']) / (scaler['ldr_max'] - scaler['ldr_min'] + 1e-8),
    (df['temp_c'] - scaler['temp_mean']) / (scaler['temp_std'] + 1e-8),
    (df['hum_pct'] - scaler['hum_mean']) / (scaler['hum_std'] + 1e-8),
    (df['tvoc_ppb'] - scaler['tvoc_min']) / (scaler['tvoc_max'] - scaler['tvoc_min'] + 1e-8),
    (df['eco2_ppm'] - scaler['eco2_min']) / (scaler['eco2_max'] - scaler['eco2_min'] + 1e-8)
], axis=1)

# (3) CREATE OUTPUT LABEL (y) and check label encoding
y = df['scenario'].astype('category').cat.codes
print('Unique scenario codes:', np.unique(y))

# (4) MODEL BUILDING AND TRAINING
model = tf.keras.Sequential([
    tf.keras.layers.InputLayer(input_shape=(5,)), # change input_shape to shape if using TF2.14+
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2), 
    tf.keras.layers.Dense(24, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(len(np.unique(y))) # Number of scenario labels
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x, y, epochs=100, validation_split=0.1)

preds = model.predict(x[:10])
print("Sample output logits:\n", preds)


# (5) Convert/yield quantized TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
def representative_dataset():
    import numpy as np
    indices = np.random.choice(x.shape[0], min(100, x.shape[0]), replace=False)
    for i in indices:
        yield [x[i:i+1].astype(np.float32)]
converter.representative_dataset = representative_dataset
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8
model.save('model_float.h5')

tflite_model = converter.convert()
with open('quantized_model.tflite', 'wb') as f:
    f.write(tflite_model)
import os
os.system("xxd -i quantized_model.tflite > model.h")
print("Model exported to quantized_model.tflite and model.h")


