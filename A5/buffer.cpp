#include <iostream>
#include <unordered_map>
#include <vector>
#include <cstring>
#include <fstream>
#include <queue>

// Write a block to disk
void write_to_disk(int block_id, const char* buffer) {
    // Open the file in binary mode and seek to the block's position
    std::fstream file("data.bin", std::ios::binary | std::ios::in | std::ios::out);
    file.seekp(block_id * 4096, std::ios::beg);

    // Write the buffer to disk
    file.write(buffer, 4096);

    // Close the file
    file.close();
}


// Read a block from disk
void read_from_disk(int block_id, char* buffer) {
    // Open the file in binary mode and seek to the block's position
    std::fstream file("data.bin", std::ios::binary | std::ios::in | std::ios::out);
    file.seekg(block_id * 4096, std::ios::beg);

    // Read the buffer from disk
    file.read(buffer, 4096);

    // Close the file
    file.close();
}

enum BUFF_MANAGEMENT {LRU, MRU, CLOCK, PIN};

class BufferBlock {
public:
    BufferBlock(): block_id(next_block_id++) {
        // Initialize the buffer with zeros
        memset(buffer_, 0, sizeof(buffer_));
        is_dirty_ = false;
        pin_count_ = 0;
        ref_bit = 1;
    }

    // Getters and setters
    char* get_buffer() { return buffer_; }
    bool is_dirty() const { return is_dirty_; }
    void set_dirty(bool dirty) { is_dirty_ = dirty; }
    int get_pin_count() const { return pin_count_; }
    void pin() { pin_count_++; }
    int get_ref_bit(){ return ref_bit; }
    void set_ref_bit(){ref_bit = 1;}
    void reset_ref_bit() {ref_bit = 0;}

    // once the use of this block is completed, it is the responsibility of the requestor to unpin the block
    // https://cs186berkeley.net/notes/note5/
    void unpin() { pin_count_--; }
    int get_block_id() { return block_id; }

private:
    char buffer_[4096];  // Buffer to hold the data
    bool is_dirty_;      // Flag to indicate if the block has been modified
    int pin_count_;      // Counter to keep track of how many times the block has been pinned
    static int next_block_id;
    int block_id;
    int ref_bit;
};

int BufferBlock::next_block_id = 0;

class BufferPool {
public:
    BufferPool(int pool_size, BUFF_MANAGEMENT management_strategy) : pool_size_(pool_size) {
        // Create the buffer pool
        for (int i = 0; i < pool_size_; i++) {
            buffer_pool_.push_back(BufferBlock());
        }

        // assign the buffer management strategy
        TYPE = management_strategy;
    }

    // Get a buffer block from the pool
    char* get_buffer_block(int block_id) {
        // Check if the block is already in the pool
        auto it = buffer_map_.find(block_id);
        if (it != buffer_map_.end()) {
            // Block is in the pool, return its buffer
            it->second.pin();
            update_access(block_id);
            return it->second.get_buffer();
        }

        // Block is not in the pool, load it from disk
        BufferBlock& block = load_from_disk(block_id);
        clock_hand = block_id; // set the clock_hand to point to a unpinned block

        // Add the block to the pool
        if (buffer_map_.size() >= pool_size_) {
            // Pool is full, evict a block
            evict_block();

            // if after evicting a block, the pool is still full then error
            if (buffer_map_.size() >= pool_size_) {
                std::cerr << "Error: Buffer pool is full" << std::endl;
                exit(1);
            }
        }
        buffer_map_[block_id] = block;

        // Return the buffer
        block.pin();
        update_access(block_id);
        return block.get_buffer();
    }

    // Flush dirty blocks to disk
    void flush() {
        for (auto& pair : buffer_map_) {
            if (pair.second.is_dirty()) {
                write_to_disk(pair.first, pair.second.get_buffer());
                pair.second.set_dirty(false);
            }
        }
    }

    // Destructor
    ~BufferPool() {
        flush();
    }

private:
    std::vector<BufferBlock> buffer_pool_;                          // Buffer pool
    std::unordered_map<int, BufferBlock> buffer_map_;               // Map of block IDs to buffer blocks
    int pool_size_;                                                 // Size of the buffer pool
    BUFF_MANAGEMENT TYPE;
    std::deque<int> block_access_pattern;                           // used for LRU and MRU
    int clock_hand;                                                 // used for clock policy algorithm

