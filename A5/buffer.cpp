#include "buffer.hpp"
#include <iostream>
#include <vector>
#include <cstring>
#include <fstream>

// Write a block to disk
void write_to_disk(int block_id, const char *buffer)
{
    // Open the file in binary mode and seek to the block's position
    std::fstream file("data.bin", std::ios::binary | std::ios::in | std::ios::out);
    file.seekp(block_id * BLOCK_SIZE, std::ios::beg);

    // Write the buffer to disk
    file.write(buffer, BLOCK_SIZE);

    // Close the file
    file.close();
}

// Read a block from disk
void read_from_disk(int block_id, char *buffer)
{
    // Open the file in binary mode and seek to the block's position
    std::fstream file("data.bin", std::ios::binary | std::ios::in | std::ios::out);
    file.seekg(block_id * BLOCK_SIZE, std::ios::beg);

    // Read the buffer from disk
    file.read(buffer, BLOCK_SIZE);

    // Close the file
    file.close();
}

BufferBlock::BufferBlock() : block_id(next_block_id++)
{
    // Initialize the buffer with zeros
    memset(buffer_, 0, sizeof(buffer_));
    is_dirty_ = false;
    pin_count_ = 0;
    ref_bit = 1;
}
int BufferBlock::next_block_id = 0;

char *BufferBlock::get_buffer() { return buffer_; }
bool BufferBlock::is_dirty() const { return is_dirty_; }
void BufferBlock::set_dirty(bool dirty) { is_dirty_ = dirty; }
int BufferBlock::get_pin_count() const { return pin_count_; }
void BufferBlock::pin() { pin_count_++; }
// once the use of this block is completed, it is the responsibility of the requestor to unpin the block
// https://cs186berkeley.net/notes/note5/
void BufferBlock::unpin() { pin_count_--; }
int BufferBlock::get_ref_bit() { return ref_bit; }
void BufferBlock::set_ref_bit() { ref_bit = 1; }
void BufferBlock::reset_ref_bit() { ref_bit = 0; }
int BufferBlock::get_block_id() { return block_id; }

BufferPool::BufferPool(int pool_size, BUFF_MANAGEMENT management_strategy) : pool_size_(pool_size)
{
    // // Create the buffer pool
    // for (int i = 0; i < pool_size_; i++) {
    //     buffer_pool_.push_back(BufferBlock());
    // }

    // assign the buffer management strategy
    TYPE = management_strategy;
}

void BufferPool::read_block(int block_id, char *buffer){
    // Check if the block is already in the pool
    auto it = buffer_map_.find(block_id);
    if (it != buffer_map_.end())
    {
        // Block is in the pool, return its buffer
        it->second.pin();
        update_access(block_id);
        memcpy(buffer, it->second.get_buffer(), BLOCK_SIZE);
        return;
    }

    // Block is not in the pool, load it from disk
    BufferBlock &block = load_from_disk(block_id);
    clock_hand = block_id; // set the clock_hand to point to a unpinned block

    // Add the block to the pool
    if (buffer_map_.size() >= pool_size_)
    {
        // Pool is full, evict a block
        evict_block();

        // if after evicting a block, the pool is still full then error
        if (buffer_map_.size() >= pool_size_)
        {
            std::cerr << "Error: Buffer pool is full" << std::endl;
            exit(1);
        }
    }
    buffer_map_[block_id] = block;

    // Return the buffer
    block.pin();
    update_access(block_id);
    memcpy(buffer, block.get_buffer(), BLOCK_SIZE);
    return;
}

void BufferPool::write_block(int block_id, const char *buffer)
{
    // Check if the block is already in the pool
    auto it = buffer_map_.find(block_id);
    if (it != buffer_map_.end())
    {
        // Block is in the pool, write to the buffer
        memcpy(it->second.get_buffer(), buffer, BLOCK_SIZE);
        it->second.set_dirty(true);
    }
    else
    {
        // Block is not in the pool, load it from disk
        BufferBlock &block = load_from_disk(block_id);
        clock_hand = block_id; // set the clock_hand to point to a unpinned block

        // Add the block to the pool
        if (buffer_map_.size() >= pool_size_)
        {
            // Pool is full, evict a block
            evict_block();

            // if after evicting a block, the pool is still full then error
            if (buffer_map_.size() >= pool_size_)
            {
                std::cerr << "Error: Buffer pool is full" << std::endl;
                exit(1);
            }
        }
        buffer_map_[block_id] = block;

        // Write to the buffer
        memcpy(block.get_buffer(), buffer, BLOCK_SIZE);
        block.set_dirty(true);
    }
}

