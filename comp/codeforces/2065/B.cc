#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    string S;
    cin >> S;

    while (true) {
        bool op = false;

        for (int i = S.length() - 1; i >= 0; i--) {
            if (S[i] != S[i+1]) {
                continue;
            }

            if (i > 0) {
                S[i] = S[i-1];
                S.erase(i+1, 1);
            } else {
                if (i < S.length() - 2) {
                    S[i] = S[i+2];
                }
                S.erase(i+1,1);
            }
            op = true;
        }

        if (!op) break;
    }

    cout << S.length() << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
