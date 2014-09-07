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

/*
 *  @author Nipun Talukdar
 *  @version $Id: SampleBoltA.java,v 1.0 Jun 12, 2014 1:56:56 AM
 */


public class SampleBoltB extends BaseRichBolt {
	
	private OutputCollector collector;
	@Override
	public void prepare(Map stormConf, TopologyContext context,
			OutputCollector collector) {
		System.out.println("SampleBoltB is prepared");
		this.collector = collector;
	}

	@Override
	public void execute(Tuple input) {
		System.out.println("SampleBoltB received a packet "
				+ (String) input.getStringByField(Consts.BOLTA_FIELD_1) + " "
				+ (String) input.getStringByField(Consts.BOLTA_FIELD_2));
		collector.ack(input);
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		// No need to declare output fields if it is not emitting data.
		// But no harm in declaring them
		declarer.declare(new Fields(Consts.BOLTB_FIELD_1, Consts.BOLTB_FIELD_2));
	}

}
