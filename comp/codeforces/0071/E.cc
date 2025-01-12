#include <bits/stdc++.h>

using namespace std;

#define ll long long

int main() {
    const vector<string> table = {
        "H",  "He", "Li", "Be", "B",  "C",  "N",  "O",  "F",  "Ne",
        "Na", "Mg", "Al", "Si", "P",  "S",  "Cl", "Ar", "K",  "Ca",
        "Sc", "Ti", "V",  "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
        "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y",  "Zr",
        "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
        "Sb", "Te", "I",  "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
        "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
        "Lu", "Hf", "Ta", "W",  "Re", "Os", "Ir", "Pt", "Au", "Hg",
        "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
        "Pa", "U",  "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    };

    map<string, int> rtable;
    for (int i = 0; i < table.size(); i++) {
        rtable[table[i]] = i + 1;
    }

    int N, K;
    cin >> N >> K;

    vector<int> reactants(N);
    for (auto &x : reactants) {
        string elem;
        cin >> elem;
        x = rtable[elem];
    }

    sort(reactants.begin(), reactants.end());

    vector<int> products(K);
    for (auto &x : products) {
        string elem;
        cin >> elem;
        x = rtable[elem];
    }

    vector<int> product_stack = products;
    reverse(products.begin(), products.end());

    set<pair<uint32_t, int>> DP;

    vector<uint32_t> solutions;
    function<void(uint32_t, uint32_t, int)> search = [&](uint32_t available, uint32_t used, int target) -> void {
        if (target == 0) {
            solutions.push_back(used);

            if (product_stack.size() == 0) {
                cout << "YES\n";
                for (int i = 0; i < K; i++) {
                    auto product = products[i];
                    auto solution = solutions[i];

                    vector<string> parts;
                    for (int j = 0; j < N; j++) {
                        if (solution & (1 << j)) {
                            parts.push_back(table[reactants[j] - 1]);
                        }
                    }

                    for (int j = 0; j < parts.size() - 1; j++) {
                        cout << parts[j] << "+";
                    }
                    cout << parts.back() << "->" << table[product - 1] << "\n";
                }
                exit(0);
            }

            target = product_stack.back(); product_stack.pop_back();
            search(available, 0, target);
            product_stack.push_back(target);
            solutions.pop_back();
        }

        if (DP.find(pair(available, target)) != DP.end()) {
            return;
        }

        for (int i = 0; i < N; i++) {
            int mask = (1 << i);
            if ((available & mask) == 0) continue;

            search(available & ~mask, used | mask, target - reactants[i]);
        }

        DP.insert(pair(available, target));
    };

    int product = product_stack.back(); product_stack.pop_back(); 
    search((1 << N) - 1, 0, product);
    cout << "NO\n";
}
