/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: SampleSpout.java,v 1.0 Jun 12, 2014 
 *  
 * ==================================================================================================================
 */
package cogeet.example.org;

import java.util.Map;
import java.util.UUID;
import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;
import backtype.storm.utils.Utils;
/*
 *  @author Nipun Talukdar
 *  @version $Id: SampleSpout.java,v 1.0 Jun 12, 2014 1:56:56 AM
 */


public class SampleSpout extends BaseRichSpout {

	private SpoutOutputCollector collector = null;

	@Override
	public void open(Map conf, TopologyContext context,
			SpoutOutputCollector collector) {
		System.out.println("Spout is opened");
		this.collector = collector;
	}

	@Override
	public void nextTuple() {
		System.out.println("Next tuple is called");
		Utils.sleep(1000);
		collector.emit(new Values("Hello" + System.currentTimeMillis(), "Hi"
				+ System.currentTimeMillis()), UUID.randomUUID().toString());
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields(Consts.SPOUT_FIELD_1, Consts.SPOUT_FIELD_2));
		System.out.println("Out put fields declared");
	}
	@Override 
	public void ack(Object id){
		System.out.println("Ack received for " + (String)id);
	}

	@Override 
	public void fail(Object id){
		System.out.println("Failure notification received for " + (String)id);
	}
}
