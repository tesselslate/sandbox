#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    ll N, R, AVG;
    cin >> N >> R >> AVG;

    multimap<ll, ll> data;
    for (int i = 0; i < N; i++) {
        ll a, b;
        cin >> a >> b;

        data.insert(pair(b, a));
    }

    ll req = AVG*N;
    for (auto pair : data) req -= pair.second;

    ll essays = 0;
    if (req > 0) {
        for (auto pair : data) {
            if (req == 0) break;

            ll inc = R-pair.second;
            inc = min(inc, req);

            req -= inc;
            essays += inc*pair.first;
        }
    }

    cout << essays << "\n";
}
