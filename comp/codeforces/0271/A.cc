#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N;
    cin >> N;

    for (int i = N+1; i <= 10000; i++) {
        int digits[4] = {0};
        int div = 1;
        for (int j = 0; j < 4; j++) {
            digits[j] = (i / div) % 10;
            div *= 10;
        }

        for (int a = 0; a < 4; a++) {
            for (int b = 0; b < 4; b++) {
                if (a != b && digits[a] == digits[b]) {
                    goto bad;
                }
            }
        }

        cout << i << "\n";
        return 0;

bad: continue;
    }
}
