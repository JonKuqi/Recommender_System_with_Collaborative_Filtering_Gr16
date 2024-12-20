#include <immintrin.h> // For SIMD intrinsics
#include <stddef.h>    // For size_t

// Cross-platform symbol export macro
#ifdef _MSC_VER
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT __attribute__((visibility("default")))
#endif

// Exported function
EXPORT void weighted_sum(const double *array1, double weight1,
                         const double *array2, double weight2,
                         const double *array3, double weight3,
                         const double *array4, double weight4,
                         double *resultArray, size_t size) {
    __m128d vec1, vec2, vec3, vec4, res;
    __m128d w1 = _mm_set1_pd(weight1);
    __m128d w2 = _mm_set1_pd(weight2);
    __m128d w3 = _mm_set1_pd(weight3);
    __m128d w4 = _mm_set1_pd(weight4);

    size_t i;
    for (i = 0; i + 2 <= size; i += 2) {  // Process two double values at a time (128-bit registers)
        vec1 = _mm_loadu_pd(&array1[i]);
        vec2 = _mm_loadu_pd(&array2[i]);
        vec3 = _mm_loadu_pd(&array3[i]);
        vec4 = _mm_loadu_pd(&array4[i]);

        vec1 = _mm_mul_pd(vec1, w1);
        vec2 = _mm_mul_pd(vec2, w2);
        vec3 = _mm_mul_pd(vec3, w3);
        vec4 = _mm_mul_pd(vec4, w4);

        res = _mm_add_pd(vec1, vec2);
        res = _mm_add_pd(res, vec3);
        res = _mm_add_pd(res, vec4);

        _mm_storeu_pd(&resultArray[i], res);
    }

    // Handle the remaining elements (if the size is not a multiple of 2)
    for (; i < size; i++) {
        resultArray[i] = array1[i] * weight1 +
                         array2[i] * weight2 +
                         array3[i] * weight3 +
                         array4[i] * weight4;
    }
}
