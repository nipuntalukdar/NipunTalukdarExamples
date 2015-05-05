namespace py lockservice

exception BadOperation {
    1: i32 what,
    2: optional string reason
}

enum LockOperation {
    WRITELOCK,
    READLOCK,
    WRITELOCKIMMD,
    READLOCKIMMD,
    UNLOCK
}

enum StatusMsg {
    SUCCESS,
    FAIL,
    REGISTER_CLIENT,
    HEARTBEAT,
    YOU_WRITELOCKKED,
    LOCK_ALREADY_TAKEN,
    READ_LOCK_ALREADY_TAKEN,
    READ_LOCK_ALREADY_QUEUED,
    WRITE_LOCK_ALREADY_QUEUED,
    CANNOT_LOCK,
    WRITE_LOCK_QUEUED,
    READ_LOCK_QUEUED,
    CLIENT_NOT_REGISTERED,
    LOCK_NOT_GRANTED,
    LOCK_INVALID_OP,
    LOCK_NOT_OWNER,
    WRITE_LOCK_OWNER_CHANGED,
    WRITE_CHANGED_TO_READ_LOCK,
    READ_CHANDGED_TO_WRIOTE_LOCK,
    LOCK_CAN_BE_REMOVED,
    ONE_READ_LOCK_REMOVED
}

struct LockCommand {
    1: LockOperation op,
    2: string lockId,
    3: i64 expireTime
}

struct LockDetails {
    1: string currentWriter,
    2: list<string> currentReaders,
    3: list<string> currentWriteWaits,
    4: string lockType
}

struct ClientLocks {
    1: list<string> reads,
    2: list<string> readWaits,
    3: list<string> writes,
    4: list<string> writeWaits
}

struct LockCommandBatch {
    1: list<LockCommand> locks
}

service LockService {
    StatusMsg lockOp(1:string clientId, 2:LockCommand cmd) throws (1:BadOperation badop)
    i32 registerClient(1:string clientId)
    i32 reRegisterLocks(1:string clientId, 2:LockCommandBatch locks)
    i32 sendHeartBeat(1:string clientId)
    LockDetails getLockDetails(1: string lockId)
    list<string> getLiveClients()
    StatusMsg unRegisterClient(1:string clientId)
    ClientLocks getClientLocks(1:string clientId) 
}
