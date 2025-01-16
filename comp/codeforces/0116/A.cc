#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N;
    cin >> N;

    vector<int> A(N), B(N);
    for (int i = 0; i < N; i++) {
        cin >> A[i] >> B[i];
    }

    int M = 0, P = 0;
    for (int i = 0; i < N; i++) {
        P -= A[i];
        P += B[i];
        M = max(M, P);
    }
    cout << M << "\n";
}
