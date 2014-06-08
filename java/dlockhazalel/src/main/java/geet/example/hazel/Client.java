/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: Client.java,v 1.0 Apr 10, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.hazel;

import java.util.concurrent.locks.Lock;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.client.config.ClientConfig;
import com.hazelcast.core.HazelcastInstance;

/*
 *  @author Nipun Talukdar
 *  @version $Id: Client.java,v 1.0 Apr 10, 2014 9:29:15 AM
 */

public class Client {
	public static void main(String[] args) {

		ClientConfig clientConfig = new ClientConfig();
		clientConfig.getNetworkConfig().addAddress("127.0.0.1:5701",
				"127.0.0.1:5702");
		HazelcastInstance client = null;
		Lock lock = null;
		try {
			client = HazelcastClient.newHazelcastClient(clientConfig);

			lock = client.getLock("mylock");
			lock.lock();
			Thread.sleep(2000);
			System.out.println("Unlocking");
			lock.unlock();
			System.out.println("Unlocked");
			lock = null;
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			System.out.println("I am here");
			try {
				if (lock != null)
					lock.unlock();
				if (client != null)
					client.shutdown();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}

	}
}
