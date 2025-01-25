#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N, L, R;
    cin >> N >> L >> R;

    vector<int> left, mid, right;
    for (int i = 1; i <= N; i++) {
        int x;
        cin >> x;

        if (i < L) {
            left.push_back(x);
        } else if (i <= R) {
            mid.push_back(x);
        } else {
            right.push_back(x);
        }
    }

    sort(left.rbegin(), left.rend());
    sort(mid.begin(), mid.end());
    sort(right.rbegin(), right.rend());

    ll mid_sum = 0;
    for (auto x : mid) mid_sum += (ll)x;

    ll left_sub = 0, right_sub = 0;
    for (auto it = mid.rbegin(); it != mid.rend(); advance(it, 1)) {
        if (left.size() > 0) {
            left_sub += max(0, *it - left.back());
            left.pop_back();
        }
        if (right.size() > 0) {
            right_sub += max(0, *it - right.back());
            right.pop_back();
        }
    }

    cout << (mid_sum - max(left_sub, right_sub)) << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
