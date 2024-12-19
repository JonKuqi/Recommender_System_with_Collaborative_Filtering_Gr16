// Exported function
#include <stdio.h>
#include <immintrin.h>
#include <math.h>


__declspec(dllexport) double cosineSimilarity(const double *A, const double *B, int n){

    //    FORMULA
    //  dotProduct = addition from i to n  (Ai * Bi)
    //  sumASquared = addition from i to n (Ai)^2
    //  sumBSquared = addition from i to n (Bi)^2
    //
    // cosine_similarity = dotProduct/ sqrt(sumASquared) * sqrt(sumBSquared)

    //Vector 256-bit for 4 double values
    __m256d vectorA;
    __m256d vectorB;
    __m256d resultVector;

    //Accumulators
    //  A*B = dotProduct
    //  a1^2 + a2^2 +...+ an^2 = sumASquared
    //  b1^2 + b2^2 +...+ bn^2 = sumBSquared

    __m256d dotProduct = _mm256_setzero_pd(); //Make it zero initially
    __m256d sumASquared = _mm256_setzero_pd();
    __m256d sumBSquared = _mm256_setzero_pd();

    // 4 by 4 we calculate these values

    int i;

    for(int i=0; i<= n-4; i+=4){
        //Take 4 elements and put into the vectors
        vectorA = _mm256_loadu_pd(&A[i]);
        vectorB = _mm256_loadu_pd(&B[i]);

        resultVector = _mm256_mul_pd(vectorA, vectorB);
        dotProduct = _mm256_add_pd(dotProduct, vectorB);

        resultVector = _mm256_mul_pd(vectorA, vectorA);
        sumASquared = _mm256_add_pd(sumASquared, resultVector);

        resultVector = _mm256_mul_pd(vectorB, vectorB);
        sumBSquared = _mm256_add_pd(sumBSquared, resultVector);


    }

    //Convert to normal arrays
    double dotP[4], sumA[4], sumB[4];
    _mm256_storeu_pd(dotP, dotProduct);
    _mm256_storeu_pd(sumA, sumASquared);
    _mm256_storeu_pd(sumB, sumBSquared);

    //Sum parts
    double dotProductFinal = dotP[0] + dotP[1] + dotP[2] + dotP[3];
    double sumASquaredFinal = sumA[0] + sumA[1] + sumA[2] + sumA[3];
    double sumBSquaredFinal = sumB[0] + sumB[1] + sumB[2] + sumB[3];

    //Remaining numbers that that were left because of the 4 partition
    for(;i<n;i++){
        dotProductFinal += A[i] * B[i];
        sumASquaredFinal += A[i] * A[i];
        sumBSquaredFinal += B[i] * B[i];
    }


    return dotProductFinal / (sqrt(sumASquaredFinal) * sqrt(sumBSquaredFinal));
}

