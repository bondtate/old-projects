/*****************************************************************************
Name: Tate Bond
Computer Project 4
*****************************************************************************/
#include <iostream>
#include <fstream>
#include <sstream>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <limits.h>
#include <sys/stat.h>

using namespace std;

struct data{
    		unsigned long int  st_dev;      /* ID of device containing file */
    		unsigned long int  st_ino;      /* inode number */
    		unsigned long int  st_nlink;    /* number of hard links */
    		unsigned      int  st_mode;     /* file type and mode */
    		unsigned      int  st_uid;      /* user ID of owner */
    		unsigned      int  st_gid;      /* group ID of owner */
                	      int  __pad0;
    		unsigned long int  st_rdev;     /* device ID (if special file) */
             	long int  st_size;     /* total size, in bytes */
             	long int  st_blksize;  /* blocksize for filesystem I/O */
             	long int  st_blocks;   /* number of 512B blocks allocated */
    		struct timespec    st_atim;     /* time of last access */
    		struct timespec    st_mtim;     /* time of last modification */
    		struct timespec    st_ctim;     /* time of last status change */
             	long int  __glibc_reserved[3];
 	};
int output(string filename, bool command){



	const char *path = filename.c_str();

	struct data *buffer = (struct data*)malloc(sizeof(struct data));

	int tri = stat("/user/bondtate", stat buffer);

	if(command == false){

	}

	else{

	}
	return 1;
}

int main(int argc, char* argv[]){

        bool is_s = true;         	// S option selected
	string paths;			// A string of all paths

        //Loop through the arguments and set variables based on input
        int count = 1;                  //count for iterating loop
        while(count < argc){
                string input = string( argv[count] );   //convert arg to string

                if(input[0] == '-'){
                        if(input == "-L"){
                                is_s = false;
                        }
                        else if(input == "-S"){
                                is_s = true;
                        }
                        else{
                                cout << "Error: Incorrect input" << endl;
                                return 0;
                        }
                }
		else if(input[0] == '/'){
			
		}
		else{
			char *env = getenv("DIRLIST");
			if (*env == NULL){
                                cout << "Error: Environment variable not set" << endl;
                                return 1;
			}

			string paths(env);
			string path;

			// Loop over the list of directories
			while(paths.length() > 0){

				size_t index = paths.find(':');
				if(index != string::npos){

					path = paths.substr(0, index);
					paths = paths.substr(index + 1);

				}
				else{
					path = paths;
					paths = "";
				}

				string path_check = path;
				path_check += '/';
				path_check += input;
				const char *path_c = path_check.c_str();

				char buffer[PATH_MAX];
				char *res = realpath(path_c, buffer);
				if(res){
					cout << buffer << endl;
					int one = output(buffer, is_s);
				}
				else{
					cout << "Error: File not found from given paths"
<< endl;
				}
			}
		}
		
		count += 1;
	}
}
