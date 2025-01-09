#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    string S;
    cin >> S;

    int upper = 0;
    for (auto c : S) {
        if (c >= 'A' && c <= 'Z') {
            upper++;
        }
    }

    if (upper > S.size() / 2) {
        for (auto &c : S) {
            if (!(c >= 'A' && c <= 'Z')) {
                c = (c - 'a') + 'A';
            }
        }
    } else {
        for (auto &c : S) {
            if (!(c >= 'a' && c <= 'z')) {
                c = (c - 'A') + 'a';
            }
        }
    }

    cout << S << "\n";
}
