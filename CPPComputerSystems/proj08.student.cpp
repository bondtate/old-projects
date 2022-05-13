/*****************************************************************************
Name: Tate Bond
Computer Project 8
*****************************************************************************/

#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>
#include <vector>

using namespace std;

typedef unsigned short int uint16;

struct cache_data{
        bool v_bit = 0;
        bool m_bit = 0;
        uint16 tag_bits;
        uint16 block[8];
};

struct ram_data{
	int address = 0;
	uint16 block[16];
};

class Ram{

        private:
                struct ram_data ram[4096];

        public:
                Ram(){
                        for (unsigned i=0; i<4096; i++){
                                ram_data temp = {};
				temp.address = i * 16;
                                for (unsigned j=0; j<16; j++){
                                        temp.block[j] = 0x00;
                                }
                                ram[i] = temp;
                        }
                }

		// Add a block to ram
		void add_ram(int address, uint16 data[16]){
			
			for (unsigned int i=0; i<4096; i++){
				if (ram[i].address == address){
					for (unsigned int j=0; j<16; j++){
						ram[i].block[j] = data[j];
					}
				}
			}
		}

		void display(){
                        for (unsigned int i=0; i<8; i++){

                                stringstream stream;
                                stream << std::setfill ('0') <<
std::setw(sizeof(int)) << std::hex << ram[i].address;
                                cout << stream.str() << ": ";

                                for (unsigned j=0; j<16; j++){
					stream.str("");
                                        stream.clear();
                                        stream << std::setfill ('0') <<
std::setw(sizeof(uint16)) << std::hex << ram[i].block[j];
                                        cout << stream.str() << " ";
                                }
                                cout << endl;
                        }
                        cout << endl;
		}

		// Get ram
                vector<uint16> pull_ram(int address){

                        vector<uint16> r_vec;

                        for (unsigned int i=0; i<4096; i++){
                                if (ram[i].address == address){
                                        for (unsigned int j=0; j<16; j++){
                                                r_vec.push_back(ram[i].block[j]);
                                        }
                                }
                        }
                        return r_vec;
                }

		// Get ram
		vector<uint16> get_ram(int address, int offset){

			vector<uint16> r_vec;

                        for (unsigned int i=0; i<4096; i++){
                                if (ram[i].address == address){
                                        for (unsigned int j=offset; j<offset+2; j++){
                                                r_vec.push_back(ram[i].block[j]);
                                        }
                                }
                        }
			return r_vec;
		}
		
};

class Cache{

	private:
		struct cache_data cache[8];

	public:

		Cache(){
			for (unsigned i=0; i<8; i++){
				cache_data temp = {};
                                        temp.v_bit = 0;
                                        temp.m_bit = 0;
                                        temp.tag_bits = 0;
				for (unsigned j=0; j<8; j++){
					temp.block[j] = 0x00;
				} 
				cache[i] = temp;
			}
		}

		vector<uint16> load_cache(Ram r, int address){

			vector<uint16> ram_block = r.pull_ram(address);
			int offset = 0x0003 & address;
			int location = 0x000c & address;
			int tag = 0xfff0 & address;
				
			struct cache_data working_cache = cache[location];
			uint16 block[8];
			if (working_cache.tag_bits == tag){
				for (unsigned int i=0; i<8; i++){
					block[i] = working_cache.block[i];
				}
			}
			else{
				for (unsigned int i=0; i<8; i++){
                                        block[i] = working_cache.block[i];
                                }
			}
		}

	       
		cache_data operator[]( unsigned I )
		{
			return cache[I];
		}

		const cache_data& operator[]( unsigned I ) const
		{
	           	return cache[I];
		}

