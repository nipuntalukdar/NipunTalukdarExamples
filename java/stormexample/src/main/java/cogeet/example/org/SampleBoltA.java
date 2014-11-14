package cogeet.example.org;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;
import java.util.Random;

import clojure.lang.Cons;



public class SampleBoltA extends BaseRichBolt {
	private OutputCollector collector = null;
	@Override
	public void prepare(Map stormConf, TopologyContext context,
			OutputCollector collector) {
		System.out.println("SampleBoltA is prepared");
		this.collector = collector;
	}

	@Override
	public void execute(Tuple input) {
		String name = String.format("Sample string %d", new Random().nextInt());
		HashMap<String, Object> hms = (HashMap<String, Object> )input.getValueByField(Consts.SPOUT_FIELD_1);
		ArrayList<String> ids = new ArrayList<String>();
		for (String s : hms.keySet()){
			if (hms.get(s) instanceof Sample)
				System.out.println(s + (Sample)hms.get(s));
			else if (hms.get(s) instanceof Sample2)
				System.out.println(s + (Sample2)hms.get(s));
		}
		ids.add(name);
		ids.add(name);
		Sample a = new Sample(new Random().nextInt(), name, ids);
		Sample2 b = new Sample2(new Random().nextInt(), name, ids);
		collector.emit(input, new Values(a, b));
		collector.ack(input);
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields(Consts.BOLTA_FIELD_1, Consts.BOLTA_FIELD_2));
	}
}
