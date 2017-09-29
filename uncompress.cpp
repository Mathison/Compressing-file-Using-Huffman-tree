//uncompress
#include "HCNode.hpp"
#include "HCTree.hpp"
#include <string>
#include <sstream>
using namespace std;

int main(int argc, char** argv)
{   
    //unsigned string in_file = atoi(argv[1]);
    //unsigned string out_file = atoi(argv[2]);
    ///////read the charaters from the ifile
    ifstream in;               ////the infile here is the outfile in compress.cpp
    in.open (argv[1],ios::binary);
    BitInputStream infile(in);
    //int nextint;
    unsigned int total_word;
    unsigned int num_word=0;
    /*
    vector<int> freqs(256, 0);
    ///read the characters from the infile
    
    while(num<256){
        //if(infile.get()=='/n')
            //continue;
        in>>nextint;

        //istringstream(infile.get())>>nextint;
        if(nextint!=0)
           freqs[num]=nextint;        /////add the frequency to the vector
        num++;
        total_word+=nextint;
     
    }
    infile.readNewline();
     */
    
    // Rebuild tree
    int temp;
    for (int i =0;i<32;i++) {
        temp = infile.readbit();
        total_word = total_word | (temp<<i);
    }
    
    HCTree* Htree=new HCTree();
    Htree->rebuild(infile);
    
    /////began to write the character into the outfile
    ofstream outfile;
    outfile.open (argv[2],ios::binary);
    unsigned int i;
    
    while(num_word<total_word){
        
        unsigned char character=Htree->decode(infile);
        outfile<<character;
        num_word++;
    }
    
    in.close();
    outfile.close();
    delete Htree;
    return 0;
}
