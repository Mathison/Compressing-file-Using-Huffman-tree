#ifndef BITOUTPUTSTREAM_HPP
#define BITOUTPUTSTREAM_HPP

#include <iostream>
#include <fstream>
#include <vector>

class BitOutputStream{
private:
   unsigned char buf;
   int nbits;
    int times;
   std::ostream & out;

public:

   BitOutputStream(std::ostream & os) : out(os), buf(0), nbits(0),times(0){
         //out.open(os);
   }

   void flush();
   
   void writeBit(int i);

   void write_freq(std::vector<int> freq);

   void writeEnd();
   //void op(const char* filename);

   //void cl();

};

#endif
