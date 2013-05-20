namespace cpp RemoteCommand

cpp_include "<stdint.h>"
cpp_include "<inttypes.h>"

exception BadOperation {
    1: i32 what,
    2: optional string reason
}

enum Operation {
    EXECUTEBIN,
    EXECUTESCRIPT
}

struct Command {
    1: Operation op
    2: string commandFile
    3: bool isBinary
    4: list <string> parameters
    5: string stdErrorFile
    6: string stdOutFile
    7: bool daemonize 
}


service RemoteCommandService {
    i32 executeCommand(1:Command cmd) throws (1:BadOperation badop)
}
