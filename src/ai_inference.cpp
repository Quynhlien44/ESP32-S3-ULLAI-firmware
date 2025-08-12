#include "ai_inference.h"
#include "model.h" // Model .h export from Python
#include <EloquentTinyML.h>
#include <Arduino.h>
#include <math.h>

// Define input/output sizes & Tensor arena size consistent với model
#define N_INPUTS 5
#define N_OUTPUTS 3
#define TENSOR_ARENA_SIZE (16 * 1024)

static Eloquent::TinyML::TfLite<N_INPUTS, N_OUTPUTS, TENSOR_ARENA_SIZE> ml;

// Thông số scaler của cảm biến (trước khi quantize)
const float adc_min = 0.0f, adc_max = 3.3f;
const float temp_mean = 25.0f, temp_std = 5.0f;
const float hum_mean = 50.0f, hum_std = 10.0f;
const float tvoc_min = 0.0f, tvoc_max = 1000.0f;
const float eco2_min = 400.0f, eco2_max = 2000.0f;

// *** Thông số quantization lấy từ export_tflite.py ***
const float input_scale = 0.0039136889f;
const int input_zero_point = -128;
const float output_scale = 0.0022567196f;
const int output_zero_point = -128;

// Chuyển float đã normalize sang int8 theo scale/zero_point
int8_t quantize_float_to_int8(float value, float scale, int zero_point)
{
    int quantized = (int)(value / scale) + zero_point;
    if (quantized > 127)
        quantized = 127;
    if (quantized < -128)
        quantized = -128;
    return (int8_t)quantized;
}

// Softmax cho logits float
void softmax(const float *input, float *output, int length)
{
    float max_val = input[0];
    for (int i = 1; i < length; i++)
        if (input[i] > max_val)
            max_val = input[i];

    float sum = 0.0f;
    for (int i = 0; i < length; i++)
    {
        output[i] = expf(input[i] - max_val);
        sum += output[i];
    }
    for (int i = 0; i < length; i++)
        output[i] /= sum;
}

void ai_init()
{
    if (!ml.begin(model_tflite))
    {
        Serial.println("Model initialization failed!");
        while (1)
            ;
    }
    Serial.println("Model initialized OK");
}

void ai_predict(float *input, float *output_float, int input_len, int output_len)
{
    // 1️⃣ Chuẩn hóa dữ liệu sensor (giống pipeline train)
    float normalized[N_INPUTS];
    normalized[0] = (input[0] - adc_min) / (adc_max - adc_min);
    normalized[1] = (input[1] - temp_mean) / temp_std;
    normalized[2] = (input[2] - hum_mean) / hum_std;
    normalized[3] = (input[3] - tvoc_min) / (tvoc_max - tvoc_min);
    normalized[4] = (input[4] - eco2_min) / (eco2_max - eco2_min);

    // 2️⃣ Quantize sang int8
    int8_t input_quantized[N_INPUTS];
    for (int i = 0; i < input_len; i++)
    {
        input_quantized[i] = quantize_float_to_int8(normalized[i], input_scale, input_zero_point);
    }

    // 3️⃣ Predict (int8 in → int8 out)
    int8_t output_int8[N_OUTPUTS];
    ml.predict(input_quantized, output_int8);

    // 4️⃣ Dequantize output sang float logits
    for (int i = 0; i < output_len; i++)
    {
        output_float[i] = (output_int8[i] - output_zero_point) * output_scale;
    }

    // Debug: In input quantized & output logits
    Serial.print("Input int8: ");
    for (int i = 0; i < input_len; i++)
    {
        Serial.printf("%d ", input_quantized[i]);
    }
    Serial.println();

    Serial.print("Output logits: ");
    for (int i = 0; i < output_len; i++)
    {
        Serial.printf("%.5f ", output_float[i]);
    }
    Serial.println();
}
