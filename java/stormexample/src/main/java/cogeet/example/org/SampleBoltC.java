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



public class SampleBoltC extends BaseRichBolt {
	private OutputCollector collector = null;
	@Override
	public void prepare(Map stormConf, TopologyContext context,
			OutputCollector collector) {
		System.out.println("SampleBoltC is prepared");
		this.collector = collector;
	}

	@Override
	public void execute(Tuple input) {
		collector.ack(input);
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
	}
}
