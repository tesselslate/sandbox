#include <bits/stdc++.h>

using namespace std;

int main() {
    int T;
    cin >> T;

    for (int i = 0; i < T; i++) {
        uint64_t N;
        cin >> N;

        uint64_t count = 1;
        while (N > 3) {
            N /= 4;
            count *= 2;
        }

        cout << count << "\n";
    }
}
