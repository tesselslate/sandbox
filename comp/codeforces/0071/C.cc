#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N;
    cin >> N;

    vector<int> moods(N);
    for (auto &x : moods) cin >> x;

    int half = N/2 + (N%2==1);
    for (int d = 1; d < half; d++) {
        if (N%d != 0) continue;

        for (int s = 0; s < d; s++) {
            bool ok = true;
            for (int i = s; i < N; i += d) {
                if (!moods[i]) {
                    ok = false;
                    break;
                }
            }
            if (ok) {
                cout << "YES\n";
                return 0;
            }
        }
    }
    cout << "NO\n";
}
