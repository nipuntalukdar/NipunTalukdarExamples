/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: Server.java,v 1.0 Apr 9, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.hazel;

import java.util.Map;
import java.util.Queue;

import com.hazelcast.config.Config;
import com.hazelcast.core.Hazelcast;
import com.hazelcast.core.HazelcastInstance;

/*
 *  @author Nipun Talukdar
 *  @version $Id: Server.java,v 1.0 Apr 9, 2014 4:25:34 AM
 */

public class ServerStand {
	   public static void main(String[] args) {
	        Config cfg = new Config();
	        HazelcastInstance instance = Hazelcast.newHazelcastInstance(cfg);
	        Map<Integer, String> mapCustomers = instance.getMap("customers");
	        mapCustomers.put(1, "Joe");
	        mapCustomers.put(2, "Ali");
	        mapCustomers.put(3, "Avi");
	 
	        System.out.println("Customer with key 1: "+ mapCustomers.get(1));
	        System.out.println("Map Size:" + mapCustomers.size());
	 
	        Queue<String> queueCustomers = instance.getQueue("customers");
	        queueCustomers.offer("Tom");
	        queueCustomers.offer("Mary");
	        queueCustomers.offer("Jane");
	        System.out.println("First customer: " + queueCustomers.poll());
	        System.out.println("Second customer: "+ queueCustomers.peek());
	        System.out.println("Queue size: " + queueCustomers.size());
	    }

}
