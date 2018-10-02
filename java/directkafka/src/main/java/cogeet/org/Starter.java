package cogeet.org;

import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.function.FlatMapFunction;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.streaming.Duration;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaInputDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.kafka010.ConsumerStrategies;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Starter {

	private static final Logger logger = LoggerFactory.getLogger(Starter.class);

	private static final void createStreams(Map<String, Object> kafkaParams, SparkConf conf, Collection<String> topics,
			JavaStreamingContext sc) {

		JavaInputDStream<ConsumerRecord<String, String>> stream = KafkaUtils.createDirectStream(sc,
				LocationStrategies.PreferConsistent(),
				ConsumerStrategies.<String, String>Subscribe(topics, kafkaParams));

		JavaDStream<String> str1 = stream.map(new Function<ConsumerRecord<String, String>, String>() {

			private static final long serialVersionUID = 2L;

			@Override
			public String call(ConsumerRecord<String, String> v1) throws Exception {
				return v1.value();
			}
		});
		JavaDStream<String> str2 = str1.flatMap(new FlatMapFunction<String, String>() {

			private static final long serialVersionUID = 1L;

			@Override
			public Iterator<String> call(String t) throws Exception {
				Thread.sleep(30000);
				logger.info("Hello {}", t);
				return Arrays.asList(t.split(" ")).iterator();
			}
		});

		logger.info("Count is {}", str2.count());
		str2.print();
	}

	public static void main(String[] args) {
		String consumerGroup = "myconsumergroup";
		String appName = "myappname";
		if (args.length >= 1) {
			consumerGroup = args[0];
		}
		if (args.length >= 2) {
			appName = args[1];
		}

		Map<String, Object> kafkaParams = new HashMap<>();
		kafkaParams.put("bootstrap.servers", "localhost:9092");
		kafkaParams.put("key.deserializer", StringDeserializer.class);
		kafkaParams.put("value.deserializer", StringDeserializer.class);
		kafkaParams.put("group.id", consumerGroup);
		kafkaParams.put("fetch.max.bytes", "10240");
		kafkaParams.put("auto.offset.reset", "earliest");
		kafkaParams.put("partition.assignment.strategy", "org.apache.kafka.clients.consumer.RangeAssignor");
		kafkaParams.put("enable.auto.commit", true);
		SparkConf sconf = new SparkConf().setAppName(appName).setMaster("spark://localhost:7077");
		sconf.set("spark.streaming.kafka.maxRatePerPartition", "10");
		JavaStreamingContext sc = new JavaStreamingContext(sconf, new Duration(10000));

		Collection<String> topics = Arrays.asList("streaming");
		createStreams(kafkaParams, sconf, topics, sc);
		sc.start();
		try {
			sc.awaitTermination();
		} catch (Exception e) {
			logger.error("Hello", e);
		}
	}
}
