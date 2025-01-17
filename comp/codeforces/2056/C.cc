#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N;
    cin >> N;

    vector<int> NX(N);

    if (N % 2 == 1) {
        // odd
        int max_count = N / 2 + 1;

        for (int i = 0; i < max_count; i++) {
            NX[i] = i + 1;
        }
        for (int i = max_count; i < N; i++) {
            NX[i] = i - max_count + 1;
        }
    } else {
        // even
        int max_count = N / 2;
        NX[0] = 1;
        for (int i = 1; i <= max_count; i++) {
            NX[i] = i;
        }
        for (int i = max_count + 1; i < N; i++) {
            NX[i] = i - max_count;
        }
    }

    for (auto x : NX) cout << x << " ";
    cout << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
