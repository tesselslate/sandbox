#include <bits/stdc++.h>

using namespace std;

int main() {
    int A, B;
    cin >> A >> B;

    for (int i = 1; i < 1000; i++) {
        A *= 3;
        B *= 2;
        if (A > B) {
            cout << i << "\n";
            return 0;
        }
    }
}
