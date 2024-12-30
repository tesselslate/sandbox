#include <bits/stdc++.h>

using namespace std;

int main() {
    int T;
    cin >> T;

    for (int i = 0; i < T; i++) {
        int N;
        cin >> N;

        vector<int> A(N), B(N);
        for (int i = 0; i < N; i++) {
            cin >> A[i];
        }
        for (int i = 0; i < N; i++) {
            cin >> B[i];
        }

        int diff = A[N-1];
        for (int i = 0; i < N-1; i++) {
            if (A[i] > B[i+1]) {
                diff += (A[i]-B[i+1]);
            }
        }

        cout << diff << "\n";
    }
}
