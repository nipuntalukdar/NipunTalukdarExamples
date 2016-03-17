package geet.org.spout;

import geet.org.data.Person;

import java.util.HashMap;
import java.util.Map;
import java.util.TreeSet;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;

import com.google.gson.Gson;

public class DataSpout extends BaseRichSpout {

	private final static long serialVerisonUid = 18282882823334L;
	private SpoutOutputCollector collector;
	private KafkaMsgCollector msgCollector;
	private KafkaConsmer kConsumer;
	private boolean closing = false;
	private HashMap<String, KafkaMessage> messages;
	private TreeSet<KafkaMessage> failedMessages;
	private long lastFailedTried = 0L;
	private Logger logger;

	@Override
	public void open(Map conf, TopologyContext context, SpoutOutputCollector collector) {
		logger = LoggerFactory.getLogger(DataSpout.class);
		this.collector = collector;
		msgCollector = new KafkaMsgCollector();
		kConsumer = new KafkaConsmer("127.0.0.1:2181", "demogroup", 30000, 6000, msgCollector);
		messages = new HashMap<>();
		failedMessages = new TreeSet<>();
		Thread t = new Thread(kConsumer);
		t.start();
	}

	@Override
	public void close() {
		closing = true;
		kConsumer.stop();
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
		}
	}

	@Override
	public void nextTuple() {
		int msgProcessed = 0;
		boolean replay = false;
		if (!failedMessages.isEmpty()) {
			if ((System.currentTimeMillis() - 30000) > lastFailedTried) {
				lastFailedTried = System.currentTimeMillis();
			} else {
				return;
			}
		}
		while (msgProcessed < 16) {
			KafkaMessage msg = failedMessages.pollFirst();
			if (msg == null)
				msg = msgCollector.get();
			if (msg == null)
				break;
			msgProcessed++;
			Gson gson = new Gson();
			Person person = gson.fromJson(new String(msg.getData()), Person.class);
			messages.put(person.getId(), msg);
			collector.emit(new Values(person), person.getId());
		}
	}

	@Override
	public void ack(Object id) {
		String msgId = (String) id;
		KafkaMessage msg = messages.get(msgId);
		logger.debug("Successfully received ack for {}", msg);
		msgCollector.done(msg);
		messages.remove(msgId);
	}

	@Override
	public void fail(Object id) {
		// We will replay the failed message
		String msgId = (String) id;
		KafkaMessage msg = messages.get(msgId);
		failedMessages.add(msg);
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		Fields flds = new Fields("person");
		declarer.declare(flds);
	}

}
