package geet.simple.accumulatelog;

import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TNonblockingServer;
import org.apache.thrift.transport.TNonblockingServerTransport;
import org.apache.thrift.transport.TNonblockingServerSocket;

public class Server {
	public static void main(String args[]) {
		if (args.length != 2) {
			System.out.println("Please supply log file name and port");
			System.exit(1);
		}
		AccumulatorHandler handler = new AccumulatorHandler(args[0]);
		AccumulateLogService.Processor<AccumulatorHandler> processor = new AccumulateLogService.Processor<AccumulatorHandler>(
				handler);
		try {

			TNonblockingServerTransport serverTransport = new TNonblockingServerSocket(
					Integer.parseInt(args[1]));
			TServer server = new TNonblockingServer(
					new TNonblockingServer.Args(serverTransport)
							.processor(processor));
			server.serve();
		} catch (Exception e) {
			System.err.println(e.getMessage());
		}
	}
}