    // Load a block from disk
    BufferBlock& load_from_disk(int block_id) {
        // Read the block from disk into a new buffer block
        BufferBlock block;
        read_from_disk(block_id, block.get_buffer());

        // Return the new block
        return block;
    }

    void update_access(int block_id){
        if(TYPE == LRU || TYPE == MRU){
            auto block_access_it = std::find(block_access_pattern.begin(), block_access_pattern.end(), block_id);
            if(block_access_it != block_access_pattern.end()){
                block_access_pattern.erase(block_access_it);
            }
            block_access_pattern.push_front(block_id);
        }
        else if(TYPE == CLOCK){
            buffer_map_[block_id].set_ref_bit();
        }
    }

    // Evict a block from the pool
    void evict_block() {
        switch(TYPE){
            case LRU:
            evict_LRU();
            break;

            case MRU:
            evict_MRU();
            break;

            case CLOCK:
            evict_CLOCK();
            break;

            case PIN:
            evict_PIN();
            break;
        }
    }

    void evict_LRU(){
        // iterate over the block_access_pattern from the back and find a block_id with pin_count_ == 0
        for(auto block_access_it = block_access_pattern.rbegin(); block_access_it != block_access_pattern.rend(); block_access_it++){
            auto buffer_map_it = buffer_map_.find(*block_access_it);
            if(buffer_map_it->second.get_pin_count() == 0){
                // found a block_id with pin_count_ == 0
                // evict this block
                if(buffer_map_it->second.is_dirty()){
                    write_to_disk(buffer_map_it->first, buffer_map_it->second.get_buffer());
                }
                buffer_map_.erase(buffer_map_it);
                block_access_pattern.erase(std::next(block_access_it).base());
                return;
            }
        }
    }

    void evict_MRU(){
        // iterate over the block_access_pattern from the front and find a block_id with pin_count_ == 0
        for(auto block_access_it = block_access_pattern.begin(); block_access_it != block_access_pattern.end(); block_access_it++){
            auto buffer_map_it = buffer_map_.find(*block_access_it);
            if(buffer_map_it->second.get_pin_count() == 0){
                // found a block_id with pin_count_ == 0
                // evict this block
                if(buffer_map_it->second.is_dirty()){
                    write_to_disk(buffer_map_it->first, buffer_map_it->second.get_buffer());
                }
                buffer_map_.erase(buffer_map_it);
                block_access_pattern.erase(block_access_it);
                return;
            }
        }
    }

    void evict_CLOCK(){
        // // iterate over the buffer_map_ starting from the clock_hand and find a block_id with pin_count_ == 0 and ref_bit == 0
        // for(auto buffer_map_it = buffer_map_.begin(); buffer_map_it != buffer_map_.end(); buffer_map_it++){
        //     if(buffer_map_it->second.get_pin_count() == 0 && buffer_map_it->second.get_ref_bit() == 0){
        //         // found a block_id with pin_count_ == 0 and ref_bit == 0
        //         // evict this block
        //         if(buffer_map_it->second.is_dirty()){
        //             write_to_disk(buffer_map_it->first, buffer_map_it->second.get_buffer());
        //         }
        //         buffer_map_.erase(buffer_map_it);
        //         return;
        //     }
        //     else{
        //         // set ref_bit to 0
        //         buffer_map_it->second.reset_ref_bit();
        //     }
        // }

        /*
        Iterate through frames within the table, skipping pinned pages and wrapping around to frame 0 upon reaching the end, until the first unpinned frame with ref bit = 0 is found.
        */
        int start = clock_hand;
        do{
            if(buffer_map_[clock_hand].get_pin_count() == 0){
                if(buffer_map_[clock_hand].get_ref_bit() == 0){
                    // found a block_id with pin_count_ == 0 and ref_bit == 0
                    // evict this block
                    if(buffer_map_[clock_hand].is_dirty()){
                        write_to_disk(clock_hand, buffer_map_[clock_hand].get_buffer());
                    }
                    buffer_map_.erase(clock_hand);
                    return;
                }
                else{
                    // set ref_bit to 0
                    buffer_map_[clock_hand].reset_ref_bit();
                }
            }
            clock_hand = (clock_hand + 1) % pool_size_;
        }while(clock_hand != start);
    }

    void evict_PIN(){

    }

};