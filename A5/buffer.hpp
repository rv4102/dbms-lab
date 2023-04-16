#ifndef __BUFFER_HPP__
#define __BUFFER_HPP__
#include <unordered_map>
#include <queue>
#include <algorithm>

#define BLOCK_SIZE 4096
enum BUFF_MANAGEMENT {LRU, MRU, CLOCK};

class BufferBlock {
public:
    BufferBlock();
    char* get_buffer();
    bool is_dirty() const;
    void set_dirty(bool dirty);
    int get_pin_count() const;
    void pin();
    int get_ref_bit();
    void set_ref_bit();
    void reset_ref_bit();
    void unpin();
    int get_block_id();
private:
    char buffer_[BLOCK_SIZE];  // Buffer to hold the data
    bool is_dirty_;      // Flag to indicate if the block has been modified
    int pin_count_;      // Counter to keep track of how many times the block has been pinned
    static int next_block_id;
    int block_id;
    int ref_bit;
};

class BufferPool {
public:
    BufferPool(int pool_size, BUFF_MANAGEMENT management_strategy);
    void read_block(int block_id, char *buffer);
    void write_block(int block_id, const char* buffer);
    void flush();
    ~BufferPool();
private:
    // std::vector<BufferBlock> buffer_pool_;                          // Buffer pool
    std::unordered_map<int, BufferBlock> buffer_map_;               // Map of block IDs to buffer blocks
    int pool_size_;                                                 // Size of the buffer pool
    BUFF_MANAGEMENT TYPE;
    std::deque<int> block_access_pattern;                           // used for LRU and MRU
    int clock_hand;                                                 // used for clock policy algorithm

    BufferBlock& load_from_disk(int block_id);
    void update_access(int block_id);
    void evict_block();
    void evict_LRU();
    void evict_MRU();
    void evict_CLOCK();
};

#endif