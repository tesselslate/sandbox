#include <bits/stdc++.h>

using namespace std;

#define ll long long

pair<pair<int, int>, pair<int, int>> find_two(set<pair<int, int>> &valid) {
    for (auto i = valid.begin(); i != valid.end(); advance(i, 1)) {
        for (auto j = i; j != valid.end(); advance(j, 1)) {
            int dx = abs(i->first - j->first);
            int dy = abs(i->second - j->second);

            if (dx >= 3 || dy >= 3) {
                return pair(*i, *j);
            }
        }
    }

    return pair(pair(-1, -1), pair(-1, -1));
}

pair<pair<int, int>, pair<int, int>> find_two_joker(set<pair<int, int>> &valid, set<pair<int, int>> &valid_replace) {
    for (auto i : valid) {
        for (auto j : valid_replace) {
            int dx = abs(i.first - j.first);
            int dy = abs(i.second - j.second);

            if (dx >= 3 || dy >= 3) {
                return pair(i, j);
            }
        }
    }

    return find_two(valid_replace);
}

void print_squares(pair<pair<int, int>, pair<int, int>> &squares) {
    cout << "Put the first square to (" << squares.first.first + 1 << ", " << squares.first.second + 1 << ").\n";
    cout << "Put the second square to (" << squares.second.first + 1 << ", " << squares.second.second + 1 << ").\n";
}

int main() {
    const string ranks = "23456789TJQKA";
    const string suits = "CDHS";

    int N, M;
    cin >> N >> M;

    set<string> replacements;
    for (auto rank : ranks) {
        for (auto suit : suits) {
            string card;
            card += rank;
            card += suit;
            replacements.insert(card);
        }
    }

    vector<vector<string>> grid(N, vector<string>(M));
    for (auto &x : grid) {
        for (auto &y : x) {
            cin >> y;
            if (replacements.find(y) != replacements.end()) {
                replacements.erase(y);
            }
        }
    }

    auto check_square = [&](int i, int j) -> bool {
        vector<string> cards;
        for (int di = 0; di < 3; di++) {
            for (int dj = 0; dj < 3; dj++) {
                cards.push_back(grid[i+di][j+dj]);
            }
        }

        // suit check
        bool ok = true;
        for (auto card : cards) {
            if (card[1] != cards[0][1]) {
                ok = false;
                break;
            }
        }
        if (ok) {
            return true;
        }

        // rank check
        set<char> ranks;
        for (auto card : cards) {
            ranks.insert(card[0]);
        }
        return ranks.size() == 9;
    };

    vector<pair<int, int>> jokers;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            if (grid[i][j][0] == 'J' && grid[i][j][1] <= '2') {
                jokers.push_back(pair(i, j));
            }
        }
    }

    set<pair<int, int>> valid;
    for (int i = 0; i < N-2; i++) {
        for (int j = 0; j < M-2; j++) {
            bool ok = true;
            for (auto joker : jokers) {
                if (joker.first >= i && joker.first <= i + 2 && joker.second >= j && joker.second <= j + 2) {
                    ok = false;
                    break;
                }
            }
            if (!ok) {
                continue;
            }

            if (check_square(i, j)) {
                valid.insert(pair(i, j));
            }
        }
    }

    auto found = find_two(valid);
    if (found != pair(pair(-1, -1), pair(-1, -1))) {
        cout << "Solution exists.\n";
        if (jokers.size() == 0) {
            cout << "There are no jokers.\n";
        } else if (jokers.size() == 1) {
            cout << "Replace " << grid[jokers[0].first][jokers[0].second] << " with " << *replacements.begin() << ".\n";
        } else if (jokers.size() == 2) {
            auto second = replacements.begin();
            advance(second, 1);
            cout << "Replace J1 with " << *replacements.begin() << " and J2 with " << *second << ".\n";
        }
        print_squares(found);
        return 0;
    }



    set<pair<int, int>> joker_squares;
    for (auto joker : jokers) {
        for (int i = joker.first; i >= joker.first - 2 && i >= 0; i--) {
            for (int j = joker.second; j >= joker.second - 2 && j >= 0; j--) {
                if (i + 2 < N && j + 2 < M)
                    joker_squares.insert(pair(i, j));
            }
        }
    }

    if (jokers.size() == 1) {
        pair<int, int> joker = jokers[0];
        string joker_card = grid[joker.first][joker.second];

        for (auto card : replacements) {
            grid[joker.first][joker.second] = card;

            set<pair<int, int>> valid_replacements;
            for (auto square : joker_squares) {
                if (check_square(square.first, square.second))
                    valid_replacements.insert(square);
            }

            auto found = find_two_joker(valid, valid_replacements);
            if (found != pair(pair(-1, -1), pair(-1, -1))) {
                cout << "Solution exists.\n";
                cout << "Replace " << joker_card << " with " << card << ".\n";
                print_squares(found);
                return 0;
            }
        }
    } else if (jokers.size() == 2) {
        pair<int, int> a = jokers[0], b = jokers[1];
        string a_card = grid[a.first][a.second], b_card = grid[b.first][b.second];

        for (auto a_repl : replacements) {
            for (auto b_repl : replacements) {
                if (a_repl == b_repl) continue;

                grid[a.first][a.second] = a_repl;
                grid[b.first][b.second] = b_repl;

                set<pair<int, int>> valid_replacements;
                for (auto square : joker_squares) {
                    if (check_square(square.first, square.second))
                        valid_replacements.insert(square);
                }

                auto found = find_two_joker(valid, valid_replacements);
                if (found != pair(pair(-1, -1), pair(-1, -1))) {
                    cout << "Solution exists.\n";
                    if (a_card == "J1") {
                        cout << "Replace J1 with " << a_repl << " and J2 with " << b_repl << ".\n";
                    } else {
                        cout << "Replace J1 with " << b_repl << " and J2 with " << a_repl << ".\n";
                    }
                    print_squares(found);
                    return 0;
                }
            }
        }
    }
    cout << "No solution.\n";
}
