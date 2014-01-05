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

public class CounterGenerator {
	private EventBus bus = null;

	public CounterGenerator(boolean async) {
		if (async)
			bus = CounterAsyncEventBus.getEventBus();
		else
			bus = CounterEventBus.getEventBus();
	}

	public void publish(String name, int val) {
		bus.post(new Counter(name, val));
	}

}
