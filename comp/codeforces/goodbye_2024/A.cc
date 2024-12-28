#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int T;
    cin >> T;

    for (int i = 0; i < T; i++) {
        int N;
        cin >> N;

        vector<int> A(N);
        for (int j = 0; j < N; j++) {
            cin >> A[j];
        }

        vector<ll> DP(N, -1);

        auto is_valid = [&](int start, int end) {
            assert(end > start);

            int min = *min_element(A.begin() + start, A.begin() + end).base();
            int max = *max_element(A.begin() + start, A.begin() + end).base();

            return (min * 2 > max);
        };

        function<ll(int)> dfs = [&](int loc) -> ll {
            if (loc >= N-1) {
                return 1;
            } else if (DP[loc] >= 0) {
                return DP[loc];
            }

            auto sum = 0;

            for (int j = loc + 1; j <= N; j++) {
                if (is_valid(loc, j)) {
                    sum += dfs(j);
                }
                if (sum >= 2) {
                    break;
                }
            }

            return sum;
        };

        if (dfs(0) >= 2) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }
}
