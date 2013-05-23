package geet.simple.accumulatelog;

import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TServer.Args;
import org.apache.thrift.server.TSimpleServer;
import org.apache.thrift.transport.TServerSocket;
import org.apache.thrift.transport.TServerTransport;
import org.apache.thrift.transport.TTransportException;


public class Server {
	public static void main(String args[]){
		if (args.length != 2){
			System.out.println("Please supply log file name and port" );
			System.exit(1);
		}
		AccumulatorHandler handler = new AccumulatorHandler(args[0]);
		AccumulateLogService.Processor<AccumulatorHandler> processor = 
				new AccumulateLogService.Processor<AccumulatorHandler>(handler);
		try {
			TServerTransport serverTransport = new TServerSocket(Integer.parseInt(args[1]));
			TServer server = new TSimpleServer(new Args(serverTransport).processor(processor));
			server.serve();
		} catch (TTransportException e) {
			System.err.println(e.getMessage());
		}
	}
}
