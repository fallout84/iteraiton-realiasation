#include <iostream>
#include <vector>
#include <fstream>
#include <iomanip>

using namespace std;

int main() {
    double k = 1.0, f = 1.0;
    double a = 0.0, bx = 1.0;
    double y0 = 0.0, y1 = 1.0;
    int n = 20;
    cout << "k,f,a,bx,y0,y1,n";
    if (!(cin >> k >> f >> a >> bx >> y0 >> y1 >> n)) {
        cerr << "Input error. Exiting.\n";
        return 1;
    }

    double h = (bx - a) / (n + 1);
    vector<vector<double>> A(n, vector<double>(n, 0.0));
    vector<double> B(n, 2.0 * h * f);
    for (int i = 0; i < n; ++i) {
        A[i][i] = 2.0 * h * k;
        if (i > 0) {
            A[i][i - 1] = -1.0;
        }
        else {
            B[i] += y0;
        }

        if (i < n - 1) {
            A[i][i + 1] = 1.0;
        }
        else {
            B[i] -= y1;
        }
    }
    ofstream fileA("../data/A.txt");
    ofstream fileB("../data/b.txt");

    fileA << scientific << setprecision(15);
    fileB << scientific << setprecision(15);

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            fileA << A[i][j] << " ";
        }
        fileA << "\n";
        fileB << B[i] << "\n";
    }

    return 0;
}