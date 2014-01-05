/*
 * ==================================================================================================================
 *  2014, Jan 4, 2014
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.example.eventbus;

import java.util.concurrent.Executors;

import com.google.common.eventbus.AsyncEventBus;
import com.google.common.eventbus.EventBus;


/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class CounterAsyncEventBus{
	private static EventBus bus = new AsyncEventBus(Executors.newFixedThreadPool(1));
	
	public static EventBus getEventBus(){
		return bus;
	}
}
