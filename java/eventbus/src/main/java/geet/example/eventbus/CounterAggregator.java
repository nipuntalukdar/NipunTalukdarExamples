/*
 * ==================================================================================================================
 *  2014, Jan 4, 2014
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.example.eventbus;

import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

import com.google.common.eventbus.AllowConcurrentEvents;
import com.google.common.eventbus.EventBus;
import com.google.common.eventbus.Subscribe;

/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class CounterAggregator {
	private ConcurrentHashMap<String, AtomicInteger> counters = null;
	private EventBus bus = null;

	public CounterAggregator(boolean async) {
		counters = new ConcurrentHashMap<String, AtomicInteger>();
		if (async)
			bus = CounterAsyncEventBus.getEventBus();
		else
			bus = CounterEventBus.getEventBus();
		bus.register(this);
	}

	@Subscribe
	@AllowConcurrentEvents
	public void addCount(Counter counter) {
		Integer val = counter.getCounterDelta();
		String counterName = counter.getCounterName();

		AtomicInteger oldval = counters.putIfAbsent(counterName,
				new AtomicInteger(val));
		if (oldval != null) {
			oldval.addAndGet(val);
		}
		System.out.print(Thread.currentThread().getName()
				+ " Value for the counter " + counterName + "="
				+ counters.get(counterName));

	}
}
