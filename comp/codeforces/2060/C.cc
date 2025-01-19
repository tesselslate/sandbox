#include <bits/stdc++.h>

using namespace std;

#define ll long long

void test_case() {
    int N, K;
    cin >> N >> K;

    map<int, int> numbers;
    int score = 0;
    for (int i = 0; i < N; i++) {
        int num;
        cin >> num;

        if (numbers.find(K-num) != numbers.end()) {
            numbers[K-num]--;
            if (numbers[K-num] == 0) numbers.erase(K-num);
            score++;
        } else {
            numbers[num]++;
        }
    }

    cout << score << "\n";
}

int main() {
    int T;
    cin >> T;
    for (int i = 0; i < T; i++) test_case();
}
