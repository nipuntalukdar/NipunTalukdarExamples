package geet.org.spout;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import kafka.consumer.Consumer;
import kafka.consumer.ConsumerConfig;
import kafka.consumer.ConsumerIterator;
import kafka.consumer.ConsumerTimeoutException;
import kafka.consumer.KafkaStream;
import kafka.javaapi.consumer.ConsumerConnector;
import kafka.message.MessageAndMetadata;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class KafkaConsmer implements Runnable {

	private String zookeeperConnect;
	private String consumerGroup;
	private long zookeeperSesssionTimeout = 1000L;
	private long autoCommitInterval = 1000L;
	private ConsumerConfig cConfig;
	private ConsumerConnector cConsumerConnector;
	private KafkaMsgCollector msgCollector;
	private boolean keepRunning = true;
	private Logger logger;

	public KafkaConsmer(String zookeeperConnect, String consumerGroup,
			long zookeeperSesssionTimeout, long autoCommitInterval, KafkaMsgCollector collector) {
		this.zookeeperConnect = zookeeperConnect;
		this.consumerGroup = consumerGroup;
		this.zookeeperSesssionTimeout = zookeeperSesssionTimeout;
		this.autoCommitInterval = autoCommitInterval;
		this.msgCollector = collector;
		logger = LoggerFactory.getLogger(KafkaConsmer.class);
	}

	@Override
	public void run() {
		Properties props = new Properties();
		props.put("zookeeper.connect", this.zookeeperConnect);
		props.put("group.id", this.consumerGroup);
		props.put("zookeeper.session.timeout.ms", String.valueOf(this.zookeeperSesssionTimeout));
		props.put("zookeeper.sync.time.ms", "200");
		props.put("auto.commit.interval.ms", String.valueOf(this.autoCommitInterval));
		props.put("consumer.timeout.ms", "1000");
		props.put("auto.offset.reset", "smallest");

		cConfig = new ConsumerConfig(props);
		cConsumerConnector = Consumer.createJavaConsumerConnector(cConfig);
		Map<String, Integer> topicCountMap = new HashMap<String, Integer>();
		topicCountMap.put("demo", new Integer(1));
		Map<String, List<KafkaStream<byte[], byte[]>>> consumerMap = cConsumerConnector
				.createMessageStreams(topicCountMap);
		List<KafkaStream<byte[], byte[]>> streams = consumerMap.get("demo");
		KafkaStream<byte[], byte[]> stream = streams.get(0);
		ConsumerIterator<byte[], byte[]> cit = stream.iterator();
		while (keepRunning) {
			try {
				if (!cit.hasNext())
					continue;
				MessageAndMetadata<byte[], byte[]> mdata = cit.next();
				String topic = mdata.topic();
				long offset = mdata.offset();
				int partition = mdata.partition();
				while (!msgCollector
						.add(new KafkaMessage(topic, partition, offset, mdata.message()))) {
					try {
						Thread.sleep(100);
					} catch (InterruptedException e) {
					}
				}
			} catch (ConsumerTimeoutException e) {
			}
		}
	}

	public void stop() {
		keepRunning = false;
	}

	public static void main(String[] args) {
		KafkaMsgCollector collector = new KafkaMsgCollector();
		KafkaConsmer cons = new KafkaConsmer("127.0.0.1:2181", "demogroup", 30000, 2000, collector);
		KafkaMessage msg = null;
		new Thread(cons).start();
		while (true) {
			msg = collector.get();
			if (msg == null) {
				try {
					Thread.sleep(100);
				} catch (InterruptedException e) {
				}
			} else {
				System.out.println(msg);
			}
		}
	}
}
