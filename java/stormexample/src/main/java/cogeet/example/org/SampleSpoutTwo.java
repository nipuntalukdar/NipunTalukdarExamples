package cogeet.example.org;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.util.Random;
import java.util.UUID;

import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;

public class SampleSpoutTwo extends BaseRichSpout {

	private SpoutOutputCollector collector = null;
	private int unacknowlegded = 0;
	private Random x = null;

	@Override
	public void open(Map conf, TopologyContext context,
			SpoutOutputCollector collector) {
		System.out.println("SpoutTwo is opened");
		this.collector = collector;
		x = new Random();
	}

	@Override
	public void nextTuple() {
		if (unacknowlegded > 20) {
			return;
		}
		String x = UUID.randomUUID().toString();
		collector.emit(new Values(new GroupingKey("hellloo-" + x)), x);
		unacknowlegded++;
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields(Consts.SPOUTTWO_FIELD));
		System.out.println("Out put fields declared");
	}

	@Override
	public void ack(Object id) {
		unacknowlegded--;
		System.out.println("Ack received for " + (String) id);
	}

	@Override
	public void fail(Object id) {
		unacknowlegded--;
		System.out.println("Failure notification received for " + (String) id);
	}
}
