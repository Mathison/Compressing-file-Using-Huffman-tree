#include "BitOutputStream.hpp"
using namespace std;

//////////////////used to write huffman code to the file
void BitOutputStream::writeBit(int i){
    
    if(nbits==8){
        flush();
        times++;
        if(times == 3999){
            out.flush();
            times = 0;
        }
    }
    buf=(buf<<1)|i;
    
    nbits++;
    
}

void BitOutputStream::writeEnd(){
  if(nbits!=0){
      buf=buf<<(8-nbits);
      flush();
  }

}

void BitOutputStream::flush(){
        out.put(buf);
        //out.flush();
        buf=nbits=0;
}

void BitOutputStream::write_freq(std::vector<int> freq){
    for(vector<int>::iterator it = freq.begin(); it != freq.end(); ++it)
        out<<*it<<endl;
}
