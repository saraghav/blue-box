#include <iostream>
#include <cstdio>
#include <cmath>
#include <string>
#include <vector>
using namespace std;

string get_expression(int const& N, int const& S);
string form_expression(vector<char> const& sign);

int main(int argc, char *argv[]) {
    int N, S;
    scanf("%d %d", &N, &S);

    string result = get_expression(N, S);
    cout << result;

    return 0;
}

string get_expression(int const& N, int const& S) {
    string const impossible = "Impossible";

    vector<bool> num_taken(N+1, false);
    num_taken[0] = true; // does not exist
    num_taken[1] = true; // always positive
    vector<char> sign(N+1, '+');
    sign[0] = '\0'; // does not exist
    sign[1] = '\0'; // always positive

    int sum = N*(N+1) / 2;

    int numbers_left = N-1;
    while (numbers_left > 0) {
        if (sum > S) {
            int desired = abs( (sum-S)/2 );
            if (desired > N) {
                desired = N;
            }
            while (desired > 1) {
                if (!num_taken[desired]) {
                    sum -= 2*desired;
                    num_taken[desired] = true;
                    sign[desired] = '-';
                    numbers_left--;
                    break;
                }
                desired--;
            }

            if (desired <= 1) {
                break;
            }
        } else {
            break;
        }
    }

    if (sum == S) {
        return form_expression(sign);
    } else {
        return impossible;
    }
}

string form_expression(vector<char> const& sign) {
    string expression = "";
    for (int i=1; i<sign.size(); i++) {
        expression += (sign[i] + to_string(i));
    }
    return expression;
}
