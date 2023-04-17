#ifndef __BUFF_MANAGER__
#define __BUFF_MANAGER__

#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <iterator>
#include <list>

using namespace std;
#define PAGE_SIZE 4096

class pageFrame{
private:
    bool is_pinned;             // either is_pinned or unpinned
    bool ref_bit;         // for clock replacement algorithm
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
    list<pageFrame> lru;  // list to implement LRU
    map<pair<FILE*, int>, list<pageFrame>::iterator> mp;   // map to identify whether a page is present in buffer or not

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
    list<pageFrame> mru;   // list to implement MRU
    map<pair<FILE*, int>, list<pageFrame>::iterator> mp;   // map to identify whether a page is present in buffer or not

public:
    MRUBufferManager(int numFrames);
    char* getPage(FILE*file_pointer, int num_page);
    void unpinPage(FILE*file_pointer, int num_page);
    ~MRUBufferManager();
};

#endif