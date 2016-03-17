package geet.org.spout;

import java.util.NoSuchElementException;
import java.util.concurrent.ConcurrentSkipListSet;
import java.util.concurrent.atomic.AtomicInteger;

public class KafkaMsgCollector {
	private ConcurrentSkipListSet<KafkaMessage> messages;
	private ConcurrentSkipListSet<KafkaMessage> currentlyProcessing;
	private AtomicInteger messagesInProcess;
	private final int maxInpRocMessage;

	public KafkaMsgCollector(int maxInProc) {
		messages = new ConcurrentSkipListSet<KafkaMessage>();
		currentlyProcessing = new ConcurrentSkipListSet<KafkaMessage>();
		messagesInProcess = new AtomicInteger(0);
		maxInpRocMessage = Math.abs(maxInProc);
	}

	public KafkaMsgCollector() {
		this(10000);
	}

	public boolean add(KafkaMessage msg) {
		if (messagesInProcess.get() >= maxInpRocMessage)
			return false;
		messages.add(msg);
		messagesInProcess.incrementAndGet();
		return true;
	}

	public boolean done(KafkaMessage msg) {
		if (currentlyProcessing.remove(msg)) {
			messagesInProcess.decrementAndGet();
			return true;
		}
		return false;
	}

	public boolean unDone(KafkaMessage msg) {
		if (currentlyProcessing.remove(msg)) {
			messages.add(msg);
			return true;
		}
		return false;
	}

	public KafkaMessage get() {
		KafkaMessage msg = null;
		try {
			msg = messages.first();
			if (messages.remove(msg)) {
				currentlyProcessing.add(msg);
			}
		} catch (NoSuchElementException e) {
		}

		return msg;
	}
}
