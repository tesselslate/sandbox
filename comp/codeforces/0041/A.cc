#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    string A, B;
    cin >> A >> B;

    if (A.size() != B.size()) {
        cout << "NO\n";
        return 0;
    }

    for (int i = 0; i < A.size(); i++) {
        if (A[i] != B[A.size() - i - 1]) {
            cout << "NO\n";
            return 0;
        }
    }
    cout << "YES\n";
}
