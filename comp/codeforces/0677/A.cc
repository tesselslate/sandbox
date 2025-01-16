#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N, H;
    cin >> N >> H;

    int sum = 0;
    for (int i = 0; i < N; i++) {
        int h;
        cin >> h;
        sum++;
        if (h > H) sum++;
    }
    cout << sum << "\n";
}
