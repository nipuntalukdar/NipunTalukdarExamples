package org.nipun.bd.storm;
import java.util.Map;
import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;

public class BasicSpout extends BaseRichSpout {

	private SpoutOutputCollector _collector;
	static final long serialVersionUID = 42L;

	@Override
	public void open(@SuppressWarnings("rawtypes") Map conf, TopologyContext context,
			SpoutOutputCollector collector) {
		_collector = collector;
	}

	@Override
	public void nextTuple() {
		System.out.println("Emitting next tuple" + System.currentTimeMillis()/ 1000);
		try {
			Thread.sleep(5000);
		} catch (InterruptedException e) {

		}
		_collector.emit(new Values("This is my value"));
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("filepath"));
	}

	@Override
	public void ack(Object id) {
		System.out.println("ACK from spout");
	}

	@Override
	public void fail(Object id) {
		System.out.println("Failed spout");
	}

}
