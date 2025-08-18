import tensorflow as tf

interpreter = tf.lite.Interpreter(model_path="quantized_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()[0]      # just first output sensor
output_details = interpreter.get_output_details()[0]    # just first output tensor

print("Input quantization:", input_details['quantization'])    # tuple (scale, zero_point)
print("Output quantization:", output_details['quantization'])

print("Input scale:", input_details['quantization'])
print("Input zero point:", input_details['quantization'][1])
print("Output scale:", output_details['quantization'][0])
print("Output zero point:", output_details['quantization'][1])
