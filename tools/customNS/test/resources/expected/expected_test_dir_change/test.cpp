#include <string>
#include <iostream>
namespace mw_cppms {
    int a = 1;
    int b = 2;
    namespace foo {
        std::string k = "something";
    }
    
}

std::string func(const std::string& str) {return "hi" + str;}

int main() {
    int one = mw_cppms::a;
    int two = mw_cppms
        ::b;
    std::cout << mw_cppms::a << func(mw_cppms::foo::k + "mw_cppms::a") << '\n';
}

