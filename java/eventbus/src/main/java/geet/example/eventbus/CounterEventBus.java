/*
 * ==================================================================================================================
 *  2014, Jan 4, 2014
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.example.eventbus;

import com.google.common.eventbus.EventBus;


/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class CounterEventBus{
	private static EventBus bus = new EventBus();
	
	public static EventBus getEventBus(){
		return bus;
	}
}
