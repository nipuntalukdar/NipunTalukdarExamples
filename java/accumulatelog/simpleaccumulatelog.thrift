namespace java geet.simple.accumulatelog

exception BadOperation {
    1: i32 what,
    2: optional string reason
}

enum Operation {
    ADDLOG
}

struct LogData {
    1: Operation op
    2: string logData
}


service AccumulateLogService {
    i32 addLog(1:LogData data) throws (1:BadOperation badop)
}
