#include <bits/stdc++.h>

using namespace std;

int main() {
    int W;
    cin >> W;

    for (int i = 2; i < W; i += 2) {
        if ((W - i) % 2 == 0) {
            cout << "YES" << "\n";
            return 0;
        }
    }
    cout << "NO" << "\n";
}
