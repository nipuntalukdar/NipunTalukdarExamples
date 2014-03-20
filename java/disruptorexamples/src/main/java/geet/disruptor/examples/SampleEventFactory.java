package geet.disruptor.examples;

import java.util.concurrent.atomic.AtomicInteger;
import com.lmax.disruptor.EventFactory;

public class SampleEventFactory implements EventFactory<SampleEvent> {

	private static AtomicInteger cur = new AtomicInteger();
	@Override
	public SampleEvent newInstance() {
		int val = cur.getAndIncrement();
		return new SampleEvent(val);
	}
}
