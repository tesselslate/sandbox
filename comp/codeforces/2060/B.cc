#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N, M;
    cin >> N >> M;

    vector<set<int>> cards(N);
    vector<pair<int, int>> cardmap;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            int card;
            cin >> card;
            cards[i].insert(card);
            cardmap.push_back(pair(card, i));
        }
    }

    sort(cardmap.begin(), cardmap.end());

    auto try_pat = [&](vector<int> perm) -> bool {
        int top = -1;

        for (int i = 0; i < N*M; i++) {
            auto card = cardmap[i];

            if (card.second != perm[i%N]) return false;
            top = card.first;
        }

        return true;
    };

    vector<int> perm;
    set<int> seen;
    for (int i = 0; i < N; i++) {
        auto card = cardmap[i];

        if (seen.find(card.second) != seen.end()) {
            cout << "-1\n";
            return;
        }
        seen.insert(card.second);
        perm.push_back(card.second);
    }

    if (try_pat(perm)) {
        for (auto x : perm) {
            cout << (x+1) << " ";
        }
        cout << "\n";
    } else {
        cout << "-1\n";
        return;
    }
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
