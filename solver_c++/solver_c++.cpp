#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <cmath>
#include <chrono>
#include <iomanip>
#include <clocale>
using namespace std;
// коэфф определяющий малость *шага*
int k1 = 1000;

// читаем матрицу из файла
vector<vector<double>> loadMatrix(string path) {
    vector<vector<double>> matrix;
    ifstream file(path);
    string line;
    while (getline(file, line)) {
        stringstream ss(line);
        double val;
        vector<double> row;
        while (ss >> val) row.push_back(val);
        if (!row.empty()) matrix.push_back(row);
    }
    return matrix;
}

// читаем вектор из файла
vector<double> loadVector(string path) {
    vector<double> vec;
    ifstream file(path);
    double val;
    while (file >> val) vec.push_back(val);
    return vec;
}

int main() {
    setlocale(LC_ALL, "Russian");
    auto A = loadMatrix("../data/A.txt");
    auto b = loadVector("../data/b.txt");
    int n = A.size();
    if (A[0].size() != n || b.size() != n) {
        cerr << "Ошибка размерности!" << endl;
        return 1;
    }
    cout << "Размерность сошлась: " << n << "x" << n << endl;
    vector<double> x(n, 0.0);
    vector<double> err;
    vector<double> time_points;

    double tau = A[0][0]/k1;
    auto start_time = chrono::high_resolution_clock::now();

    for (int k = 0; k < 5000000; ++k) {
        vector<double> r(n);
        double r_norm = 0;
        for (int i = 0; i < n; ++i) {
            double Ax_i = 0;
            for (int j = 0; j < n; ++j) {
                Ax_i += A[i][j] * x[j];
            }
            r[i] = b[i] - Ax_i;
            r_norm += r[i] * r[i];
        }
        r_norm = sqrt(r_norm);
        auto current_time = chrono::high_resolution_clock::now();
        chrono::duration<double> elapsed = current_time - start_time;

        err.push_back(r_norm);
        time_points.push_back(elapsed.count());
        for (int i = 0; i < n; ++i) {
            x[i] += tau * r[i];
        }

    }
    ofstream f_err("../result/output_err_cpp.txt");
    ofstream f_time("../result/output_time_cpp.txt");
    ofstream f_dot("../result/output_dot_cpp.txt");
    f_err << scientific << setprecision(18);
    f_time << scientific << setprecision(18);

    for (size_t i = 0; i < err.size(); ++i) {
        f_err << err[i] << (i == err.size() - 1 ? "" : ", ");
        f_time << time_points[i] << (i == time_points.size() - 1 ? "" : ", ");
    }for (size_t i = 0; i < x.size(); ++i) {
        f_dot << x[i] << (i == x.size() - 1 ? "" : ", ");
    }

    return 0;
}