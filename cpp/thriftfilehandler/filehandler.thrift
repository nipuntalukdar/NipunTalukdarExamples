namespace cpp FileHandler

cpp_include "<stdint.h>"
cpp_include "<inttypes.h>"

exception BadOperation {
    1: i32 what,
    2: optional string reason
}

enum Operation {
    CREATE,
    DELETE,
    FILECONTENT,
    DIRCONTENT
}

struct Work {
    1: Operation op
    2: string filename
    3: string data
    4: string rootdir
}


service FileService {
    i32 createFile(1:Work w) throws (1:BadOperation badop),
    list<string> getFiles(1:Work w) throws (1:BadOperation badop)


}
