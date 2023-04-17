#include "simulate.hpp"
#include <iostream>
#include <fstream>
#include <string>

// constructor for QueryProcessor
simulate::simulate(int numFrames, policy policyType){
    if(policyType == CLOCK) bufferManager = new ClockBufferManager(numFrames);
    else if(policyType == LRU) bufferManager = new LRUBufferManager(numFrames);
    else if(policyType == MRU) bufferManager = new MRUBufferManager(numFrames);
    else{
        cout << "Invalid replacement policy\n";
        exit(1);
    }
}

// process a select from query
void simulate::processSelectQuery(FILE *file_pointer, int col1, string value){
    int numPages = 0;
    int recordSize = 20*sizeof(char) + 2*sizeof(int);

    // get number of pages
    fseek(file_pointer, 0, SEEK_END);
    numPages = ftell(file_pointer)/PAGE_SIZE;
    fseek(file_pointer, 0, SEEK_SET);

    // iterate over all pages
    for(int i=0;i<numPages;++i){
        // get page from buffer
        char *data = bufferManager->getPage(file_pointer, i);
        int numLeft = PAGE_SIZE;
        int numRecords;
        memcpy(&numRecords, data, sizeof(int));
        data += sizeof(int);
        while(numRecords--){
            char name[20];
            int grade;
            int rollno;
            memcpy(name, data,20*sizeof(char));
            memcpy(&grade, data+20*sizeof(char), sizeof(int));
            memcpy(&rollno, data+20*sizeof(char)+sizeof(int), sizeof(int));
            data += recordSize;
            numLeft -= recordSize;
            if(col1==2 && grade == atoi(value.c_str())){
                cout<<name<<" "<<grade<<" "<<rollno<<endl;
            }
            else if(col1==3 && rollno == atoi(value.c_str())){
                cout<<name<<" "<<grade<<" "<<rollno<<endl;
            }
            else if(col1==1 && value == name){
                cout<<name<<" "<<grade<<" "<<rollno<<endl;
            }
        }
        // unpin page
        bufferManager->unpinPage(file_pointer, i);
    }
    cout << "----------------------- Query Statistics -----------------------\n";
    cout<<"Page Accesses: " << bufferManager->getStats().accesses << endl;
    cout<<"Page fault and Disk Reads: " << bufferManager->getStats().diskReads << endl;
    cout<<"Page Hits: " << bufferManager->getStats().pageHits << endl;

}


void simulate::processJoinQuery(FILE *file_pointer1, FILE *file_pointer2, int col1, int col2){
    int numPages1 = 0;
    int recordSize1 = 20*sizeof(char) + 2*sizeof(int);

    int numPages2 = 0;
    int recordSize2 = 20*sizeof(char) + 2*sizeof(int);
    // get number of pages
    fseek(file_pointer1, 0, SEEK_END);
    numPages1 = ftell(file_pointer1)/PAGE_SIZE;
    fseek(file_pointer1, 0, SEEK_SET);

    fseek(file_pointer2, 0, SEEK_END);
    numPages2 = ftell(file_pointer2)/PAGE_SIZE;
    fseek(file_pointer2, 0, SEEK_SET);

    for(int i=0;i<numPages1;++i){
        char* data1 = bufferManager->getPage(file_pointer1, i);        
        if(data1 == NULL){
            cout<<"Number of Frames is too small\n";
            exit(0);
        }
        for(int j=0;j<numPages2;++j){
            char* data2 = bufferManager->getPage(file_pointer2, j);
            if(data2 == NULL){
                cout<<"Number of Frames is too small\n";
                exit(0);
            }
            int x = 0;
            int page1Offset = 0;
            int numRecords1;
            memcpy(&numRecords1, data1, sizeof(int));
            page1Offset += sizeof(int);
            while(numRecords1--){
                char name1[20];
                x++;
                int age1;
                int weight1;
                int page2Offset = 0;
                memcpy(name1, data1+page1Offset,20*sizeof(char));
                memcpy(&age1, data1+page1Offset+20*sizeof(char), sizeof(int));
                memcpy(&weight1, data1+page1Offset+20*sizeof(char)+sizeof(int), sizeof(int));
                page1Offset += recordSize1;
                int numRecords2;
                memcpy(&numRecords2, data2, sizeof(int));
                page2Offset += sizeof(int);
                while(numRecords2--){
                    char name2[20];
                    int age2;
                    int weight2;
                    memcpy(name2, data2+page2Offset,20*sizeof(char));
                    memcpy(&age2, data2+page2Offset+20*sizeof(char), sizeof(int));
                    memcpy(&weight2, data2+page2Offset+20*sizeof(char)+sizeof(int), sizeof(int));
                    page2Offset += recordSize2;
                    string allCols1[3];
                    allCols1[0] = name1;
                    allCols1[1] = to_string(age1);
                    allCols1[2] = to_string(weight1);
                    string allCols2[3];
                    allCols2[0] = name2;
                    allCols2[1] = to_string(age2);
                    allCols2[2] = to_string(weight2);
                    if(allCols1[col1-1] == allCols2[col2-1]){
                        cout<<name1<<" "<<age1<<" "<<weight1<<" "<<name2<<" "<<age2<<" "<<weight2<<endl;
                    }
                }
            }
            bufferManager->unpinPage(file_pointer2, j);
        }
        bufferManager->unpinPage(file_pointer1, i);
    }
    cout << "----------------------- Query Statistics -----------------------\n";
    cout<<"Page Accesses: "<<bufferManager->getStats().accesses<<endl;
    cout<<"Page fault and Disk Reads: "<<bufferManager->getStats().diskReads<<endl;
    cout<<"Page Hits: "<<bufferManager->getStats().pageHits<<endl;

}

int main(){
    FILE *file_pointer1 = fopen("data.bin", "rb");
    FILE *file_pointer2 = fopen("data.bin", "rb");

    cout << "The following replacement algorithms are available:\n1: LRU, 2: MRU, 3: CLOCK\nEnter choice: ";
    int choice;
    cin >> choice;

    if(choice<1 || choice>3){
        cout<<"Invalid choice\n";
        exit(1);
    }

    cout<<"Enter number of frames: ";
    int numFrames;
    cin >> numFrames;

    simulate s(numFrames, (policy)choice);

    cout<<"Enter 1 for select query, 2 for join query: ";
    int queryType;
    cin>>queryType;

    if(queryType == 1){
        cout<<"Enter column number of Database: ";
        int col;
        cin>>col;
        cout<<"Enter value to get all matching records: ";
        string value;
        cin>>value;
        s.processSelectQuery(file_pointer1, col, value);
    }
    else if(queryType == 2){
        cout<<"Enter column number of Database 1: ";
        int col1;
        cin>>col1;
        cout<<"Enter column number of Database 2: ";
        int col2;
        cin>>col2;
        s.processJoinQuery(file_pointer1, file_pointer2, col1, col2);
    }
    else{
        cout<<"Invalid query type\n";
        exit(1);
    }

    fclose(file_pointer1);
    fclose(file_pointer2);
}