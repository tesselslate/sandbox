#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    string S;
    cin >> S;

    int a = 0, b = 0;
    for (auto c : S) {
        if (c == '1') {
            a++;
            b = 0;
            if (a == 7) {
                cout << "YES\n";
                return 0;
            }
        } else {
            b++;
            a = 0;
            if (b == 7) {
                cout << "YES\n";
                return 0;
            }
        }
    }

    cout << "NO\n";
}
