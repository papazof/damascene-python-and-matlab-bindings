#ifndef __MY_FAKE_CUTIL__
#define __MY_FAKE_CUTIL__

#define TO_STR(x) #x
#define CUDA_SAFE_CALL(X) {X; checkCudaError(TO_STR(X), __FILE__, TO_STR(__LINE__));} 

#include <stdexcept>

inline void checkCudaError(const char *msg, const char *file, const char *line)
{
    cudaError_t err = cudaGetLastError();

    if (cudaSuccess != err) {
        throw std::runtime_error(std::string(msg) + cudaGetErrorString(err) + '[' + std::string(file) + ',' + std::string(line) + ']');
    } 
}

#endif
