#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    string S;
    cin >> S;

    string NS;
    for (int i = 0; i < S.length() - 2; i++) {
        NS.push_back(S[i]);
    }
    NS.push_back('i');

    cout << NS << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
