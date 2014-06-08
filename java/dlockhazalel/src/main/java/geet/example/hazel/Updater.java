/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: Updater.java,v 1.0 Jun 7, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.hazel;

import java.util.Collection;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;

import com.hazelcast.client.HazelcastClient;
import com.hazelcast.client.config.ClientConfig;
import com.hazelcast.core.HazelcastInstance;
import com.hazelcast.core.MultiMap;
import com.hazelcast.core.Partition;

/*
 *  @author Nipun Talukdar
 *  @version $Id: Updater.java,v 1.0 Jun 7, 2014 5:33:28 PM
 */

public class Updater implements Runnable {

	private HazelcastInstance client = null;
	private MultiMap<Object, Object> map = null;

	public Updater() {
		ClientConfig clientConfig = new ClientConfig();
		clientConfig.getNetworkConfig().addAddress("192.168.56.100:5701",
				"192.168.56.101:5701");

		client = HazelcastClient.newHazelcastClient(clientConfig);
		map = client.getMultiMap("mymulti3");
		for (Partition p2 : client.getPartitionService().getPartitions()){
			System.out.println(p2.getOwner() + "= " + p2.getPartitionId());
		}
	}

	public MultiMap<Object, Object> getMap() {
		return map;
	}

	public void stop() {
		client.shutdown();
	}

	@Override
	public void run() {
		int i = 0;
		Lock lck = null;
		while (i++ < 1000) {
			lck = client.getLock("update");
			try {
				if (lck.tryLock(10, TimeUnit.SECONDS)) {
					Collection<Object> datas = map.get("simple");

					Object[] dataobjs = datas.toArray();
					if (dataobjs.length == 0) {
						map.put("simple", new SimpleData(1));
					} else {
						SimpleData data = (SimpleData) dataobjs[0];
						map.remove("simple", data);
						data.setValue(data.getValue() + 1);
						map.put("simple", data);
					}
					lck.unlock();
				}
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}

	public static void main(String[] args) {
		Updater upd = new Updater();
		Thread t1 = new Thread(upd);
		Thread t2 = new Thread(upd);
		Thread t3 = new Thread(upd);
		Thread t4 = new Thread(upd);
		t1.start();
		t2.start();
		t3.start();
		t4.start();
		try {
			t1.join();
			t2.join();
			t3.join();
			t4.join();
		} catch (InterruptedException e) {
		}

		MultiMap<Object, Object> map = upd.getMap();
		Collection<Object> datas = map.get("simple");

		Object[] dataobjs = datas.toArray();
		SimpleData data = (SimpleData) dataobjs[0];
		System.out.println(data.getValue());

		upd.stop();

	}
}
