#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    ll N;
    cin >> N;

    ll lucky = 0;
    while (N > 0) {
        ll digit = N % 10;
        if (digit == 4 || digit == 7) lucky++;
        N /= 10;
    }

    cout << ((lucky == 4 || lucky == 7) ? "YES" : "NO") << "\n";
}
