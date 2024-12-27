#include <bits/stdc++.h>

using namespace std;

int main() {
    int N;
    cin >> N;

    string S;
    cin >> S;

    int c = 0;
    for (int i = S.size() - 1; i >= 0; i--) {
        if (S[i+1] == S[i]) {
            c++;
        }
    }

    cout << c << "\n";
}
