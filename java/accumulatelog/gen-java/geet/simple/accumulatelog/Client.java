package geet.simple.accumulatelog;

import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;

public class Client {
	int port;
	String server;
	TTransport transport;
	TProtocol protocol;
	AccumulateLogService.Client cl;

	public Client() throws Exception {
		port = 9900;
		server = "127.0.0.1";
		init();
	}

	public Client(int port, String server) throws Exception {
		this.port = port;
		this.server = server;
		init();
	}

	private void init() throws Exception {
		transport = new TSocket(server, port);
		transport.open();
		protocol = new TBinaryProtocol(transport);
		cl = new AccumulateLogService.Client(protocol);
	}

	boolean addLog(String message) {
		try {
			return 0 == cl.addLog(new LogData(Operation.ADDLOG, message));
		} catch (Exception e) {
			return false;
		}
	}
	
	public void  stop() {
		transport.close();
	}
}
