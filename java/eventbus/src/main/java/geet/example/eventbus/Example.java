/*
 * ==================================================================================================================
 *  2014, Jan 4, 2014
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.example.eventbus;

import java.util.Random;

/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class Example {
	public static void main(String[] args) {
		String []counterNames = {"c1", "c2", "c3", "c4" };
		Random random = new Random();
		@SuppressWarnings("unused")
		CounterAggregator aggr = new CounterAggregator(true);
		CounterGenerator gen = new CounterGenerator(true);
		int i = 0;
		while (i++ < 10000){
			System.out.println("HI");
			gen.publish(counterNames[i & 3], random.nextInt(50000));
		}
	}
}
