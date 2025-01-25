#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int L, R;
    cin >> L >> R;

    if (L == R && L == 1) {
        cout << "1\n";
    } else {
        cout << (R - L) << "\n";
    }
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
