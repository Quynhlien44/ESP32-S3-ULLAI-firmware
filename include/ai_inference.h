#ifndef AI_INFERENCE_H
#define AI_INFERENCE_H

void ai_init();
void ai_predict(float *input, float *output, int input_len, int output_len);

#endif
