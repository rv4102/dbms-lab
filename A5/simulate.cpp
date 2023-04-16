#include "buffer.hpp"
#include <iostream>
#include <fstream>
#include <cstring>

using namespace std;

struct Record {
    int id;
    char name[20];
};

void write_to_file(const char *filename, Record& rec){
    ofstream output(filename, ios::binary | ios::app);
    output.write(reinterpret_cast<char*>(&rec), BLOCK_SIZE);
    output.close();
}

void populate_records(){
    // add 2 entries to employees.bin
    Record rec1 = {1, "John"};
    Record rec2 = {2, "Mary"};
    write_to_file("employees.bin", rec1);
    write_to_file("employees.bin", rec2);

    // add 1 entry to departments.bin
    Record rec3 = {1, "Sales"};
    write_to_file("departments.bin", rec3);
}

// Load records from a binary file into the buffer pool
void load_records(BufferPool& pool, int start_block, int num_blocks, const char* filename) {
    ifstream input(filename, ios::binary);
    char buffer[BLOCK_SIZE];
    for (int i = 0; i < num_blocks; i++) {
        input.read(buffer, BLOCK_SIZE);
        pool.write_block(start_block + i, buffer);
    }
}

int main() {
    // Create a buffer pool with LRU eviction strategy and a size of 3 blocks
    BufferPool pool(3, LRU);
    populate_records();

    // Load the records for the "employees" table
    load_records(pool, 0, 2, "employees.bin");

    // Load the records for the "departments" table
    load_records(pool, 2, 1, "departments.bin");

    // Perform a join query between the two tables
    for (int i = 0; i < 2; i++) {
        char buffer1[BLOCK_SIZE], buffer2[BLOCK_SIZE];
        pool.read_block(i, buffer1);
        Record* record1 = reinterpret_cast<Record*>(buffer1);
        cout << record1->id << " " << record1->name << " ";
        for (int j = 0; j < 1; j++) {
            pool.read_block(2 + j, buffer2);
            Record* record2 = reinterpret_cast<Record*>(buffer2);
            cout << record2->id << " " << record2->name << endl;
            if (record1->id == record2->id) {
                cout << record1->id << " " << record1->name << " " << record2->name << endl;
            }
        }
    }

    return 0;
}