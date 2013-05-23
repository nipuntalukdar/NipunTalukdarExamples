package geet.simple.accumulatelog;

public class SimpleClient {
	public static void main(String args[]) {
		String host = "127.0.0.1";
		int port = 9900;
		if (args.length > 0)
			host = args[0];
		if (args.length > 1)
			port = Integer.parseInt(args[1]);

		try {
			Client cl = new Client(port, host);
			cl.addLog("A message for sure\n");
			cl.addLog("Another message for sure\n");
			cl.stop();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
