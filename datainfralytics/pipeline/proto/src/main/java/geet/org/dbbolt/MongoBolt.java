package geet.org.dbbolt;

import geet.org.data.Configs;
import geet.org.data.Person;
import geet.org.mongo.MongoService;

import java.io.Serializable;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

public class MongoBolt extends BaseRichBolt implements Serializable {
	private final static long serialVerisonUid = 18282882823335L;
	private OutputCollector collector;
	private Logger logger;

	@Override
	public void prepare(Map stormConf, TopologyContext context, OutputCollector collector) {
		logger.info("MongoBolt task started");
		this.collector = collector;
		logger = LoggerFactory.getLogger(MongoBolt.class);
		Configs.initConfig(stormConf);
	}

	@Override
	public void execute(Tuple input) {
		collector.ack(input);
		Person person = (Person) input.getValueByField("person");
		if (MongoService.getMongoService().updatePerson(person)) {
			collector.emit(input, new Values(person));
			logger.debug("Added document to db for person={}", person.getName());
			collector.ack(input);
		} else {
			logger.error("Failing message for id={}", person.getId());
			collector.fail(input);
		}
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		Fields flds = new Fields("person");
		declarer.declare(flds);
	}
}
