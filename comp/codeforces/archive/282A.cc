#include <bits/stdc++.h>

using namespace std;

int main() {
    int N;
    cin >> N;

    int X = 0;
    for (int i = 0; i < N; i++) {
        string op;
        cin >> op;

        if (op[0] == '-' || op[2] == '-') {
            X--;
        } else {
            X++;
        }
    }

    cout << X << "\n";
}
