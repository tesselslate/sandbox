#include <bits/stdc++.h>

using namespace std;

#define ll long long

struct entry {
    vector<ll> A;
    ll sum;
};

void test_case() {
    int N, M;
    cin >> N >> M;

    vector<struct entry> A;
    for (int i = 0; i < N; i++) {
        vector<ll> a(M);
        for (auto &x : a) cin >> x;

        ll sum = 0;
        for (auto x : a) sum += x;
        A.push_back((struct entry){.A = a, .sum = sum});
    }

    auto sortfunc = [&](const struct entry& a, const struct entry& b) -> bool {
        return a.sum < b.sum;
    };

    sort(A.rbegin(), A.rend(), sortfunc);

    ll sum = 0;
    ll count = N*M;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            sum += count * A[i].A[j];
            count--;
        }
    }

    cout << sum << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
