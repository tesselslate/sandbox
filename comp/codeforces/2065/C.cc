#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N, M;
    cin >> N >> M;

    vector<ll> A(N), B(M);
    for (auto &x : A) cin >> x;
    for (auto &x : B) cin >> x;

    sort(B.begin(), B.end());

    for (int i = 0; i < A.size(); i++) {
        if (i == 0) {
            int alt = B[0] - A[i];
            if (alt < A[i]) {
                A[i] = alt;
            }
            continue;
        }

        ll target = A[i] + A[i-1];
        auto it = lower_bound(B.begin(), B.end(), target);
        if (it == B.end()) continue;

        ll alt = *it - A[i];
        if (alt < A[i] || A[i] < A[i-1]) {
            A[i] = alt;
        }
    }

    for (int i = 0; i < A.size() - 1; i++) {
        if (A[i] > A[i+1]) {
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
