#include "HCTree.hpp"
#include "BitInputStream.hpp"
#include "BitOutputStream.hpp"
#include <queue>


void HCTree::build(const vector<int>& freqs){
    std::priority_queue<HCNode*, std::vector<HCNode*>, HCNodePtrComp> pq;
    for(unsigned int i=0;i<256;i++){
        unsigned char sym=i;
        if(freqs[i]!=0){
           leaves[i]=new HCNode(freqs[i], sym, 0, 0, 0);
           pq.push(leaves[i]);
        }
    }
    ////////////////////build the tree
    while(!pq.empty()){
        //leaves[(pq.top())->symbol]=pq.top();
        ////////if the size is 1 that means we have reach the last node which is the root

        if(pq.size()==1){
            root = pq.top();
            pq.pop();
            break;
        }
        ///create the parent with the sum frequency from its childs, and the sum bytes of the symbol from its childs
        
        ///////take the first element (less value) out
        HCNode* first = pq.top();
        pq.pop();
 
        ///////take the second element(larger or equal value) out
        HCNode* second = pq.top();
        pq.pop();
        HCNode* parent = new HCNode(first->count+second->count,first->symbol, 0, 0 ,0);   
        parent->c0 = first;
        parent->c1 = second;
        first->p=parent;
        second->p=parent;
    
        ////push the new node into the priority queue
        pq.push(parent);
    }
    
}

/*Header File recover
 *First I deal with Root, and push it in queue. For every bit read,
 *if nextbit =  0 -> make it be the child of first element of queue. push it in queue.
 *if nextbit =  1 -> make it be the child of first element of queue. read next 8 bit and recover byte.
 *if first element of queue has two child, just pop it.
 *Repeat until queue is empty
 */
void HCTree::rebuild(BitInputStream& in){
    int bit = in.readbit();
    unsigned char ascii;
    int temp;
    queue<HCNode*> queue;
    
    //initial root
    if (bit == 1) {
        //only one char
        ascii=0;
    
        for (int i =0;i<8;i++) {
            temp = in.readbit();
            ascii = ascii | (temp<<i);
        }
        root = new HCNode(1,ascii,0,0,0);
        return ;
    }else if(bit == -1){
        printf("empty file\n");
        root = NULL;
        return ;
    }else {
        //normal root
        root = new HCNode(0,0,0,0,0);
        queue.push(root);
    }
    
    //BFS
    while (!queue.empty()) {
        HCNode *top = queue.front();
        for(int j=0;j<2;j++){
            bit = in.readbit();
            if (bit == 1) {
                //leaf
                ascii=0;
                for (int i =0;i<8;i++) {
                    //get symbol
                    temp = in.readbit();
                    ascii = ascii | (temp<<i);
                }
                HCNode *leave = new HCNode(1,ascii,0,0);
                leave -> p = top;
                if(j==0){
                    top -> c0 = leave;
                }else{
                    top -> c1 = leave;
                }
            } else {
                //non-leaf
                HCNode * node = new HCNode(0,0,0,0,0);
                node -> p = top;
                if(j==0){
                    top -> c0 = node;
                }else{
                    top -> c1 = node;
                }
                queue.push(node);
            }
        }
        queue.pop();
    }
 
}

void HCTree::encode(byte symbol, BitOutputStream& out) const{
    unsigned int num = symbol;
    HCNode* curr;
    std::vector<int> code;
    curr = leaves[num];
    /*while(curr->p!=NULL){
        if(curr->p->c0 == curr)    ////node is at the left position( 0 position)of it's parent
            code.push_back(0);
        else                       ////node is at the right position( 1 position)of it's parent
            code.push_back(1);
        curr=curr->p;
    }
    //////////because the order we insert the number into the vector is actuallly the opposite order of the original code
    //////////we need to take it out in an opposite way
    for(int n=code.size()-1;n>=0;n--)
    {
        out.writeBit(code[n]);
    }
    //reach the end of the file
    //eof
    //out.writeEnd();*/
    rewrite(curr,out);

}

