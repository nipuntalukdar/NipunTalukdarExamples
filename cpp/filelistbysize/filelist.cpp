#include <iostream>
#include <iterator>
#include <queue>
#include <vector>
#include <map>
#include <algorithm>
#include <boost/filesystem.hpp>

using namespace std;
using namespace boost::filesystem;

int main(int argc, char *argv[])
{
    queue<path> directories;
    multimap<uintmax_t, path> filesizes;

    if (argc < 2) {
        cout << "Usage: " << argv[1] <<  " path\n";
        return 1;
    }
    path p(argv[1]); 

    try {
        if (exists(p)){
            if (is_regular_file(p)){
                cout << file_size(p) << "  " << p << endl;
                return 0;
            }

            if (!is_directory(p)) {
                return 0;
            }
            directories.push(p);
            vector <path> entries;
            path thispath;
            while (!directories.empty()) {
                thispath = directories.front();
                directories.pop();
                copy(directory_iterator(thispath), directory_iterator(), back_inserter(entries));
                for (vector <path>::iterator it = entries.begin();
                        it != entries.end(); ++it) {
                    if (!exists(*it))
                        continue;
                    if (!is_symlink(*it) && is_directory(*it)) {
                        directories.push(*it);
                    } else if (is_regular(*it)) {
                        uintmax_t file_siz = file_size(*it);
                        filesizes.insert(pair<uintmax_t, path>(file_siz, *it));
                    }
                }
                entries.clear();
            }
        }
        for (multimap<uintmax_t, path>::iterator it1 = filesizes.begin(), it2 = filesizes.end();
                it1 != it2; ++it1) {
            cout << it1->first << " " << it1->second << endl;
        }
        filesizes.clear();
    } catch(const filesystem_error & ex) {
        cout << ex.what() << '\n';
    }
    return 0;
}
