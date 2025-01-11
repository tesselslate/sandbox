#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N, W, H;
    cin >> N >> W >> H;

    map<int, map<int, int>> sorted;
    for (int i = 0; i < N; i++) {
        int w, h;
        cin >> w >> h;
        sorted[w][h] = i;
    }

    vector<int> DP_SIZE(N+1, -1), DP_PATH(N+1, -1);

    function<int(int, int, int)> search = [&](int width, int height, int id) -> int {
        if (DP_SIZE[id] >= 0) {
            return DP_PATH[id];
        }

        int best_size = 0;
        int best_path = -1;

        for (auto w = sorted.lower_bound(width + 1); w != sorted.end(); w++) {
            auto h = w->second.lower_bound(height + 1);
            for (auto h = w->second.lower_bound(height + 1); h != w->second.end(); h++) {
                auto next = search(w->first, h->first, h->second);

                if (DP_SIZE[h->second] > best_size) {
                    best_size = DP_SIZE[h->second];
                    best_path = h->second;
                }
            }
        }

        DP_SIZE[id] = best_size + 1;
        DP_PATH[id] = best_path;
        return best_path;
    };

    int next = search(W, H, N);
    if (next == -1) {
        cout << "0\n";
    } else {
        cout << DP_SIZE[N] - 1 << "\n";
        while (next != -1) {
            cout << next + 1 << " ";
            next = DP_PATH[next];
        }
        cout << "\n";
    }
}
