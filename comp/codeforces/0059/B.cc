#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N;
    cin >> N;

    vector<int> petals(N);
    for (auto &x : petals) cin >> x;

    int sum = 0;
    vector<int> odd;
    for (auto x : petals) {
        if (x % 2 == 0) {
            sum += x;
        } else {
            odd.push_back(x);
        }
    }

    if (odd.size() == 0) {
        cout << "0\n";
        return 0;
    }
    sort(odd.begin(), odd.end());

    if (odd.size() % 2 == 1) {
        for (auto x : odd) sum += x;
    } else {
        for (int i = 1; i < odd.size(); i++) {
            sum += odd[i];
        }
    }

    cout << sum << "\n";
}
