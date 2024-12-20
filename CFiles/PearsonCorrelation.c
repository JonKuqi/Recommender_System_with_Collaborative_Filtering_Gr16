#include <stdio.h>
#include <math.h>

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif


EXPORT double PearsonCorrelation(double user1[], double user2[], double avg_user1, double avg_user2, int n) {
    double numerator = 0.0;
    double sum_sq_diff_user1 = 0.0;
    double sum_sq_diff_user2 = 0.0;
     
    for (int i = 0; i < n; i++) {
        
        double diff_user1 = user1[i] - avg_user1;
        double diff_user2 = user2[i] - avg_user2;
           
        numerator += diff_user1 * diff_user2;
        sum_sq_diff_user1 += diff_user1 * diff_user1;
        sum_sq_diff_user2 += diff_user2 * diff_user2;
    }
 
    
    if (sum_sq_diff_user1 == 0.0 || sum_sq_diff_user2 == 0.0) {
        return 0.0;
    }
   
    double denominator = sqrt(sum_sq_diff_user1 * sum_sq_diff_user2);
    
    return numerator / denominator;
}