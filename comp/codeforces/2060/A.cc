#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int a[5] = {0};
    cin >> a[0] >> a[1] >> a[3] >> a[4];

    int best = 0;
    for (int i = -200; i <= 200; i++) {
        a[2] = i;

        int n = 0;
        for (int j = 0; j < 3; j++) {
            if (a[j] + a[j+1] == a[j+2]) n++;
        }

        best = max(best, n);
    }
    cout << best << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
