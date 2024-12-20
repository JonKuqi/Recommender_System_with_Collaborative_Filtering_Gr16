// Exported function
#include <stdio.h>
#include <immintrin.h>
#include <math.h>
#include <stddef.h>    // For size_t
#include <stdlib.h>    // For malloc


__declspec(dllexport) double cosineSimilarity(const double *A, const double *B, int n) {

    //    FORMULA
    //  dotProduct = addition from i to n  (Ai * Bi)
    //  sumASquared = addition from i to n (Ai)^2
    //  sumBSquared = addition from i to n (Bi)^2
    //
    // cosine_similarity = dotProduct / (sqrt(sumASquared) * sqrt(sumBSquared))

    // 256-bit vectors for 4 double values
    __m256d vectorA;
    __m256d vectorB;
    __m256d resultVector;

    // Accumulators
    __m256d dotProduct = _mm256_setzero_pd(); // Initialize to zero
    __m256d sumASquared = _mm256_setzero_pd();
    __m256d sumBSquared = _mm256_setzero_pd();

    int i;

    // Process 4 elements at a time
    for (i = 0; i <= n - 4; i += 4) {
        // Load 4 elements into the vectors
        vectorA = _mm256_loadu_pd(&A[i]);
        vectorB = _mm256_loadu_pd(&B[i]);

        // Compute the dot product for these 4 elements
        resultVector = _mm256_mul_pd(vectorA, vectorB);
        dotProduct = _mm256_add_pd(dotProduct, resultVector);

        // Compute the squared sums for A and B
        resultVector = _mm256_mul_pd(vectorA, vectorA);
        sumASquared = _mm256_add_pd(sumASquared, resultVector);

        resultVector = _mm256_mul_pd(vectorB, vectorB);
        sumBSquared = _mm256_add_pd(sumBSquared, resultVector);
    }

    // Convert to normal arrays to sum the partial results
    double dotP[4], sumA[4], sumB[4];
    _mm256_storeu_pd(dotP, dotProduct);
    _mm256_storeu_pd(sumA, sumASquared);
    _mm256_storeu_pd(sumB, sumBSquared);

    // Sum up the parts
    double dotProductFinal = dotP[0] + dotP[1] + dotP[2] + dotP[3];
    double sumASquaredFinal = sumA[0] + sumA[1] + sumA[2] + sumA[3];
    double sumBSquaredFinal = sumB[0] + sumB[1] + sumB[2] + sumB[3];

    // Handle the remaining elements that didn't fit into the 4-element partition
    for (; i < n; i++) {
        dotProductFinal += A[i] * B[i];
        sumASquaredFinal += A[i] * A[i];
        sumBSquaredFinal += B[i] * B[i];
    }

    // Prevent division by zero
    if (sumASquaredFinal == 0 || sumBSquaredFinal == 0) {
        return 0.0;
    }

    return dotProductFinal / (sqrt(sumASquaredFinal) * sqrt(sumBSquaredFinal));
}



//weighted sum function
__declspec(dllexport) double* weighted_sum(const double *array1, double weight1,
                            const double *array2, double weight2,
                            const double *array3, double weight3,
                            const double *array4, double weight4,
                            size_t size) {

    // Use 256bit AVX registers (4 doubles per register)
    __m256d vec1, vec2, vec3, vec4, res;
    __m256d w1 = _mm256_set1_pd(weight1);
    __m256d w2 = _mm256_set1_pd(weight2);
    __m256d w3 = _mm256_set1_pd(weight3);
    __m256d w4 = _mm256_set1_pd(weight4);

    // dynamically allocate memory for the result array
    double* resultArray = (double*)malloc(size * sizeof(double));
    if (resultArray == NULL) {
        // if memory allocation fails
        return NULL;
    }

    size_t i;
    // Main loop that process 4 doubles at a time using AVX
    for (i = 0; i + 4 <= size; i += 4) {
        vec1 = _mm256_loadu_pd(&array1[i]);
        vec2 = _mm256_loadu_pd(&array2[i]);
        vec3 = _mm256_loadu_pd(&array3[i]);
        vec4 = _mm256_loadu_pd(&array4[i]);

        vec1 = _mm256_mul_pd(vec1, w1);
        vec2 = _mm256_mul_pd(vec2, w2);
        vec3 = _mm256_mul_pd(vec3, w3);
        vec4 = _mm256_mul_pd(vec4, w4);

        res = _mm256_add_pd(vec1, vec2);
        res = _mm256_add_pd(res, vec3);
        res = _mm256_add_pd(res, vec4);

        _mm256_storeu_pd(&resultArray[i], res);
    }

    // handle the remaining elements, if the size is not a multiple of 4
    for (; i < size; i++) {
        resultArray[i] = array1[i] * weight1 +
                         array2[i] * weight2 +
                         array3[i] * weight3 +
                         array4[i] * weight4;
    }

    return resultArray;  // return the dynamically allocated result array
}

__declspec(dllexport) void free_array(double* array) {
    free(array);
}

