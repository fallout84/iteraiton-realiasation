#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <cmath>
#include <chrono>
#include <iomanip>

using namespace std;

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

// норма чебишева
double matrixNormInf(const vector<vector<double>>& A) {
    double max_sum = 0;
    for (const auto& row : A) {
        double current_sum = 0;
        for (double val : row) current_sum += abs(val);
        if (current_sum > max_sum) max_sum = current_sum;
    }
    return max_sum;
}

int main() {
    auto A = loadMatrix("../data/A_5_1.txt");
    auto b = loadVector("../data/b_5_1.txt");
    int n = A.size();
    if (n == 0 || A[0].size() != n || b.size() != n) {
        cerr << "Ошибка размерности!" << endl;
        return 1;
    }
    cout << "Размерность сошлась: " << n << "x" << n << endl;
    vector<double> x(n, 0.0);
    vector<double> err;
    vector<double> time_points;

    double tau = 1.0 / matrixNormInf(A);
    auto start_time = chrono::high_resolution_clock::now();

    for (int k = 0; k < 1000; ++k) {
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
        if (r_norm < 0.01) {
            cout << "Процесс завершен на " << k << " шаге" << endl;
            break;
        }
        if (k > 0 && err[k] > err[0]) {
            cerr << "Ошибка растёт, пора грустить." << endl;
            return 1;
        }
    }
    ofstream f_err("../result/output_err_1_cpp.txt");
    ofstream f_time("../result/output_time_1_cpp.txt");

    f_err << scientific << setprecision(18);
    f_time << scientific << setprecision(18);

    for (size_t i = 0; i < err.size(); ++i) {
        f_err << err[i] << (i == err.size() - 1 ? "" : ", ");
        f_time << time_points[i] << (i == time_points.size() - 1 ? "" : ", ");
    }
    return 0;
}