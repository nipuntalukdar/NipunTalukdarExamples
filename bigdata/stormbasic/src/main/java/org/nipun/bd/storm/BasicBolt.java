package org.nipun.bd.storm;

import java.util.Map;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.IRichBolt;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

public class BasicBolt implements IRichBolt {
	/**
	 * 
	 */
	private static final long serialVersionUID = 23788898L;
	OutputCollector _collector ;

	@Override
	public void prepare(@SuppressWarnings("rawtypes") Map stormConf, TopologyContext context,
			OutputCollector collector) {
		_collector = collector;
		System.out.println("Prepared");
	}

	@Override
	public void execute(Tuple input) {
		String  path = (String)input.getValueByField("filepath");
		System.out.println("Recieved " + path  + " " +  System.currentTimeMillis()/ 1000);
		_collector.emit(new Values(path,  "CalculatedMD5"));
	}

	@Override
	public void cleanup() {
		System.out.println("Doing clean up");

	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("filepath", "filemd5"));
	}

	@Override
	public Map<String, Object> getComponentConfiguration() {
		return null;
	}

}
