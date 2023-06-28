#ifndef __SIMULATE__
#define __SIMULATE__

#include "bufferManager.hpp"
using namespace std;    

enum policy{
    LRU = 1,
    MRU,
    CLOCK
};

#define PAGE_SIZE 4096

// process a select from query

class simulate{
private:
    baseBufferManager* bufferManager;

public:
    simulate(int numFrames, policy PolicyType);
    void processSelectQuery(FILE *file_pointer, int col1, string value);
    void processJoinQuery(FILE *file_pointer1, FILE *file_pointer2, int col1, int col2);
};


#endif