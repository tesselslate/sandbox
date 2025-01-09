#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    string S;
    cin >> S;

    map<char, ll> freq;
    for (auto c : S) {
        freq[c]++;
    }

    ll sum = 0;
    for (auto p : freq) {
        sum += p.second * p.second;
    }

    cout << sum << "\n";
}
