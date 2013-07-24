/*
 * In this example we demonstrate a simple way to delete nodes in the zookeeper
 * server. Twenty nodes will be deleted with path /testpath0, /testpath1,
 * /testpath2, /testpath3, ....., /testpath19.
 * All these nodes will be initialized to the same value "myvalue1".
 * We will use zookeeper synchronus API to create the nodes. As soon as our
 * client enters connected state, we start creating the nodes.
 * 
 * Zookeeper version used is 3.4.5
 * We may use the zookeeper client program to get the nodes and examine their
 * contents.
 * Suppose you have downloaded and extracted zookeeper to a directory 
 * /home/yourdir/packages/zookeeper-3.4.5 . Then after you build the C libraries
 * ,they will be available at /home/yourdir/packages/zookeeper-3.4.5/src/c/.libs/
 * and the c command line tool will available at 
 * /home/yourdir/packages/zookeeper-3.4.5/src/c. The command line tools are cli_st
 * and cli_mt and cli. They are convenient tool to examine zookeeper data.
 * 
 * Compile the below code as shown below:
 * $gcc -o testzk1 zoo_create_node.c -I \
 * /home/yourdir/packages/zookeeper-3.4.5/src/c/include -I \ 
 * /home/yourdir/packages/zookeeper-3.4.5/src/c/generated -L \
 * /home/yourdir/packages/zookeeper-3.4.5/src/c/.libs/ -lzookeeper_mt
 *
 * Make sure that your LD_LIBRARY_PATH includes the zookeeper C libraries to run
 * the example. Before you run the example, you have to configure and run the
 * zookeeper server. Please go through the zookeeper wiki how to do that. 
 * Now you run the example as shown below:
 * ./testzk1 127.0.0.1:22181  # Assuming zookeeper server is listening on port
 * 22181 and IP 127.0.0.1 
 * Now use one of the cli tools to examine the znodes created and also their
 * values.
 *
 */
 

#include <unistd.h>
#include <sys/select.h>
#include <sys/time.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>

#include <zookeeper.h>
static const char *hostPort;
static zhandle_t *zh;
static clientid_t myid;
static int connected;

void watcher(zhandle_t *zzh, int type, int state, const char *path,
             void* context)
{
    if (type == ZOO_SESSION_EVENT) {
        if (state == ZOO_CONNECTED_STATE) {
            connected = 1;
        } else if (state == ZOO_AUTH_FAILED_STATE) {
            zookeeper_close(zzh);
            exit(1);
        } else if (state == ZOO_EXPIRED_SESSION_STATE) {
            zookeeper_close(zzh);
            exit(1);
        }
    }
}


int main(int argc, char *argv[])
{
    int rc;
    int fd;
    int interest;
    int events;
    struct timeval tv;
    fd_set rfds, wfds, efds;

    if (argc != 2) {
        fprintf(stderr, "USAGE: %s host:port\n", argv[0]);
        exit(1);
    }

    FD_ZERO(&rfds);
    FD_ZERO(&wfds);
    FD_ZERO(&efds);

    zoo_set_debug_level(ZOO_LOG_LEVEL_WARN);
    zoo_deterministic_conn_order(1); 
    hostPort = argv[1];
    int x = 0;
    zh = zookeeper_init(hostPort, watcher, 4000, 0, 0, 0);
    if (!zh) {
        return errno;
    }
    while (1) {
        char mypath[255];
        zookeeper_interest(zh, &fd, &interest, &tv);
        usleep(10);
        memset(mypath, 0, 255);
        if (connected) {
            while (x < 20) {
                sprintf(mypath, "/testpath%d", x);
                usleep(10);
                rc = zoo_delete(zh, mypath, -1);
                if (rc != ZOK){
                    printf("Problems %s %d\n", mypath, rc);
                } else {
                    printf("Deleted %s\n", mypath);
                }

                x++;
            }
            connected++;
        }
        if (fd != -1) {
            if (interest&ZOOKEEPER_READ) {
                FD_SET(fd, &rfds);
            } else {
                FD_CLR(fd, &rfds);
            }
            if (interest&ZOOKEEPER_WRITE) {
                FD_SET(fd, &wfds);
            } else {
                FD_CLR(fd, &wfds);
            }
        } else {
            fd = 0;
        }
        rc = select(fd+1, &rfds, &wfds, &efds, &tv);
        events = 0;
        if (rc > 0) {
            if (FD_ISSET(fd, &rfds)) {
           	    events |= ZOOKEEPER_READ;
            }
            if (FD_ISSET(fd, &wfds)) {
                events |= ZOOKEEPER_WRITE;
            }
        }
        zookeeper_process(zh, events);
        if (2 == connected ) {
            // We created the nodes, so we will exit now
            zookeeper_close(zh);
            break;
        }   
    }
    return 0;
}
