/*****************************************************************************
Name: Tate Bond
Computer Project 7
*****************************************************************************/

#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>

using namespace std;

typedef unsigned short int uint16;

struct data{
        bool v_bit = 0;
        bool m_bit = 0;
        uint16 tag_bits;
        uint16 block[8];
};

class Cache{

	private:
		struct data cache[8];

	public:

		Cache(){
			for (unsigned i=0; i<8; i++){
				data temp = {};
				for (unsigned j=0; j<8; j++){
					temp.block[j] = 0x00;
				}
                                for (unsigned j=0; j<8; j++){
                                        cout << temp.block[j] << endl;
                                }
				cache[i] = temp;
			}
		}

	       
		data operator[]( unsigned I )
		{
			return cache[I];
		}

		const data& operator[]( unsigned I ) const
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
	
        ifstream working_file(instructions);
        stringstream word_stream;
        string line;

        string instruction;
        string reg;
        string phy_add;

        if(working_file.is_open()){

                // Loop through the contents of the working_file
                while(getline(working_file, line)){
                        word_stream.str("");
                        word_stream.clear();

                        word_stream << line;
                        word_stream >> instruction;
                        word_stream >> reg;
                        word_stream >> phy_add;

			cout << instruction << " " << reg << " " << phy_add <<
endl;
                }
        }
        else{
                cout << "Error: File does not exist" << endl;
        }
}
