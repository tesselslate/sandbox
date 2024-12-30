#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int T;
    cin >> T;

    for (int i = 0; i < T; i++) {
        int N;
        cin >> N;

        vector<int> A(N);
        for (int j = 0; j < N; j++) {
            cin >> A[j];
        }

        bool ok = false;
        for (int i = 0; i < N-1; i++) {
            auto min = std::min(A[i], A[i+1]);
            auto max = std::max(A[i], A[i+1]);

            if (min * 2 > max) {
                ok = true;
                break;
            }
        }

        if (ok) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }
}
