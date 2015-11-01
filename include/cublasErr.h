#ifndef CUBLAS_ERR_H
#define CUBLAS_ERR_H

#define TO_STR(x) #x
#define CUBLAS_GET_ERR(X) checkCublasError(X, __FILE__, TO_STR(__LINE__)) 

#include <stdexcept>
#include <cublas_api.h>
#include "cublas_errors.h"

inline cublasStatus_t checkCublasError(cublasStatus_t error, const char *file, const char *line)
{
    char *errStr = NULL;

    errStr = (char *) CUBLAS_RESULT_STR[error].name;
    if (CUBLAS_STATUS_SUCCESS != error) {
        throw std::runtime_error(std::string(errStr) + '[' + std::string(file) + ',' + std::string(line) + ']');
    }

     return error; 
}
#endif
