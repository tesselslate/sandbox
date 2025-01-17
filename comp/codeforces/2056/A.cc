#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N, M;
    cin >> N >> M;

    vector<int> X(N), Y(N);
    for (int i = 0; i < N; i++) {
        cin >> X[i] >> Y[i];
    }

    ll perimeter = 4 * M * N;
    ll overlap = 0;
    int x = 0, y = 0;
    for (int i = 0; i < N; i++) {
        int nx = X[i], ny = Y[i];
        if (i >= 1) {
            if (M > nx) {
                overlap += M - nx;
            }
            if (M > ny) {
                overlap += M - ny;
            }
        }

        x += nx;
        y += ny;
    }

    perimeter -= overlap * 2;
    cout << perimeter << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
