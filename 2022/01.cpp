#include "util.h"
#include <algorithm>
#include <cstdint>
#include <string>

std::vector<uint32_t> get_calories();

int main() {
    auto elves = get_calories();

    // part 1
    auto max = *std::max_element(elves.begin(), elves.end());
    std::cout << "part 1: " << max << std::endl;

    // part 2
    std::sort(elves.begin(), elves.end());
    auto sum = 0;
    for (int i = 0; i < 3; i++) {
        sum += elves.back();
        elves.pop_back();
    }
    std::cout << "part 2: " << sum << std::endl;
}

std::vector<uint32_t> get_calories() {
    std::vector<uint32_t> out;
    uint32_t sum = 0;
    for (std::string line : advent::get_input()) {
        if (line.empty()) {
            out.push_back(sum);
            sum = 0;
            continue;
        }
        sum += std::stoi(line);
    }
    return out;
}