		void display( std::ostream& out ) const
		{ 
			std::ios old( nullptr );
			old.copyfmt( out );
	      
			out << std::setfill( '0' ) << std::hex;
	      
			/*for (unsigned i=0; i<4; i++){ 
				unsigned n = i;
				out << "R" << std::setw(1) << n << ": "
				<< std::setw(4) << cache[n] << "  ";
				n = n+4;
				out << "R" << std::setw(1) << n << ": "
				<< std::setw(4) << cache[n] << "  ";
				n = n+4;
				out << "R" << std::setw(1) << n << ": "
				<< std::setw(4) << cache[n] << "  ";
				n = n+4;
				out << "R" << std::setw(1) << n << ": "
				<< std::setw(4) << cache[n] << std::endl;
			}
	      
			out.copyfmt( old );*/
    		}	
};

class RegisterUnit{
 	 private:

    		uint16 reg[16];

  	 public:

    	 // Construct and initialize
    	 //
    	 RegisterUnit(){
     		for (unsigned i=0; i<16; i++)
       		reg[i] = 0x00;
   	 }

    	 // Return reference to element I
    	 //
    	 uint16& operator[]( unsigned I ){
      	 	return reg[I&0xf];
    	 }

    	 // Return constant reference to element I
    	 //
    	 const uint16& operator[]( unsigned I ) const{
      	 	return reg[I&0xf];
    	 }

	 // Display RegisterUnit
	 //
	 void display( std::ostream& out ) const{
	      std::ios old( nullptr );
	      old.copyfmt( out );

	      out << std::setfill( '0' ) << std::hex;

	      for (unsigned i=0; i<4; i++){
			unsigned n = i;
			out << "R" << std::setw(1) << n << ": "
		    		<< std::setw(4) << reg[n] << "  ";
			n = n+4;
			out << "R" << std::setw(1) << n << ": "
		    		<< std::setw(4) << reg[n] << "  ";
			n = n+4;
			out << "R" << std::setw(1) << n << ": "
		    		<< std::setw(4) << reg[n] << "  ";
			n = n+4;
			out << "R" << std::setw(1) << n << ": "
		    		<< std::setw(4) << reg[n] << std::endl;
	      }

	      out.copyfmt( old );
	}
};

int main(int argc, char* argv[]){
 	//Cache cache;
	//cache.display(std::cout);
        string ram = "";            	// RAM to load
        bool is_debug = false;      	// Debug option selected
        string instructions = "";       // File of instructions

        //Loop through the arguments and set variables based on input
        int count = 1;                  //count for iterating loop
        while(count < argc){
                string input = string( argv[count] );   //convert arg to string

                if(input[0] == '-'){
                        if(input == "-debug"){
                                is_debug = true;
                        }
                        else if(input == "-ram"){
                                ram = string( argv[count + 1] );
                                count += 1;
                        }
			else if(input == "-input"){
				instructions = string( argv[count + 1] );
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

        ifstream working_file_r(ram);
        stringstream word_stream_r;
        Ram r;
	Cache c;
        uint16 block[16];
        int address = 0;
        string line_r;

        if(working_file_r.is_open()){

                // Loop through the contents of the working_file
                while(getline(working_file_r, line_r)){
                        word_stream_r.str("");
                        word_stream_r.clear();

                        word_stream_r << hex << line_r;
                        word_stream_r >> address;
                        uint16 temp;
                        for (unsigned int i=0; i<16; i++){
                                word_stream_r >> temp;
                                block[i] = temp;
                        }
                        r.add_ram(address, block);
                } 
        }
        else{
                cout << "Error: File does not exist" << endl;
        }
	
        ifstream working_file(instructions);
        stringstream word_stream;
        stringstream word_stream_2;
        string line;

        string instruction;
        string reg;
        int phy_add;

        if(working_file.is_open()){

                // Loop through the contents of the working_file
                while(getline(working_file, line)){
                        word_stream.str("");
                        word_stream.clear();
			word_stream_2.clear();

			word_stream_2 << hex << line.substr(6, 10);
                        word_stream_2 >> phy_add;

			word_stream.clear();

                        word_stream << line;
                        word_stream >> instruction;
                        word_stream >> reg;

			vector<uint16> vals = c.load_cache(r, phy_add);
                }
        }
        else{
                cout << "Error: File does not exist" << endl;
        }
	r.display();
}
//
