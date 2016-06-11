namespace go dcache

struct PutCommand {
    1: string Key,
    2: binary data
}

struct GetResponse {
    1: string Key
    2: optional binary data
}



service DcacheService {
    bool Put(1:PutCommand Put)
    GetResponse Get(1:string Key)
}
