/*
 * In this example we demonstrate a simple way to watch the appearance of a node
 * in the server.
 * In this program we will watch for the appearance of a node
 * "/testforappearance". Once we create the node from another program, the watch
 * event will be sent to the client and the watcher routine woll be called.
 *
 * We will use zookeeper synchronus API to watch the node. As soon 
 * as our client enters connected state, we will set a watch for the node.
 * 
 * All the examples used latest stable version of zookeeper that is version
 * 3.3.6
 * We may use the zookeeper client program to get the nodes and examine their
 * contents.
 * Suppose you have downloaded and extracted zookeeper to a directory 
 * /home/yourdir/packages/zookeeper-3.3.6 . Then after you build the C libraries
 * ,they will be available at /home/yourdir/packages/zookeeper-3.3.6/src/c/.libs/
 * and the c command line tool will available at 
 * /home/yourdir/packages/zookeeper-3.3.6/src/c. The command line tools are cli_st
 * and cli_mt and cli. They are convenient tool to examine zookeeper data.
 * 
 * Compile the below code as shown below:
 * $gcc -o testzk1 zoo_exist_watch.c -I \
 * /home/yourdir/packages/zookeeper-3.3.6/src/c/include -I \ 
 * /home/yourdir/packages/zookeeper-3.3.6/src/c/generated -L \
 * /home/yourdir/packages/zookeeper-3.3.6/src/c/.libs/ -lzookeeper_mt
 *
 * Make sure that your LD_LIBRARY_PATH includes the zookeeper C libraries to run
 * the example. Before you run the example, you have to configure and run the
 * zookeeper server. Please go through the zookeeper wiki how to do that. 
 * Now you run the example as shown below:
 * ./testzk1 127.0.0.1:22181  # Assuming zookeeper server is listening on port
 * 22181 and IP 127.0.0.1 
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
static char mycontext[] = "This is context data for test";

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

void watchexistence(zhandle_t *zzh, int type, int state, const char *path,
             void* context)
{
    static struct Stat st;
    int rc;

    if (type == ZOO_SESSION_EVENT) {
        if (state == ZOO_CONNECTED_STATE) {
            return;
        } else if (state == ZOO_AUTH_FAILED_STATE) {
            zookeeper_close(zzh);
            exit(1);
        } else if (state == ZOO_EXPIRED_SESSION_STATE) {
            zookeeper_close(zzh);
            exit(1);
        }
    } else if (type == ZOO_CREATED_EVENT) {
        printf("Node appeared %s, now Let us watch for its delete \n", path);
        rc = zoo_wexists(zh, path, 
                watchexistence , mycontext, &st);
        if (ZOK != rc){
            printf("Problems  %d\n", rc);
        }
    } else if (type == ZOO_DELETED_EVENT) {
        printf("Node deleted %s, now Let us watch for its creation \n", path);
        rc = zoo_wexists(zh, path, 
                watchexistence , mycontext, &st);
        if (ZOK != rc){
            printf("Problems  %d\n", rc);
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

    zoo_set_debug_level(ZOO_LOG_LEVEL_INFO);
    zoo_deterministic_conn_order(1); 
    hostPort = argv[1];

    zh = zookeeper_init(hostPort, watcher, 30000, &myid, 0, 0);
    if (!zh) {
        return errno;
    }

    while (1) {
        static struct Stat st;

        zookeeper_interest(zh, &fd, &interest, &tv);
        usleep(10);
        if (connected == 1) {
            // watch existence of the node
            usleep(10);
            rc = zoo_wexists(zh, "/testforappearance", 
                    watchexistence , mycontext, &st);
            if (ZOK != rc){
                printf("Problems  %d\n", rc);
            }
            connected++;
        }
        if (fd != -1) {
            if (interest & ZOOKEEPER_READ) {
                FD_SET(fd, &rfds);
            } else {
                FD_CLR(fd, &rfds);
            }
            if (interest & ZOOKEEPER_WRITE) {
                FD_SET(fd, &wfds);
            } else {
                FD_CLR(fd, &wfds);
            }
        } else {
            fd = 0;
        }
        FD_SET(0, &rfds);
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
    }
    return 0;
}
