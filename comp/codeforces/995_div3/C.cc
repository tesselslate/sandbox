#include <bits/stdc++.h>

using namespace std;

int main() {
    int T;
    cin >> T;

    for (int i = 0; i < T; i++) {
        int N, M, K;
        cin >> N >> M >> K;

        vector<int> Ms(M), Ks(N);
        for (int i = 0; i < M; i++) {
            cin >> Ms[i];
            Ms[i]--;
        }

        for (int i = 0; i < K; i++) {
            int x;
            cin >> x;
            x--;
            Ks[x] = true;
        }

        for (int i = 0; i < M; i++) {
            if (K == N) {
                cout << "1";
            } else if (K == N-1) {
                cout << (!Ks[Ms[i]] ? "1" : "0");
            } else {
                cout << "0";
            }
        }

        cout << "\n";
    }
}
