#include <bits/stdc++.h>

using namespace std;

int main() {
    int T;
    cin >> T;

    int sum = 0;
    for (int i = 0; i < T; i++) {
        int A, B, C;
        cin >> A >> B >> C;

        if (A + B + C >= 2) {
            sum += 1;
        }
    }

    cout << sum << "\n";
}
