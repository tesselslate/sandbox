#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N;
    string S;
    cin >> N >> S;

    int a = 0;
    for (auto c : S)
        if (c == 'A') a++;

    int d = N-a;
    if (a > d) cout << "Anton\n";
    else if (d > a) cout << "Danik\n";
    else cout << "Friendship\n";
}
