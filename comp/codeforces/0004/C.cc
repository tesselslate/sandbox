#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    int N;
    cin >> N;

    map<string, int> names;
    for (int i = 0; i < N; i++) {
        string name;
        cin >> name;

        auto it = names.find(name);
        if (it == names.end()) {
            names[name] = 0;
            cout << "OK\n";
        } else {
            int id = it->second + 1;
            cout << name << id << "\n";
            names[name]++;
        }
    }
}
