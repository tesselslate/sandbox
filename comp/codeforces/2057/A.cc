#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    ll N, M;
    cin >> N >> M;

    cout << max(M, N) + 1 << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
