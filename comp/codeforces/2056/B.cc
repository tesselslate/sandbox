#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N;
    cin >> N;

    vector<vector<bool>> adj(N, vector<bool>(N));
    for (int i = 0; i < N; i++) {
        string S;
        cin >> S;

        for (int j = 0; j < N; j++) {
            if (S[j] == '1') {
                adj[i][j] = true;
                adj[j][i] = true;
            }
        }
    }

    vector<int> seq;
    vector<bool> visited(N);

    for (int i = N - 1; i >= 0; i--) {
        if (visited[i]) continue;

        function<void(int)> dfs = [&](int node) -> void {
            if (visited[node]) return;
            visited[node] = true;

            vector<int> children;
            for (int j = 0; j < node; j++) {
                if (adj[node][j]) children.push_back(j);
            }

            sort(children.begin(), children.end(), greater<int>());
            for (auto child : children) {
                dfs(child);
            }

            seq.push_back(node + 1);
        };

        dfs(i);
    }

    for (auto x : seq) cout << x << " ";
    cout << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
