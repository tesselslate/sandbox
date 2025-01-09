#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    ll K, N, W;
    cin >> K >> N >> W;

    ll cost = 0;
    for (ll i = 1; i <= W; i++) {
        cost += i * K;
    }

    if (cost <= N) {
        cout << "0\n";
    } else {
        cout << cost-N << "\n";
    }
}
