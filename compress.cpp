//compress
#include "HCNode.hpp"
#include "HCTree.hpp"
using namespace std;


int main(int argc, char** argv)
{
    ///////read the charaters from the ifile
    ifstream infile;
    infile.open (argv[1],ios::binary);

    byte nextchar;
    unsigned int num;
    unsigned int sum=0;
    vector<int> freqs(256, 0);
    
    ///read the characters from the infile
    while(1){
        nextchar = infile.get();
        if(infile.eof()){
            break;
        }
        num = nextchar;
        freqs[num]++;        /////add the frequency when find the character
        sum++;
    }
    infile.close();
    HCTree* Htree=new HCTree();
    Htree->build(freqs);
    
    //////back to the beginning of the file to get the character again
    ifstream inside_file;
    inside_file.open (argv[1],ios::binary);
    
    /////began to write the header into the outfile
    ofstream out;
    out.open(argv[2], ios::binary);
    BitOutputStream outfile(out);
    //write the sum
    if(sum!=0){
        for (int i=0;i<32;i++) {
            outfile.writeBit(sum%2);
            sum = sum >> 1;
        }
    }
    
    //record the tree
    Htree->recordTree(NULL,0,outfile);
    //outfile.writeEnd();
 
    ///began to write code into the outfile
    unsigned char c;
    while(1){
        c=inside_file.get();
        if(inside_file.eof())
            break;
        Htree->encode(c, outfile);
    }
    
    outfile.writeEnd();
    
    inside_file.close();
    out.close();
    delete Htree;
    return 0;
}
