#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N, L;
    cin >> N >> L;

    vector<int> NX(N);
    for (auto &x : NX) cin >> x;

    sort(NX.begin(), NX.end());
    int prev = -NX[0];
    int max_dist = 0;

    for (int i = 0; i < N; i++) {
        max_dist = max(max_dist, NX[i] - prev);
        prev = NX[i];
    }
    max_dist = max(max_dist, (L - NX.back()) * 2);

    printf("%lf\n", (double)max_dist / 2.0);
}
