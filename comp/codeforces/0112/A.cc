#include <bits/stdc++.h>

using namespace std;

int main() {
    string a, b;
    cin >> a >> b;

    for (int i = 0; i < a.size(); i++)
        if (a[i] < 'a')
            a[i] += 'a' - 'A';
    for (int i = 0; i < b.size(); i++)
        if (b[i] < 'a')
            b[i] += 'a' - 'A';

    for (int i = 0; i < a.size(); i++) {
        if (a[i] < b[i]) {
            cout << "-1\n";
            return 0;
        } else if (a[i] > b[i]) {
            cout << "1\n";
            return 0;
        }
    }

    cout << "0\n";
}
