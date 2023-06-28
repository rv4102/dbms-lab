#include "bufferManager.hpp"

// constructor for pageFrame
pageFrame::pageFrame(){}

// copy constructor for Frame
pageFrame::pageFrame(const pageFrame &pageFrame){
    this->num_page = pageFrame.num_page;
    this->data = new char[PAGE_SIZE];
    memcpy(this->data, pageFrame.data, PAGE_SIZE);
    this->file_pointer = pageFrame.file_pointer;
    this->is_pinned = pageFrame.is_pinned;
    this->ref_bit = pageFrame.ref_bit;
}

// populates a frame in memory
void pageFrame::setFrame(FILE*file_pointer, int num_page, char* data, bool is_pinned){
    this->num_page = num_page;
    this->data = data;
    this->file_pointer = file_pointer;
    this->is_pinned = is_pinned;
    this->ref_bit = true;
}

// unpin a frame
void pageFrame::unpinFrame(){
    this->is_pinned = false;
}

// destructor for Frame
pageFrame::~pageFrame(){
    delete[] data;
}


// constructor for bufferStats
bufferStats::bufferStats(): accesses(0), diskReads(0), pageHits(0) {}

// clear stats
void bufferStats::clear(){
    accesses = 0;
    diskReads = 0;
    pageHits = 0;
}


void baseBufferManager::increment_accesses(){
    stats.accesses++;
}

void baseBufferManager::increment_diskReads(){
    stats.diskReads++;
}

void baseBufferManager::increment_pageHits(){
    stats.pageHits++;
}

int baseBufferManager::getNumFrames(){
    return numFrames;
}

// clear stats
void baseBufferManager::clearStats(){
    stats.clear();
}

// get stats
bufferStats baseBufferManager::getStats(){
    return stats;
}


// constructor for LRUBufferManager
LRUBufferManager::LRUBufferManager(int numFrames): baseBufferManager(numFrames) {}

// destructor for LRUBufferManager
LRUBufferManager::~LRUBufferManager(){
    lru.clear();    // calls destructor of Frame so delete of data happens
    mp.clear();
}

// get a page from buffer
char* LRUBufferManager::getPage(FILE*file_pointer, int num_page){
    // check if page present in memory using map
    auto it = mp.find({file_pointer, num_page});
    if(it!=mp.end()){
        increment_accesses();
        increment_pageHits();

        // page present in memory
        lru.push_front(*(it->second));
        lru.erase(it->second);
        mp[{file_pointer, num_page}] = lru.begin();
        lru.begin()->is_pinned = true;
        return lru.begin()->data;
    }

    // if page is not in memory
    // check if space is there in buffer
    if((int)lru.size() == getNumFrames()){
        // find last unpinned page and remove it
        auto it = lru.end();
        it--;

        while(it->is_pinned){
            if(it==lru.begin())return NULL;
            it--;
        }

        // remove page from buffer
        mp.erase({it->file_pointer, it->num_page});
        lru.erase(it);
    }

    // add the page to buffer
    char* data = new char[PAGE_SIZE];
    fseek(file_pointer, num_page*PAGE_SIZE, SEEK_SET);
    fread(data, PAGE_SIZE, 1, file_pointer);

    pageFrame frame = pageFrame();
    frame.setFrame(file_pointer, num_page, data, true);
    lru.push_front(frame);

    mp[{file_pointer, num_page}] = lru.begin();
    increment_accesses();
    increment_diskReads();
    char name[20];
    memcpy(name, data, 20);
    return lru.begin()->data;
}

// unpin a page
void LRUBufferManager::unpinPage(FILE*file_pointer, int num_page){
    // check if page present in memory using map
    auto it = mp.find({file_pointer, num_page});
    if(it != mp.end()){
        // page present in memory
        // unpin page
        it->second->unpinFrame();
    }
}



// constructor for ClockBufferManager
ClockBufferManager::ClockBufferManager(int numFrames): baseBufferManager(numFrames), clock_hand(0), numPages(0){
    bufferPool = new pageFrame[numFrames];
}

// destructor for ClockBufferManager
ClockBufferManager::~ClockBufferManager(){
    delete[] bufferPool;
}

