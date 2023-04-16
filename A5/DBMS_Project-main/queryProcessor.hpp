#ifndef __QUERY_PROCESSOR_H_
#define __QUERY_PROCESSOR_H_

#include "bufferManager.hpp"
using namespace std;    

enum policy{
    LRU = 1,
    MRU,
    CLOCK
};

#define PAGE_SIZE 4096

// process a select from query

class QueryProcessor{
private:
    baseBufferManager* bufferManager;

public:
    QueryProcessor(int numFrames, policy PolicyType);
    void processSelectQuery(FILE *file_pointer, int col1, string value);
    void processJoinQuery(FILE *file_pointer1, FILE *file_pointer2, int col1, int col2);
};


#endif