#include <bits/stdc++.h>

using namespace std;

int main() {
    int X;
    cin >> X;

    int p = 0, steps = 0;
    for (int i = 5; i >= 1; i--) {
        int n = (X-p)/i;
        steps += n;
        p += n*i;
    }
    cout << steps << "\n";
}
