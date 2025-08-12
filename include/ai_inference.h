#ifndef AI_INFERENCE_H
#define AI_INFERENCE_H

#include <stdint.h>

void ai_init();
void ai_predict(float *input, float *output, int input_len, int output_len);
void softmax(const float *input, float *output, int length);
int8_t quantize_float_to_int8(float value, float scale, int zero_point);

#endif
