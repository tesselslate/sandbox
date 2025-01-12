#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N, A, B;
    cin >> N >> A >> B;

    int diff = abs(A-B);
    if (diff % 2 == 0) {
        cout << "YES\n";
    } else {
        cout << "NO\n";
    }
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
