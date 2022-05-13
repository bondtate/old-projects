/*****************************************************************************
Name: Tate Bond
Computer Project 5
*****************************************************************************/

#include <stdio.h>
#include <iostream>
#include <string>
#include <fcntl.h>
#include <unistd.h>
#include <exception>

using namespace std;

int main(int argc, char* argv[]){

	int a = 0;	// a selected
	int t = 0;	// t selected
	int b = 0;	// b selected
	string source;	// source file
	string dest;	// destination file
	string buffer;	// buffer size

	int index = 1;	// argument index
	while(index < argc){
		
		string command = string(argv[index]);
		if(command[0] == '-'){

			try{

				if(command[1] == 'a'){
					a = 1;
				}
				else if(command[1] == 't'){
					t = 1;
				}
				else if(command[1] == 'b'){
					if(index + 1 < argc){
						buffer = string(argv[index + 1]);
						index += 1;
					}
					else{
						cout << "No Buffer Value Given" << endl;
						return 3;
					}
					b = 1;
				}
				else{
					cout << "Please Enter a valid argument" << endl;
					return 3;
				}
			}catch(exception& e){
				cout << "Please select a valid argument" << endl;
			} 
		}
		
		else if(source.empty()){
			source = command;
		}
		
                else if(!source.empty() && dest.empty()){
                        dest = command;
                }

                else{
                        cout << "Please Enter Valid Input" << endl;
                        return 3;
                }
                index += 1;
	}

	// Get the size of the buffer
	// 64 as default
        int buffer_size = 64;
        try{
                if(b && stoi(buffer) > 1){
                        buffer_size = stoi(buffer);
                }
                else if(b && stoi(buffer) < 1){
                        cout << "Please enter a valid buffer size" << endl;
                        return 3;
                }
        }catch(exception& e){
                cout << "Please enter a valid buffer value" << endl;
                return 3;
        }

	// Check the values of a and t
        if(a && t){
                cout << "Cannot use -a and -t together" << endl;
                return 3;
        }
        if(source.empty() || dest.empty()){
                cout << "Please enter a file argument" << endl;
                return 3;
        }

        int fd_source;                  //source file iterator
        int fd_dest;             	//destination file iterator

        //Open file
        if(!a && !t){
                fd_source = open(source.c_str(), O_RDONLY, S_IRUSR | S_IWUSR);
                fd_dest = open(dest.c_str(), O_CREAT | O_WRONLY, S_IRUSR | S_IWUSR);
        }
        else if(t){
                fd_source = open(source.c_str(), O_RDONLY, S_IRUSR | S_IWUSR);
                fd_dest = open(dest.c_str(), O_WRONLY | O_TRUNC, S_IRUSR | S_IWUSR);
        }
        else if(a){
                fd_source = open(source.c_str(), O_RDONLY, S_IRUSR | S_IWUSR);
                fd_dest = open(dest.c_str(), O_WRONLY | O_APPEND, S_IRUSR | S_IWUSR);
        }
        if(fd_source == -1 || fd_dest == -1){
                cout << "File Doesn't exist" << endl;
                return 3;
        }


        //Read from source file to destination file
        char *c_buffer[buffer_size];              //convert buffer to character string
        ssize_t read_count = 1;                 // Place holder for reader

        while(read_count != 0){
                read_count = read(fd_source, c_buffer, buffer_size);
                write(fd_dest, c_buffer, read_count);
        }

	// Close Files
        close(fd_source);
        close(fd_dest);

        return 0;
}
