package geet.org.indexbolt;

import geet.org.data.Person;
import geet.org.es.EsService;

import java.io.Serializable;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Tuple;

public class EsBolt extends BaseRichBolt implements Serializable{
	private final static long serialVerisonUid = 18282882823334L;
	private OutputCollector collector;
	private static final String iType = "person";
	private static final String index = "demo";
	private Logger logger;

	@Override
	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
		this.collector = collector;
		this.logger = LoggerFactory.getLogger(EsBolt.class);
		logger.info("ES bolt task started");
	}

	@Override
	public void execute(Tuple input) {
		collector.ack(input);
		Person person = (Person) input.getValueByField("person");
		if (EsService.getInstance().indexDocument(person, index, iType)){
			collector.ack(input);
			logger.info("Indexed document for id={}", person.getId());
		} else {
			logger.error("Failed to index document {}", person);
			collector.fail(input);
		}
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
	}

}
