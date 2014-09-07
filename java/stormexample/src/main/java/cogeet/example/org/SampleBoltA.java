/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: SampleBoltA.java,v 1.0 Jun 12, 2014 
 *  
 * ==================================================================================================================
 */
package cogeet.example.org;

import java.util.Map;

import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Tuple;
import backtype.storm.tuple.Values;

/*
 *  @author Nipun Talukdar
 *  @version $Id: SampleBoltA.java,v 1.0 Jun 12, 2014 1:56:56 AM
 */

public class SampleBoltA extends BaseRichBolt {
	private OutputCollector collector = null;

	@Override
	public void prepare(Map stormConf, TopologyContext context,
			OutputCollector collector) {
		this.collector = collector;
		System.out.println("SampleBoltA is prepared");
	}

	@Override
	public void execute(Tuple input) {
		System.out.println("SampleBoltA received a packet "
				+ (String) input.getStringByField(Consts.SPOUT_FIELD_1) + " "
				+ (String) input.getStringByField(Consts.SPOUT_FIELD_2));
		collector
				.emit(input,
						new Values(
								" Modified by bolt A:   "
										+ (String) input
												.getStringByField(Consts.SPOUT_FIELD_1),
								" Modified this also: "
										+ (String) input
												.getStringByField(Consts.SPOUT_FIELD_2)));

	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields(Consts.BOLTA_FIELD_1, Consts.BOLTA_FIELD_2));
	}

}
