package geet.disruptor.examples;

import com.lmax.disruptor.BatchEventProcessor;
import com.lmax.disruptor.EventPublisher;
import com.lmax.disruptor.EventTranslator;
import com.lmax.disruptor.RingBuffer;
import com.lmax.disruptor.SequenceBarrier;


public class EventPublisherCheck implements EventTranslator<SampleEvent> {

	private static final int RINGBUFFER_SIZE = 256;
	private RingBuffer<SampleEvent> sevent = null;
	private EventPublisher<SampleEvent> publisher = null;
	private SequenceBarrier sbarrier = null;

	public EventPublisherCheck() {
		sevent = new RingBuffer<SampleEvent>(new SampleEventFactory(),
				RINGBUFFER_SIZE);
		publisher = new EventPublisher<SampleEvent>(sevent);
		sbarrier = sevent.newBarrier();
		BatchEventProcessor<SampleEvent> batchproc = new BatchEventProcessor<SampleEvent>(
				sevent, sbarrier, new SampleEventHandler());
		sevent.setGatingSequences(batchproc.getSequence());
		new Thread(batchproc).start();
	}

	@Override
	public void translateTo(SampleEvent event, long sequence) {
//		System.out.println("The sequence number is " + sequence);
//		System.out.println("The event value is " + event.getValue());
		event.setValue(sequence);
	}

	void tryPublish(int howmany) {
		while (howmany > 0) {
			publisher.publishEvent(this);
			howmany--;
		}
	}

	public static void main(String[] args) {
		new EventPublisherCheck().tryPublish(100000);
		try {
			Thread.sleep(200000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
}
