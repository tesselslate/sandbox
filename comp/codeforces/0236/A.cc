#include <bits/stdc++.h>

using namespace std;

int main() {
    string s;
    cin >> s;

    set<char> chars;
    for (auto c : s) {
        chars.insert(c);
    }

    cout << ((chars.size() % 2 == 0) ? "CHAT WITH HER!" : "IGNORE HIM!") << "\n";
}