void rewrite(HCNode* curr,  BitOutputStream& out){
    if(!curr->p)
        return;
    rewrite(curr->p,out);
    if(curr->p->c0==curr)
        out.writeBit(0);
    if(curr->p->c1==curr)
        out.writeBit(1);
}

/* Header file
 Use 1 to denote leaf and 0 to denote internal node
 */
void HCTree::recordTree(HCNode *curr, int depth, BitOutputStream& out) const{
    int temp;
    unsigned char ascii;
    
    // record root
    if(depth == 0){
        curr = root;
        if(curr->c0 == 0 && curr->c1 == 0){
            out.writeBit(1);
            ascii = curr->symbol;
            for(int i=0;i<8;i++){
                temp = ascii | 1;
                out.writeBit(temp);
                ascii = ascii >> 1;
            }
            return;
        }else{
            out.writeBit(0);
        }
    }
    
    //BFS
    queue<HCNode*> queue;
    queue.push(curr);
    while(!queue.empty()){
        curr = queue.front();
        queue.pop();
        
        //left
        if(curr->c0->c0==0){
            //leaf
            out.writeBit(1);
            ascii = curr->c0->symbol;
            for(int i=0; i<8; i++){
                temp = ascii & 1;
                out.writeBit(temp);
                ascii = ascii >> 1;
            }
        }else{//nonleaf
            out.writeBit(0);
            queue.push(curr->c0);
        }
        
        //right
        if(curr->c1->c1==0){
            //leaf
            out.writeBit(1);
            ascii = curr->c1->symbol;
            for(int i=0; i<8; i++){
                temp = ascii & 1;
                out.writeBit(temp);
                ascii = ascii >> 1;
            }
        }else{//nonleaf
            out.writeBit(0);
            queue.push(curr->c1);
        }
        

        
    }
    
    
    
    
    
    
}


/*
void HCTree::encode(byte symbol, ofstream& out) const{
    unsigned int num;
    HCNode* curr;
    num = symbol;
    std::vector<int> code;
    curr = leaves[num];
    while(curr->p!=NULL){
        if(curr->p->c0 == curr)    ////node is at the left position( 0 position)of it's parent
            code.push_back(0);
        else                       ////node is at the right position( 1 position)of it's parent
            code.push_back(1);
        curr=curr->p;
    }
    //////////because the order we inser the number into the vector is actuallly the opposite order of the original code
    //////////we need to take it out in an opposite way
    for(int n=code.size()-1;n>=0;n--)
    {
        out<< code[n]; 
    }
    //out<<endl;
    
}
*/

int HCTree::decode(BitInputStream& in) const{
    HCNode* curr;
    curr=root;
    int nextint;
    
    //////////////read to the part that we need to decode from, not the header       
    while(curr->c0 && curr->c1)   //check whether it reach the end of the tree
    {
        nextint=(int)in.readbit();
        if(nextint==-1)
            return -1;
        if(nextint==1)
            curr=curr->c1;
        else
            curr=curr->c0;
    }
    
    return curr->symbol;
}

/*
int HCTree::decode(ifstream& in) const{
    
    ////////decoding
    HCNode* curr;
    curr=root;
    unsigned int nextint;
    
    //////////////read to the part that we need to decode from, not the header       
    while(curr->c0 && curr->c1)   //check whether it reach the end of the tree
    {
        nextint=in.get();
        if(in.eof())
            return -1;
        cout<<nextint<<endl;
        if(nextint=='1')
            curr=curr->c1;
        else
            curr=curr->c0;
    }
    
    return curr->symbol;
    
}
*/

void HCTree::deleteAll(HCNode* node){
    if(!node)
        return;
    deleteAll(node->c0);
    deleteAll(node->c1);
    delete node;
}

HCTree::~HCTree(){
   
        deleteAll(root);
      
}

