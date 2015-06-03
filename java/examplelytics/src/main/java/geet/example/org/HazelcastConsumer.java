package geet.example.org;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingDeque;
import java.util.concurrent.TimeUnit;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class HazelcastConsumer implements Runnable {
	private String queue;
	private boolean keepRunning;
	private LinkedBlockingDeque<Event> events;
	BlockingQueue<Event> hazelcastQueue;
	Logger logger;

	public HazelcastConsumer(String queue, LinkedBlockingDeque<Event> events) {
		this.queue = queue;
		keepRunning = true;
		events = new LinkedBlockingDeque<>();
		hazelcastQueue = QueClient.getClient().getQueue(queue);
		logger = LoggerFactory.getLogger(HazelcastConsumer.class);
	}

	public void stop() {
		keepRunning = false;
	}

	public String getQueue() {
		return queue;
	}

	public void setQueue(String queue) {
		this.queue = queue;
	}

	public boolean getKeepRunning() {
		return keepRunning;
	}

	public void setKeepRunning(boolean keepRunning) {
		this.keepRunning = keepRunning;
	}

	@Override
	public void run() {
		Event ev = null;
		while (keepRunning) {
			try {
				if (ev == null)
					ev = hazelcastQueue.poll(2, TimeUnit.SECONDS);
				if (ev != null) {
					if (events.offer(ev, 2, TimeUnit.SECONDS))
						ev = null;
				}
			} catch (InterruptedException e) {
				logger.error("Why interrupting? ",e);
			}
		}
	}

}
