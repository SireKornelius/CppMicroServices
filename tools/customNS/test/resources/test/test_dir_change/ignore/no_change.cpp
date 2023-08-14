#include <string>
#include <iostream>
namespace cppmicroservices {
    int a = 1;
    int b = 2;
    namespace foo {
        std::string k = "something";
    }
    
}

std::string func(const std::string& str) {return "hi" + str;}

int main() {
    int one = cppmicroservices::a;
    int two = cppmicroservices
        ::b;
    std::cout << cppmicroservices::a << func(cppmicroservices::foo::k + "cppmicroservices::a") << '\n';
}
