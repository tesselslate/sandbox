#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N, K, T;
    cin >> N >> K >> T;

    int total = N*K;
    int progress = (total * T) / 100;

    for (int i = 0; i < N; i++) {
        if (progress >= K) {
            cout << K << " ";
            progress -= K;
        } else if (progress > 0) {
            cout << progress << " ";
            progress = 0;
        } else {
            cout << "0 ";
        }
    }
    cout << "\n";
}
