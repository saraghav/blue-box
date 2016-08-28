#include <iostream>
#include <cstdio>
#include <cmath>
#include <string>
#include <vector>
using namespace std;

string const get_expression(int const& N, int const& S);
string const form_expression(vector<char> const& sign);

int main(int argc, char *argv[]) {
    int N, S;
    scanf("%d %d", &N, &S);

    string const result = get_expression(N, S);
    cout << result << endl;

    return 0;
}

string const get_expression(int const& N, int const& S) {
    string const impossible = "Impossible";

    vector<char> sign(N+1, '+');
    sign[0] = '\0'; // does not exist
    sign[1] = '\0'; // always positive

    int sum = N*(N+1) / 2;
    int desired = (sum-S)/2;

    for (int current_num=N; current_num>1; current_num--) {
        if (desired <= 1) {
            break;
        } else {
            // because 1 cannot change sign, the smallest pair can only be 2+some_number = desired
            if (current_num == desired || current_num <= (desired-2)) {
                sum -= 2*current_num;
                sign[current_num] = '-';
                desired = (sum-S)/2;
            }
        }
    }

    if (sum == S) {
        return form_expression(sign);
    } else {
        return impossible;
    }
}

string const form_expression(vector<char> const& sign) {
    string expression = "";
    for (int i=1; i<sign.size(); i++) {
        expression += (sign[i] + to_string(i));
    }
    return expression;
}
