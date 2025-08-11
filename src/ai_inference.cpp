#include "ai_inference.h"
#include "model.h" // Model .h export from Python
#include <EloquentTinyML.h>

// Define input/output sizes & Tensor arena size consistent với model
#define N_INPUTS 5
#define N_OUTPUTS 3
#define TENSOR_ARENA_SIZE (16 * 1024)

static Eloquent::TinyML::TfLite<N_INPUTS, N_OUTPUTS, TENSOR_ARENA_SIZE> ml;

const float adc_min = 0.0f, adc_max = 3.3f;
const float temp_mean = 25.0f, temp_std = 5.0f;
const float hum_mean = 50.0f, hum_std = 10.0f;
const float tvoc_min = 0.0f, tvoc_max = 1000.0f;
const float eco2_min = 400.0f, eco2_max = 2000.0f;

void ai_init()
{
    if (!ml.begin(model_tflite))
    {
        Serial.println("Model initialization failed!");
        while (1)
            ;
    }
}

void ai_predict(float *input, float *output, int input_len, int output_len)
{

    float normalized_input[N_INPUTS];
    normalized_input[0] = (input[0] - adc_min) / (adc_max - adc_min);
    normalized_input[1] = (input[1] - temp_mean) / temp_std;
    normalized_input[2] = (input[2] - hum_mean) / hum_std;
    normalized_input[3] = (input[3] - tvoc_min) / (tvoc_max - tvoc_min);
    normalized_input[4] = (input[4] - eco2_min) / (eco2_max - eco2_min);

    ml.predict(normalized_input, output);
}
