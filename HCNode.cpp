#include "HCNode.hpp"
#include <iostream>


bool HCNode::operator<(const HCNode& other){
    if(this->count!=other.count) 
        return this->count > other.count;    
    return this->symbol > other.symbol;
}