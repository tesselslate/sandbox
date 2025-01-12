#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    ll N;
    cin >> N;

    vector<ll> A(N), B(N);
    for (auto &x : A) cin >> x;
    for (auto &x : B) cin >> x;

    ll min_excess = LONG_LONG_MAX;
    ll diff = 0;
    for (int i = 0; i < N; i++) {
        if (A[i] >= B[i]) {
            min_excess = min(min_excess, A[i] - B[i]);
        }
        if (B[i] > A[i]) {
            if (diff != 0) {
                cout << "NO\n";
                return;
            }
            diff = B[i] - A[i];
        }
    }

    cout << (min_excess >= diff ? "YES\n" : "NO\n");
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
