#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int D, sumTime;
    cin >> D >> sumTime;

    vector<int> MIN(D), MAX(D);
    for (int i = 0; i < D; i++) {
        cin >> MIN[i] >> MAX[i];
    }

    int sum = 0;
    for (auto x : MIN) sum += x;
    vector<int> days = MIN;
    while (sum < sumTime) {
        bool added = false;

        for (int i = 0; i < D; i++) {
            if (sum >= sumTime) {
                break;
            }

            if (MAX[i] > days[i]) {
                days[i]++;
                sum++;

                added = true;
            }
        }

        if (!added) {
            break;
        }
    }

    if (sum == sumTime) {
        cout << "YES\n";
        for (auto x : days) cout << x << " ";
        cout << "\n";
    } else {
        cout << "NO\n";
    }
}