// Flush dirty blocks to disk
void BufferPool::flush()
{
    for (auto &pair : buffer_map_)
    {
        if (pair.second.is_dirty())
        {
            write_to_disk(pair.first, pair.second.get_buffer());
            pair.second.set_dirty(false);
        }
    }
}

// Destructor
BufferPool::~BufferPool()
{
    flush();
}

// Load a block from disk
BufferBlock & BufferPool::load_from_disk(int block_id)
{
    // Read the block from disk into a new buffer block
    BufferBlock block;
    read_from_disk(block_id, block.get_buffer());

    // Return the new block
    return block;
}

void BufferPool::update_access(int block_id)
{
    if (TYPE == LRU || TYPE == MRU)
    {
        auto block_access_it = std::find(block_access_pattern.begin(), block_access_pattern.end(), block_id);
        if (block_access_it != block_access_pattern.end())
        {
            block_access_pattern.erase(block_access_it);
        }
        block_access_pattern.push_front(block_id);
    }
    else if (TYPE == CLOCK)
    {
        buffer_map_[block_id].set_ref_bit();
    }
}

// Evict a block from the pool
void BufferPool::evict_block()
{
    switch (TYPE)
    {
    case LRU:
        evict_LRU();
        break;

    case MRU:
        evict_MRU();
        break;

    case CLOCK:
        evict_CLOCK();
        break;
    }
}

void BufferPool::evict_LRU()
{
    // iterate over the block_access_pattern from the back and find a block_id with pin_count_ == 0
    for (auto block_access_it = block_access_pattern.rbegin(); block_access_it != block_access_pattern.rend(); block_access_it++)
    {
        auto buffer_map_it = buffer_map_.find(*block_access_it);
        if (buffer_map_it->second.get_pin_count() == 0)
        {
            // found a block_id with pin_count_ == 0
            // evict this block
            if (buffer_map_it->second.is_dirty())
            {
                write_to_disk(buffer_map_it->first, buffer_map_it->second.get_buffer());
            }
            buffer_map_.erase(buffer_map_it);
            block_access_pattern.erase(std::next(block_access_it).base());
            return;
        }
    }
}

void BufferPool::evict_MRU()
{
    // iterate over the block_access_pattern from the front and find a block_id with pin_count_ == 0
    for (auto block_access_it = block_access_pattern.begin(); block_access_it != block_access_pattern.end(); block_access_it++)
    {
        auto buffer_map_it = buffer_map_.find(*block_access_it);
        if (buffer_map_it->second.get_pin_count() == 0)
        {
            // found a block_id with pin_count_ == 0
            // evict this block
            if (buffer_map_it->second.is_dirty())
            {
                write_to_disk(buffer_map_it->first, buffer_map_it->second.get_buffer());
            }
            buffer_map_.erase(buffer_map_it);
            block_access_pattern.erase(block_access_it);
            return;
        }
    }
}

void BufferPool::evict_CLOCK()
{
    int start = clock_hand;
    do
    {
        if (buffer_map_[clock_hand].get_pin_count() == 0)
        {
            if (buffer_map_[clock_hand].get_ref_bit() == 0)
            {
                // found a block_id with pin_count_ == 0 and ref_bit == 0
                // evict this block
                if (buffer_map_[clock_hand].is_dirty())
                {
                    write_to_disk(clock_hand, buffer_map_[clock_hand].get_buffer());
                }
                buffer_map_.erase(clock_hand);
                return;
            }
            else
            {
                // set ref_bit to 0
                buffer_map_[clock_hand].reset_ref_bit();
            }
        }
        clock_hand = (clock_hand + 1) % pool_size_;
    } while (clock_hand != start);
}