package geet.example.org;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.client.config.ClientConfig;
import com.hazelcast.core.HazelcastInstance;

public class HazelcastClienTest {
	
	public static void main(String []args){
		ClientConfig cfg = new ClientConfig();
		cfg.getNetworkConfig().addAddress("127.0.0.1:5701");
		HazelcastInstance client = HazelcastClient.newHazelcastClient(cfg);
		BlockingQueue<Event> queue = client.getQueue("myQueue");
		try {
			queue.offer(new Event("hello3", "hi" ), 60, TimeUnit.SECONDS);
			queue.offer(new Event("hello4", "hi2" ), 60, TimeUnit.SECONDS);
			Event ev = queue.poll();
			if (ev != null){
				System.out.println(ev);
			}
			ev = queue.poll();
			if (ev != null){
				System.out.println(ev);
			}
		} catch (InterruptedException e) {
		}
		
	}
}
