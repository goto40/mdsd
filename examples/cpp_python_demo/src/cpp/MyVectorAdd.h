#ifndef __MyVectorAdd_H
#define __MyVectorAdd_H

#include "algos/example.h"
#include <iostream>

// AxxxCTIVATE FOR SWIG
// if visible for SWIG, we need:
//#ifdef SWIG
//%shared_ptr(MyVectorAdd)
//#endif

class MyVectorAdd : public algos::VectorAdd {
    inline static struct __Init {
        __Init() { algos::VectorAdd::set_factory([]() { return std::make_shared<MyVectorAdd>(); } ); }
    } __init;
public:

    ~MyVectorAdd() { std::cout << "~MyVectorAdd\n"; }

    void compute(
        const items::Point& p1, 
        const items::Point& p2, 
        items::Point& p
    ) override {
        std::cout << "myVectorAdd::compute called\n";
        p.x = p1.x+p2.x;
        p.y = p1.y+p2.y;
    }

};

#endif
