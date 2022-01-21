#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

namespace py = pybind11;

#include <vector>
#include <string>
#include <map>
#include <algorithm>

using namespace std;

vector<string> tokens_by_prio(string text, const vector<string>& prio_lexer_rules){
    vector<pair<size_t, size_t> > tokenized;
    string original = text;

    // prefilter rules
    vector<string> rules;
    copy_if(prio_lexer_rules.begin(), prio_lexer_rules.end(), back_inserter(rules),
        [&text](const string& s) -> size_t {
            return text.find(s) != string::npos;
    });
    size_t n_rules = rules.size();
    if (n_rules==0){
        return vector<string>();
    }
    size_t n_text = text.size();
    size_t chars_to_fit = n_text;
    size_t rule_ix = 0;
    size_t fit_i = 0;

    while(chars_to_fit>0){
        // try to fit rules.
        // if a rule fits from index, we add rule index to the tokenized
        const string& current_rule = rules[rule_ix];
        fit_i = text.find(current_rule, fit_i);  // we don't need "found" as in the python code
        if (fit_i != string::npos){
            size_t n_rule = current_rule.size();
            tokenized.push_back(make_pair(rule_ix, fit_i));
            // and move index
            chars_to_fit -= n_rule;
            // replace the token in the string with '='
            text.replace(fit_i, n_rule, n_rule, '=');
            rule_ix = 0;
        }
        else{
            fit_i = 0;
            rule_ix += 1;
        }
        // if nothing fits at the moment,
        while (rule_ix == n_rules){
            // take back one step and try to fit the rules, starting from last rule_ix + 1
            if (tokenized.size()>0){
                pair<size_t, size_t> data = tokenized.back();
                tokenized.pop_back();
                rule_ix = data.first;
                fit_i = data.second;
            } else{
                // if we backtracked to the beginning => failed.
                return vector<string>();
            }
            size_t n_rule = rules[rule_ix].size();
            chars_to_fit += n_rule;
            // put back the token from the original string
            text.replace(fit_i, n_rule, original, fit_i, n_rule);
            ++fit_i;
        }
    }
    sort(tokenized.begin(), tokenized.end(), [](auto &left, auto &right) -> bool {
        return left.second < right.second;
    });
    vector<string> result;
    transform(tokenized.begin(), tokenized.end(), back_inserter(result),
        [&rules](const auto& rule_fit_pair) -> string{
            return rules[rule_fit_pair.first];
        }
    );
    return result;
}

string get_pron(const vector<string>& tokens, const unordered_map<string, string> rules){
    string result;
    for(size_t i=0; i<tokens.size(); ++i){
        result += rules.at(tokens[i]);
    }
    return result;
}

PYBIND11_MODULE(prio_lexer, m) {
    py::bind_vector<std::vector<std::string> >(m, "VectorStr");

    m.doc() = "pybind11 prio lexer";

    m.def("prio_lexer_tokenize", &tokens_by_prio, "Tokenizes string using prio rules.");
    m.def("get_pron", &get_pron, "Transforms tokenized text into pronunciation.");
}