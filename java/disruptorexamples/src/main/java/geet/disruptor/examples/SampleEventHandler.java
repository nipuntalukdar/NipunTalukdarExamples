package geet.disruptor.examples;

import java.util.concurrent.atomic.AtomicInteger;
import com.lmax.disruptor.EventHandler;

public class SampleEventHandler implements EventHandler<SampleEvent> {
	private AtomicInteger called = null;

	public SampleEventHandler() {
		called = new AtomicInteger();
	}

	@Override
	public void onEvent(SampleEvent event, long sequence, boolean endOfBatch)
			throws Exception {
		System.out.println("Got event= " + event + " Sequence=" + sequence
				+ " " + endOfBatch + " called " + called.getAndIncrement());
	}
}
