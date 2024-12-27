#include <bits/stdc++.h>

using namespace std;

int main() {
    int N, K;
    cin >> N >> K;

    vector<int> places(N);
    for (int i = 0; i < N; i++) {
        cin >> places[i];
    }

    int a = 0;
    for (int i = 0; i < N; i++) {
        if (places[i] >= places[K-1] && places[i] > 0) {
            a++;
        }
    }
    cout << a << "\n";
}
