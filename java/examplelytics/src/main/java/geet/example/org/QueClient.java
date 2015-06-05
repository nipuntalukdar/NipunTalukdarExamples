package geet.example.org;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.client.config.ClientConfig;
import com.hazelcast.core.HazelcastInstance;

public class QueClient {
	private static HazelcastInstance qclient = null;
	private static Object lock = new Object();

	public static HazelcastInstance getClient() {
		if (qclient != null) {
			return qclient;
		}
		synchronized (lock) {
			if (qclient == null) {
				ClientConfig cfg = new ClientConfig();
				cfg.getNetworkConfig().addAddress("127.0.0.1:5701");
				HazelcastInstance instance = HazelcastClient.newHazelcastClient(cfg);
				qclient = instance;
			}
			return qclient;
		}
	}

}
