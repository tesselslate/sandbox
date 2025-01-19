#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N;
    cin >> N;

    int levels = 0;
    int sum = 0;

    for (int i = 1; i < 100000; i++) {
        sum += i;
        if (sum > N) break;
        N -= sum;
        levels++;
    }

    cout << levels << "\n";
}
