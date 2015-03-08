package cogeet.example.org;

import java.util.Map;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;

public class SampleSpoutTwo extends BaseRichSpout {

	private SpoutOutputCollector collector = null;
	private int unacknowlegded = 0;
	final static long serialVersionUID = 0x1233444;
	private Logger logger = null;

	@Override
	public void open(@SuppressWarnings("rawtypes") Map conf,
			TopologyContext context, SpoutOutputCollector collector) {
		logger = LoggerFactory.getLogger(SampleSpoutTwo.class);
		logger.debug("SpoutTwo is opened");
		this.collector = collector;
	}

	@Override
	public void nextTuple() {
		if (unacknowlegded > 20) {
			return;
		}
		String x = UUID.randomUUID().toString();
		collector.emit(new Values(new GroupingKey("hellloo-" + x)), x);
		unacknowlegded++;
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
		}
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields(Consts.SPOUTTWO_FIELD));
	}

	@Override
	public void ack(Object id) {
		unacknowlegded--;
		logger.debug("Ack received for {}", (String)id);
	}

	@Override
	public void fail(Object id) {
		unacknowlegded--;
		logger.debug("Failure for {}", (String) id);
	}
}
