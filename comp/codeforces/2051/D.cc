#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int T;
    cin >> T;

    for (int i = 0; i < T; i++) {
        ll N, X, Y;
        cin >> N >> X >> Y;

        vector<ll> Ns(N);
        ll sum = 0;
        for (int i = 0; i < N; i++) {
            cin >> Ns[i];
            sum += Ns[i];
        }

        sort(Ns.begin(), Ns.end());

        auto between = [&](ll lo, ll hi) -> int {
            if (hi < 0 || lo > Ns[N-1]) return 0;

            ll li = distance(Ns.begin(), lower_bound(Ns.begin(), Ns.end(), lo));
            ll ri = distance(Ns.begin(), upper_bound(Ns.begin(), Ns.end(), hi));

            return ri - li;
        };

        ll ans = 0;
        for (int i = 0; i < N; i++) {
            // ans += count of N where (lower <= N <= upper)
            ll partial_sum = sum - Ns[i];
            ll lower = partial_sum - Y;
            ll upper = partial_sum - X;

            ll x = between(lower, upper);
            if (x > 0 && Ns[i] >= lower && Ns[i] <= upper) {
                x--;
            }

            ans += x;
        }

        cout << ans/2 << "\n";
    }
}
