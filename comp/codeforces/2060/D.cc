#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N;
    cin >> N;

    vector<int> A(N);
    for (auto &x : A) cin >> x;

    for (int i = 0; i < N-1; i++) {
        int m = min(A[i], A[i+1]);
        A[i] -= m;
        A[i+1] -= m;
    }

    for (int i = 0; i < N-1; i++) {
        if (A[i+1] < A[i]) {
            cout << "NO\n";
            return;
        }
    }

    cout << "YES\n";
    return;
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
