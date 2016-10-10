#include <vector>
#include <list>
#include <map>
#include <set>
#include <queue>
#include <deque>
#include <stack>
#include <bitset>
#include <algorithm>
#include <functional>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>

using namespace std;


class ClosestRegex {
    // first index is the end index of the regex atoms
    // second index is the length of the substring of text from the beginning
    // value is the total number of changes for the best possible match at this state
    //  if the value is -1, then that state is undefined
    vector< vector<int> > n_changes;
    vector< vector<string> > n_changes_string;
public:
    string closestString(string text, string regex) {
        // first element is character
        // second element indicates * present
        vector< pair<char, bool> > regex_atoms;
        
        for (auto const& c : regex) {
            if (c == '*') {
                regex_atoms.rbegin()->second = true;
            } else {
                regex_atoms.push_back( make_pair(c, false) );
            }
        }
        
        n_changes.resize(regex_atoms.size(), vector<int>(text.size()+1, -1));
        n_changes_string.resize(regex_atoms.size(), vector<string>(text.size()+1, ""));
        
        for (int regex_index=0; regex_index<regex_atoms.size(); regex_index++) {
            for (int text_length=0; text_length<=text.size(); text_length++) {
                if (text_length > 0) {
                    // when the text length is non-zero
                    if (regex_atoms[regex_index].second == true) {
                        // if the current atom can have any number of repetitions
                        int min_n_change = -1;
                        string best_split_string = "";
                        for (int split_length=0; split_length <= text_length; split_length++) {
                            int n_change = (regex_index == 0) ? n_changes[regex_index][split_length] : n_changes[regex_index-1][split_length];
                            string split_string = (regex_index == 0) ? n_changes_string[regex_index][split_length] : n_changes_string[regex_index-1][split_length];
                            if (n_change == -1) {
                                continue;
                            }
                            int text_index_start = split_length;
                            int text_index_end = text_length-1;
                            for (int i=text_index_start; i<=text_index_end; i++) {
                                if (regex_atoms[regex_index].first != text[i]) {
                                    n_change++;
                                }
                                split_string += regex_atoms[regex_index].first;
                            }
                            if (min_n_change == -1 || n_change < min_n_change || (n_change==min_n_change && lex_compare(split_string, best_split_string)) ) {
                                min_n_change = n_change;
                                best_split_string = split_string;
                            }
                        }
                        n_changes[regex_index][text_length] = min_n_change;
                        n_changes_string[regex_index][text_length] = best_split_string;
                    } else {
                        // if the current atom needs to occur exactly once
                        int n_change = (regex_index == 0) ? 0 : n_changes[regex_index-1][text_length-1];
                        string best_string = (regex_index == 0) ? "" : n_changes_string[regex_index-1][text_length-1];
                        if (n_change == -1 || (regex_index==0 && text_length>1) ) {
                            continue;
                        }
                        int text_index = text_length-1;
                        if (regex_atoms[regex_index].first != text[text_index]) {
                            n_change++;
                        }
                        best_string += regex_atoms[regex_index].first;

                        n_changes[regex_index][text_length] = n_change;
                        n_changes_string[regex_index][text_length] = best_string;
                    }
                } else {
                    // when the text length is zero
                    int n_change = (regex_index == 0) ? 0 : n_changes[regex_index-1][text_length];
                    if (n_change == -1) {
                        continue;
                    }
                    if (regex_atoms[regex_index].second == true) {
                        n_changes[regex_index][text_length] = 0;
                    } else {
                        n_changes[regex_index][text_length] = -1;
                    }
                }
            }
        }
        
        return *(n_changes_string.rbegin()->rbegin());
    }

    bool lex_compare(string const& str1, string const& str2) const {
        return lexicographical_compare(str1.begin(), str1.end(), str2.begin(), str2.end());
    }

    int calculateDifference(string str1, string str2) {
        int diff = 0;
        for (auto i1=str1.cbegin(), i2=str2.cbegin(); i1 != str1.cend(), i2 != str2.cend(); i1++, i2++) {
            if (*i1 != *i2) {
                diff++;
            }
        }
        return diff;
    }

    void debugPrint(void) const {
        for (auto const& i : n_changes) {
            for (auto const& j : i) {
                cout << j << ", ";
            }
            cout << endl;
        }
        for (auto const& i : n_changes_string) {
            for (auto const& j : i) {
                cout << j << ", ";
            }
            cout << endl;
        }
    }
};


int main(int argc, char *argv[]) {
    // string text = "abcd";
    // string regex = "bcdd";
    
    // string text = "topcoder";
    // string regex = "t*px*coa*de*";

    string text = "cmu";
    string regex = "c*m*fm*u*";

    // string text = "abc";
    // string regex = "ab";

    ClosestRegex solution_obj;
    cout << "solution = " << solution_obj.closestString(text, regex) << endl;

    return 0;
}