// get a page from buffer
char *ClockBufferManager::getPage(FILE* file_pointer, int num_page){
    // check if the page is present in memory
    for(int i=0;i<numPages;++i){
        if(bufferPool[i].file_pointer == file_pointer && bufferPool[i].num_page == num_page){
            // page is present in memory
            // update stats
            increment_accesses();

            // update second chance
            bufferPool[i].ref_bit = true;
            bufferPool[i].is_pinned = true;
            increment_pageHits();
            return bufferPool[i].data;
        }
    }

    // page is not present in memory
    if(numPages < getNumFrames()){
        fseek(file_pointer, num_page*PAGE_SIZE, SEEK_SET);
        char* data = new char[PAGE_SIZE];
        fread(data, PAGE_SIZE, 1, file_pointer);
        bufferPool[numPages].setFrame(file_pointer, num_page, data, true);
        numPages++;
        increment_accesses();
        increment_diskReads();
        return data;
    }
    increment_accesses();
    increment_diskReads();

    // page is not present in memory and memory is full
    while(true){
        if(bufferPool[clock_hand].ref_bit){
            // page has second chance
            bufferPool[clock_hand].ref_bit = false;
            clock_hand = (clock_hand+1)%getNumFrames();
            continue;
        }
        if(bufferPool[clock_hand].is_pinned){
            // page is is_pinned
            clock_hand = (clock_hand+1)%getNumFrames();
            continue;
        }
        // page is not is_pinned and does not have second chance
        // seek the page in file
        fseek(file_pointer, num_page*PAGE_SIZE, SEEK_SET);
        fread(bufferPool[clock_hand].data, PAGE_SIZE, 1, file_pointer);
        bufferPool[clock_hand].file_pointer = file_pointer;
        bufferPool[clock_hand].num_page = num_page;
        bufferPool[clock_hand].is_pinned = true;
        bufferPool[clock_hand].ref_bit = true;
        int store = clock_hand;
        clock_hand = (clock_hand+1)%getNumFrames();
        increment_diskReads();
        return bufferPool[store].data;
    }
}

// unpin a page
void ClockBufferManager::unpinPage(FILE* file_pointer, int num_page){
    // check if page is present in memory
    for(int i=0;i<numPages;++i){
        if(bufferPool[i].file_pointer == file_pointer && bufferPool[i].num_page == num_page){
            // page is present in memory
            // unpin page
            bufferPool[i].unpinFrame();
            return;
        }
    }
}



// constructor for MRUBufferManager
MRUBufferManager::MRUBufferManager(int numFrames): baseBufferManager(numFrames) {}

// destructor for MRUBufferManager
MRUBufferManager::~MRUBufferManager(){
    mru.clear();      // the destructor of frame will be automatically called
    mp.clear();
}

// get a page from buffer
char *MRUBufferManager::getPage(FILE* file_pointer, int num_page){

    // check if page is present in memory
    auto it = mp.find({file_pointer, num_page});
    if(it!=mp.end()){
        increment_accesses();
        // present so bring it to first and pin
        mru.push_front(*it->second);
        mru.erase(it->second);
        mp[{file_pointer, num_page}] = mru.begin();
        mru.begin()->is_pinned = true;
        increment_pageHits();
        return mru.begin()->data;
    }

    // not in memory, so check size
    if((int)mru.size() == getNumFrames()){

        int removed = 0;
        for(auto it=mru.begin();it!=mru.end();++it){
            if(it->is_pinned){
                // page is is_pinned
                continue;
            }
            // page is not is_pinned
            // remove it from memory
            mp.erase({it->file_pointer, it->num_page});
            mru.erase(it);
            removed = 1;
            break;
        }

        if(!removed)return NULL;
    }

    // add the frame at start
    fseek(file_pointer, num_page*PAGE_SIZE, SEEK_SET);
    char* data = new char[PAGE_SIZE];
    fread(data, PAGE_SIZE, 1, file_pointer);
    pageFrame frame = pageFrame();
        
    frame.setFrame(file_pointer, num_page, data, true);
    mru.push_front(frame);
    mp[{file_pointer, num_page}] = mru.begin();
    increment_accesses();
    increment_diskReads();
    return mru.begin()->data;
}

// unpin the frame
void MRUBufferManager::unpinPage(FILE *file_pointer, int num_page){
    // check if page is present in memory
    auto it = mp.find({file_pointer, num_page});
    if(it != mp.end()){
        // page is present in memory
        // unpin page
        it->second->unpinFrame();
    }
}