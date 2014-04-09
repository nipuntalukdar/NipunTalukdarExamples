/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: Client.java,v 1.0 Apr 9, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.hazel;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.client.config.ClientConfig;
import com.hazelcast.core.HazelcastInstance;

/*
 *  @author Nipun Talukdar
 *  @version $Id: Client.java,v 1.0 Apr 9, 2014 5:06:05 AM
 */

public class Client {
	public static void main(String[] args) {
		ClientConfig clientConfig = new ClientConfig();
		clientConfig.addAddress("127.0.0.1:5701");
		HazelcastInstance client = HazelcastClient
				.newHazelcastClient(clientConfig);
		Lock lck = client.getLock("mylock");
		boolean gotLock = true;
		while (true) {
			gotLock = false;
			try {
				gotLock = lck.tryLock(20, TimeUnit.SECONDS);
				if (gotLock){
					System.out.println("Got Lock: " + System.currentTimeMillis());
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			if (gotLock){
				lck.unlock();
				System.out.println("Unlocked: " + System.currentTimeMillis());
			}
		}
	}
}
