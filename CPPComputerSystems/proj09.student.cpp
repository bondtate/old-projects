/*****************************************************************************
Name: Tate Bond
Computer Project 9
*****************************************************************************/

#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>
#include <vector>
#include <math.h>

using namespace std;

typedef unsigned short int uint16;

// One row in the page table
struct table_data{
	unsigned int index;
	bool v;
	bool w;
	bool p;
	bool r;
	bool m;
	uint16 fn;
};

// Data Structure representing a page table
class PageTable{
	private:
		struct table_data table[16];
	public:

		// Initialize the table to 0
		PageTable(){
			for (unsigned i=0; i<16; i++){
				table_data temp= {i, 0, 0, 0, 0, 0, 0};
				table[i] = temp;
			}
		}

		// Replace a row with the given row
		void edit_row(table_data row){
                        for (unsigned i=0; i<16; i++){
                                if (row.index == table[i].index){
					table[i] = row;
				}
                        }
		}

		// Display the contents of the table
		void display(){
			cout << "     V W P R M FN" << endl;
			cout << "------------------" << endl;

			stringstream hex_index;
			stringstream hex_fn;
                        for (unsigned i=0; i<16; i++){
				hex_index.str("");
				hex_index.clear();
                                hex_fn.str("");
                                hex_fn.clear();

				hex_index << hex << table[i].index;
				hex_fn << setfill('0') << 
					std::setw(sizeof(uint16)) << 
					hex << table[i].fn;

                                cout << "[" << hex_index.str() << "]: ";
				cout << table[i].v << " ";
				cout << table[i].w << " ";
                                cout << table[i].p << " ";
                                cout << table[i].r << " ";
                                cout << table[i].m << " ";
                                cout << hex_fn.str() << endl;
                        }
		}
};

int main(int argc, char* argv[]){

	string proc = "";               // Process to load
        bool is_debug = false;          // Debug option selected
        string refs = "";       	// Refs to load

        //Loop through the arguments and set variables based on input
        int count = 1;                  //count for iterating loop
        while(count < argc){
                string input = string( argv[count] );   //convert arg to string

                if(input[0] == '-'){
                        if(input == "-debug"){
                                is_debug = true;
                        }
                        else if(input == "-proc"){
                                proc = string( argv[count + 1] );
                                count += 1;
                        }
                        else if(input == "-refs"){
                                refs = string( argv[count + 1] );
                                count += 1;
                        }
                        else{
                                cout << "Error: Incorrect input" << endl;
                                return 0;
                        }
                }
                else{
                        cout << "Error: Incorrect input" << endl;
                        return 0;
                }
                count += 1;
        }

	// If input files aren't given return
	if (proc == "" || refs == ""){
		cout << "Error: Incorrect input" << endl;
		return 0;
	}

	PageTable table;			// PageTabel Data Structure
	
        ifstream working_file(proc);
        stringstream word_stream;
        stringstream hex_stream;
        string line;

        unsigned int index;
        bool is_wr;

        if(working_file.is_open()){

                // Loop through the contents of the working_file
                while(getline(working_file, line)){
                        word_stream.str("");
                        word_stream.clear();
			hex_stream.str("");
                        hex_stream.clear();

                        hex_stream << hex << line[0];
                        hex_stream >> index;

                        word_stream << line[2];
                        word_stream >> is_wr;
			
			// Replace with row in table with data from file
			table_data row = {index, 1, is_wr, 0, 0, 0, 0};
			table.edit_row(row);
                }

		if (is_debug){
			cout << "Simulation Start" << endl;
			table.display();
			cout << endl;
		}
        }
        else{
                cout << "Error: File does not exist" << endl;
		return 0;
        }
	
        ifstream working_file_one(refs);
        stringstream word_stream_one;
	stringstream word_hex;
        string line_one;
	string instruct = "";
	int address;
	int page;
	int offset;

	int rd_count = 0;
	int wr_count = 0;

	stringstream hex_add;
        stringstream hex_page;
        stringstream hex_offset;

        if(working_file_one.is_open()){

                // Loop through the contents of the working_file
                while(getline(working_file_one, line_one)){

                        word_stream_one.str("");
			word_hex.str("");
                        word_stream_one.clear();
                        word_hex.clear();

			hex_add.str("");
                        hex_page.str("");
                        hex_offset.str("");
			hex_add.clear();
                        hex_page.clear();
                        hex_offset.clear();

                        word_hex << hex << line_one.substr(3, 7);
                        word_hex >> address;

			page = floor(address / 1024);
			offset = address % 1024;

                        word_stream_one << line_one;
                        word_stream_one >> instruct;

			if (instruct == "RD"){
				rd_count += 1;
			}
			else if (instruct == "WR"){
				wr_count += 1;			
			}
			else{
				cout << "Invalid instruction" << endl;
				return 0;
			}

			hex_add << setfill('0') << setw(sizeof(int)) << 
				hex << address;

			hex_page << setfill ('0') << setw(sizeof(int)/4) << 
				hex << page;

			hex_offset << setfill ('0') << setw(sizeof(int)-1) << 
				hex << offset;

			// Print the current instruction, address and page number
			cout << instruct << " " << 
				hex_add.str() << " " << 
				hex_page.str() << " " << 
				hex_offset.str() << endl;

			if (is_debug){
				table.display();
				cout << endl;
			}
                }

		if (!is_debug){
			cout << endl;
			table.display();
		}
		cout << endl;
		cout << "Read Count: " << rd_count << endl;
		cout << "Write Count: " << wr_count << endl;
		cout << endl;
        }
        else{
                cout << "Error: File does not exist" << endl;
		return 0;
        }
}
