#ifndef __BUFF_MANAGER__
#define __BUFF_MANAGER__

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <iterator>
#include <queue>

using namespace std;
#define PAGE_SIZE 4096

class pageFrame{
private:
    bool is_pinned;             // either is_pinned or unpinned
    bool second_chance;         // for clock replacement algorithm
    int num_page;               // page number of page
    char *data;                 // data in page
    FILE *file_pointer;         // file to which this page belongs to

    void setFrame(FILE*file_pointer, int num_page, char* data, bool is_pinned);
    void unpinFrame();

public:
    pageFrame();                        // default constructor
    pageFrame(const pageFrame& f);          // copy constructor
    ~pageFrame();                       // destructor
    friend class LRUBufferManager;
    friend class MRUBufferManager;
    friend class ClockBufferManager;
};


class bufferStats{
public:
    int accesses;
    int diskReads;
    int pageHits;

    bufferStats();          // constructor
    void clear();           // clear stats
};


struct PairHash {
    size_t operator()(const pair<FILE *, int>& p) const {
        size_t h1 = hash<FILE *>()(p.first);
        size_t h2 = hash<int>()(p.second);
        return h1 ^ h2;
    }
};


class baseBufferManager {
private:
    int numFrames;          // number of frames that can be fit in pool
    bufferStats stats;      // stats for buffer manager
public:
    baseBufferManager(int numFrames): numFrames(numFrames) {}    // constructor
    virtual ~baseBufferManager() {}                              // destructor
    virtual char* getPage(FILE *file_pointer, int num_page) = 0;
    virtual void unpinPage(FILE *file_pointer, int num_page) = 0;
    
    bufferStats getStats();
    void clearStats();
    int getNumFrames();
    void increment_accesses();
    void increment_diskReads();
    void increment_pageHits();
};


class LRUBufferManager: public baseBufferManager{
private:
    deque<pageFrame> lru;  // list to implement LRU
    unordered_map<pair<FILE*, int>, deque<pageFrame>::iterator, PairHash> mp;   // map to identify whether a page is present in buffer or not

public:
    LRUBufferManager(int numFrames);
    char* getPage(FILE *file_pointer, int num_page);
    void unpinPage(FILE *file_pointer, int num_page);
    ~LRUBufferManager();
};


// implement clock replacement algorithm
class ClockBufferManager: public baseBufferManager{
private:
    pageFrame* bufferPool;  // list to implement clock
    int clock_hand;     // clock hand
    int numPages;

public:
    ClockBufferManager(int numFrames);
    char* getPage(FILE*file_pointer, int num_page);
    void unpinPage(FILE*file_pointer, int num_page);
    ~ClockBufferManager();
};


class MRUBufferManager: public baseBufferManager{
private:
    deque<pageFrame> mru;   // list to implement MRU
    unordered_map<pair<FILE*, int>, deque<pageFrame>::iterator, PairHash> mp;   // map to identify whether a page is present in buffer or not

public:
    MRUBufferManager(int numFrames);
    char* getPage(FILE*file_pointer, int num_page);
    void unpinPage(FILE*file_pointer, int num_page);
    ~MRUBufferManager();
};

#endif