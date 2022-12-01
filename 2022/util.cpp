#include "util.h"
#include <iostream>
#include <string>
#include <vector>

namespace advent {
    std::vector<std::string> get_input() {
        std::vector<std::string> vec;
        std::string line;
        while (std::cin) {
            std::getline(std::cin, line);
            vec.push_back(line);
        }
        return vec;
    }
} // namespace advent
