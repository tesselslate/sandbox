#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    const vector<ll> LUT = {
        0,
        10,
        100,
        1000,
        10000,
        100000,
        1000000,
        10000000,
        100000000,
        1000000000,
        10000000000,
        100000000000,
        1000000000000,
    };

    ll N;
    cin >> N;

    int maxdigits = distance(LUT.begin(), upper_bound(LUT.begin(), LUT.end(), N));

    vector<ll> super_lucky;
    for (int digits = maxdigits - 1; digits <= maxdigits + 2; digits++) {
        if (digits % 2 == 1) continue;

        int range = (1 << digits) - 1;
        for (int i = 0; i < range; i++) {
            if (__builtin_popcount(i) != digits / 2) continue;

            ll acc = 0;
            ll mult = 1;

            for (int j = 0; j < digits; j++) {
                if (i & (1 << j)) {
                    acc += 4 * mult;
                } else {
                    acc += 7 * mult;
                }
                mult *= 10;
            }

            super_lucky.push_back(acc);
        }
    }
    sort(super_lucky.begin(), super_lucky.end());

    cout << *lower_bound(super_lucky.begin(), super_lucky.end(), N) << "\n";
}
