// Below is a an example how you print the valid combination of parenthesis
// e.g. if you have 3 pairs of parenthesis, you have to print out the
// all the valid combination,
// i.e. 
// ()()()
// ((()))
// (())()
//
// etc. etc.
//
// How does it work ?
// Basically we take a valid prefix of combination and pass along a possible
// suffix and recursively add a elements to the valid prefix in such a way that
// the prefix always remains valid. When the suffix becomes null, we print
// out the prefix. We express the suffix by the number of open and close
// parenthesis left
//

// Function is_valid_prefix
// A open parenthesis much be followed by a open parenthesis or a closed one,
// but number of closed parenthesis must not outnumber open parenthesis
// We assumed that prefix only contains '(' or ')'
//
// Returns 0 if invalid prefix and 1 if a valid prefix

#include <stdio.h>
#include <string.h>

int is_valid_prefix(const char *prefix, int len)
{
    int i = 0;
    int right_parenthesis_more = 0;
    while ( i < len) {
        if (prefix[i] == '(') 
            right_parenthesis_more++;
        else
            right_parenthesis_more--;
        if (right_parenthesis_more < 0)
            return 0;
        i++;
    }
    return right_parenthesis_more >= 0;
}

void print_valid_parenthesis_combination(const char *prefix, int prefix_size, int open_left, int close_left)
{
    char myprefix[512] = "";
    if (0 == close_left ) {
        printf("%s\n", prefix);
        return;
    }
    memset(myprefix, 0, 512);
    if (prefix_size > 0) {
        strncpy(myprefix, prefix, prefix_size);
    }
    if (open_left > 0) {
        myprefix[prefix_size] = '(';
        print_valid_parenthesis_combination(myprefix, prefix_size + 1, open_left -1 , close_left);
    }
    if (close_left > 0) {
        myprefix[prefix_size] = ')';
        if (is_valid_prefix(myprefix, prefix_size + 1))
            print_valid_parenthesis_combination(myprefix, prefix_size + 1, open_left , close_left - 1);
    }
}

int main()
{
    // Print out valid combination of parenthesis for 5 () pairs
    print_valid_parenthesis_combination(0, 0, 5, 5);

    return 0;
}
