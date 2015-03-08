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

public class SampleSpout extends BaseRichSpout {
	private static final long serialVersionUID = 123334L;
	private SpoutOutputCollector collector = null;
	private int unacknowlegded = 0;
	private Random x = null;

	@Override
	public void open(@SuppressWarnings("rawtypes") Map conf, TopologyContext context,
			SpoutOutputCollector collector) {
		System.out.println("Spout is opened");
		this.collector = collector;
		x = new Random();
	}

	@Override
	public void nextTuple() {
		if (unacknowlegded > 20) {
			return;
		}
		HashMap<String, Object> hms = new HashMap<String, Object>();
		ArrayList<String> a = new ArrayList<String>();
		a.add("hoi");
		a.add("hhh");
		Sample2 s2 = new Sample2(x.nextInt(1000000), "sample-" + x.nextInt(10000), a);
		Sample s = new Sample(x.nextInt(999999), "sample2-" + x.nextInt(40000), a);
		hms.put("sample2", s2);
		hms.put("sample", s);
		collector.emit(new Values(hms, s2), UUID.randomUUID().toString());
		collector.emit("cstream", new Values(hms, s2), UUID.randomUUID().toString());
		unacknowlegded++;
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields(Consts.SPOUT_FIELD_1, Consts.SPOUT_FIELD_2));
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
