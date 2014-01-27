#include <signal.h>
#include <pthread.h>
#include <platform.h>
#include <microhttpd.h>
#include <iostream>
#include <map>
#include <string>

#include <api.hpp>

using std::map;
using std::string;

#define PAGE "<html><head><title>Error</title></head><body>Bad data</body></html>"

static int shouldNotExit = 1;

static int send_bad_response( struct MHD_Connection *connection)
{
    static char *bad_response = (char *)PAGE;
    int bad_response_len = strlen(bad_response);
    int ret;
    struct MHD_Response *response;

    response = MHD_create_response_from_buffer ( bad_response_len,
                bad_response,MHD_RESPMEM_PERSISTENT);
    if (response == 0){
        return MHD_NO;
    }
    ret = MHD_queue_response (connection, MHD_HTTP_OK, response);
    MHD_destroy_response (response);
    return ret;
}


static int get_url_args(void *cls, MHD_ValueKind kind,
                    const char *key , const char* value)
{
    map<string, string> * url_args = static_cast<map<string, string> *>(cls);

    if (url_args->find(key) == url_args->end()) {
         if (!value)
             (*url_args)[key] = "";
         else 
            (*url_args)[key] = value;
    }
    return MHD_YES;

}
                
static int url_handler (void *cls,
    struct MHD_Connection *connection,
    const char *url,
    const char *method,
    const char *version,
    const char *upload_data, size_t *upload_data_size, void **ptr)
{
    static int aptr;
    const char *fmt = (const char *)cls;
    const char *val;
    char *me;
    const char *typexml = "xml";
    const char *typejson = "json";
    const char *type = typejson;

    struct MHD_Response *response;
    int ret;
    map<string, string> url_args;
    map<string, string>:: iterator  it;
    ourapi::api callapi;
    string respdata;

    // Support only GET for demonstration
    if (0 != strcmp (method, "GET"))
        return MHD_NO; 


    if (&aptr != *ptr) {
        *ptr = &aptr;
        return MHD_YES;
    }


    if (MHD_get_connection_values (connection, MHD_GET_ARGUMENT_KIND, 
                           get_url_args, &url_args) < 0) {
        return send_bad_response(connection);

    }

    callapi.executeAPI(url, url_args, respdata);

    *ptr = 0;                  /* reset when done */
    val = MHD_lookup_connection_value (connection, MHD_GET_ARGUMENT_KIND, "q");
    me = (char *)malloc (respdata.size() + 1);
    if (me == 0)
        return MHD_NO;
    strncpy(me, respdata.c_str(), respdata.size() + 1);
    response = MHD_create_response_from_buffer (strlen (me), me,
					      MHD_RESPMEM_MUST_FREE);
    if (response == 0){
        free (me);
        return MHD_NO;
    }

    it = url_args.find("type");
    if (it != url_args.end() && strcasecmp(it->second.c_str(), "xml") == 0)
        type = typexml;

    MHD_add_response_header(response, "Content-Type", "text");
    MHD_add_response_header(response, "OurHeader", type);

    ret = MHD_queue_response (connection, MHD_HTTP_OK, response);
    MHD_destroy_response (response);
    return ret;
}

void handle_term(int signo)
{
    shouldNotExit = 0;
}

void* http(void *arg)
{
    int *port = (int *)arg;
    struct MHD_Daemon *d;

    d = MHD_start_daemon (MHD_USE_SELECT_INTERNALLY | MHD_USE_DEBUG | MHD_USE_POLL,
                        *port,
                        0, 0, &url_handler, (void *)PAGE, MHD_OPTION_END);
    if (d == 0){
        return 0;
    }
    while(shouldNotExit) {
        sleep(1);
    }
    MHD_stop_daemon (d);
    return 0;
}

int main (int argc, char *const *argv)
{

    if (argc != 2){
        printf ("%s PORT\n", argv[0]);
        exit(1);
    }
    daemon(0,0);
    signal(SIGTERM, handle_term);
    int port = atoi(argv[1]);
    pthread_t  thread;
    if ( 0 != pthread_create(&thread, 0 , http, &port)){
        exit(1);
    }
    pthread_join(thread, 0);
    return 0;
}
