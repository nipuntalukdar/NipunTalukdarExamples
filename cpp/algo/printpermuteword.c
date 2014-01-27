// Below is the code for printing permutations of an word. Here I am 
// not taking into account the case of repeated letters. Which results
// in printing duplicates. More thoughts for avoiding printing duplicates
// efficiently. I don't want to use a store the words and printing them
// at them at the end. I want an algorithmic way out to solve the issue
// 
// How does it work ?
// Suppose your whord has 'n' chars,
// then first letter of your word can have n options,
// second n -1 options
// third n -2 options
// and so on....
// last will have just one option.
// Trick is to add the options successively to the prefix, and sending 
// the suffix (i.e.) the options for remaining positions to function
// and call the function print_permutations_word repeatedly
//

#define MAX_WORD_LEN 52

#include <string.h>
#include <stdio.h>

int print_permutations_word(const char *prefix, const char *suffix, int suffixlen)
{
    char myprefix[MAX_WORD_LEN]  = "";
    char mysuffix[MAX_WORD_LEN] = "";
    int i = 0, j = 0, k = 0;
    if (suffixlen == 0) {
        printf("word %s\n", prefix);
        return 0;
    }

    while (i < suffixlen) {
        memset(myprefix, 0, MAX_WORD_LEN);
        memset(mysuffix, 0, MAX_WORD_LEN);
        snprintf(myprefix,MAX_WORD_LEN,"%s%c", prefix,suffix[i]);
        j = 0;
        k = 0;
        while (j < suffixlen) {
           if (i != j){
                mysuffix[k++] = suffix[j];
           }
           j++;
        }
        i++;
        print_permutations_word(myprefix,  mysuffix, suffixlen - 1);
    }
    return 0;
}

#if 0
//example run
int main()
{
    print_permutations_word("", "abcde", 5);
    return 0;
}
#endif
