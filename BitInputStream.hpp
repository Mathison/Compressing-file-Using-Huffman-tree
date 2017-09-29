#ifndef BITINPUTSTREAM_HPP
#define BITINPUTSTREAM_HPP
#include <iostream>

class BitInputStream {
private :
      char buf;
      int nbits;
      std::istream & in;
public :
      
      BitInputStream(std::istream & is):in(is){
          buf = 0;
          nbits = 8;
      }

      void fill();

      int readbit();
  void readNewline();
    };

#endif
