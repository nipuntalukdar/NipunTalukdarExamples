package cogeet.example.org;

import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Tuple;

public class SampleBoltC extends BaseRichBolt {
	private OutputCollector collector = null;
	private final static long serialVersionUID = 123444455;
	private Logger logger = null;
	private long received = 0;
	private long nextLog = 1000;

	@Override
	public void prepare(@SuppressWarnings("rawtypes") Map stormConf,
			TopologyContext context, OutputCollector collector) {
		System.out.println("SampleBoltC is prepared");
		this.collector = collector;
		logger = LoggerFactory.getLogger(SampleBoltC.class);
	}

	@Override
	public void execute(Tuple input) {
		received++;
		if (received == nextLog){
			logger.info("Rececived {} tuples", received);
			nextLog += 1000;
		}
		collector.ack(input);
		GroupingKey gk = (GroupingKey)input.getValueByField(Consts.SPOUTTWO_FIELD);
		logger.trace("Received {}", gk);
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
	}
}
