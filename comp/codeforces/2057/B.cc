#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N, K;
    cin >> N >> K;

    vector<int> xs(N);
    for (auto &x : xs) cin >> x;

    map<int, int> present;
    for (auto x : xs) present[x]++;

    multimap<int, int> fpresent;
    for (auto p : present) fpresent.insert(pair(p.second, p.first));

    int min = *min_element(xs.begin(), xs.end());

    int ops = present.size();
    for (auto p : fpresent) {
        if (p.first <= K) {
            K -= p.first;
            ops -= 1;
        } else {
            break;
        }
    }

    cout << max(ops, 1) << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
