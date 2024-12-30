#include <bits/stdc++.h>

using namespace std;

int main() {
    string s;
    cin >> s;

    int N[3] = {0};
    for (int i = 0; i < s.size(); i += 2) {
        N[s[i] - '1'] += 1;
    }

    vector<int> nums;
    for (int i = 0; i < N[0]; i++)
        nums.push_back(1);
    for (int i = 0; i < N[1]; i++)
        nums.push_back(2);
    for (int i = 0; i < N[2]; i++)
        nums.push_back(3);

    for (int i = 0; i < nums.size(); i++) {
        cout << nums[i];
        if (i + 1 != nums.size()) {
            cout << "+";
        }
    }
    cout << "\n";
}
