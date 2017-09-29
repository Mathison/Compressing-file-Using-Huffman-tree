#include "BitInputStream.hpp"
using namespace std;
void BitInputStream::fill(){
          buf = in.get();
          nbits = 0;
      }

int BitInputStream::readbit(){
    if(nbits==8){     
        fill();  
       
        if(in.eof())
          return -1;   
    }
    if(buf>>7 == 0){
      nbits++;
      buf = buf<<1;
      return 0;}
    else{
      nbits++;
      buf = buf<<1;
      return 1;}
    /*
    unsigned char test=buf<<nbits;
    int test=test>>7;
    nbits++;
    return test;
    */
}
 
 void BitInputStream::readNewline(){
      fill();
      nbits = 8;
    }
          



