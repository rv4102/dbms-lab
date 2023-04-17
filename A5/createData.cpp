#include <iostream>
#include <fstream>
#include <string>

#define PAGE_SIZE 4096
#define NUM_RECORDS 1000
using namespace std;

// make a struct for database
typedef struct{
    char name[20];
    int grade;
    int rollno;
}Student;

void fill_data(Student *p){
    for(int i=0; i<NUM_RECORDS; i++){
        string name = "abc" + to_string(i);
        strcpy(p[i].name, name.c_str());
        p[i].grade = rand()%12+1;
        p[i].rollno = rand()%100+1;
        cout<<p[i].name<<" "<<p[i].grade<<" "<<p[i].rollno<<endl;
    }
}

int main(){
    FILE *file_pointer;
    file_pointer = fopen("data.bin", "wb");

    Student p[NUM_RECORDS];
    fill_data(p);

    int recordSize = sizeof(Student);

    // add first 4 bytes in page 1 as number of records in last page
    int i=0, totalRecords = NUM_RECORDS;
    while(1){
        // starting of each page add number of records in this page
        int possible = (PAGE_SIZE - 4)/recordSize; // max number of records that can be stored in a page
        int recordsInPage = min(possible, totalRecords); // number of records in this page

        fwrite(&recordsInPage, sizeof(int), 1, file_pointer);
        totalRecords -= recordsInPage;

        int numLeft = PAGE_SIZE;
        numLeft -= sizeof(int);

        while(numLeft >= recordSize){
            fwrite(&p[i], recordSize, 1, file_pointer);
            numLeft -= recordSize;
            i++;
            if(i==NUM_RECORDS){
                break;
            }
        }
        while(numLeft > 0){
            char c = '\0';
            fwrite(&c, sizeof(char), 1, file_pointer);
            numLeft--;
        }
        if(i==NUM_RECORDS){
            break;
        }
    }

    fclose(file_pointer);
}