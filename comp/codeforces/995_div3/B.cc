#include <bits/stdc++.h>

using namespace std;

int main() {
    int T;
    cin >> T;

    for (int i = 0; i < T; i++) {
        int N, A, B, C;
        cin >> N >> A >> B >> C;

        int sum = A + B + C;
        int loops = N/sum;
        N -= sum*loops;

        int days = loops * 3;
        if (N > 0) { N -= A; days += 1; }
        if (N > 0) { N -= B; days += 1; }
        if (N > 0) { N -= C; days += 1; }

        cout << days << "\n";
    }
}
