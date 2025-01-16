#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N, M;
    cin >> N >> M;

    string P;
    cin >> P;

    vector<vector<ll>> grid(N, vector<ll>(M));
    for (auto &row : grid) {
        for (auto &col : row) {
            cin >> col;
        }
    }

    vector<ll> rowsum(N), colsum(M);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            rowsum[i] += (ll)grid[i][j];
            colsum[j] += (ll)grid[i][j];
        }
    }

    pair<int, int> pos = pair(0, 0);
    vector<pair<int, int>> path = {pos};
    vector<set<int>> rows(N), cols(M);
    for (char d : P) {
        if (d == 'D') pos.first++;
        else pos.second++;

        path.push_back(pos);
    }

    for (auto pos : path) {
        rows[pos.first].insert(pos.second);
        cols[pos.second].insert(pos.first);
    }

    auto update = [&](int row, int col, ll value) -> void {
        rows[row].erase(col);
        cols[col].erase(row);

        grid[row][col] = value;
        rowsum[row] += value;
        colsum[col] += value;
    };

    for (;;) {
        bool modified = false;

        for (int i = path.size() - 1; i >= 0; i--) {
            auto pos = path[i];

            if (rows[pos.first].size() == 1) {
                update(pos.first, pos.second, -rowsum[pos.first]);
                path.erase(path.begin() + i);
                modified = true;
            } else if (cols[pos.second].size() == 1) {
                update(pos.first, pos.second, -colsum[pos.second]);
                path.erase(path.begin() + i);
                modified = true;
            }
        }

        if (!modified) break;
    }

    for (auto &row : grid) {
        for (auto cell : row) cout << cell << " ";
        cout << "\n";
    }
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
