/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: TopologyStarter.java,v 1.0 Jun 12, 2014 
 *  
 * ==================================================================================================================
 */

package cogeet.example.org;


import org.slf4j.LoggerFactory;

import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.joran.JoranConfigurator;
import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.generated.AlreadyAliveException;
import backtype.storm.generated.InvalidTopologyException;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.tuple.Fields;
import backtype.storm.utils.Utils;

/*
 *  @author Nipun Talukdar
 *  @version $Id: TopologyStarter.java,v 1.0 Jun 12, 2014 1:56:56 AM
 */

public class TopologyStarter {
	public static void main(String[] args) {
		TopologyBuilder tbuilder = new TopologyBuilder();
		JoranConfigurator jconf = new JoranConfigurator();
		LoggerContext lc = (LoggerContext)LoggerFactory.getILoggerFactory();
		lc.reset();
		jconf.setContext(lc);
		//Define the topology
		Fields groupingFields = new Fields(Consts.BOLTA_FIELD_1, Consts.BOLTA_FIELD_2);
		tbuilder.setSpout("SampleSpout", new SampleSpout(), 3);
		tbuilder.setBolt("bolta", new SampleBoltA(), 4).shuffleGrouping(
				"SampleSpout");
		tbuilder.setBolt("boltb", new SampleBoltB(), 6).fieldsGrouping("bolta", groupingFields);
		
		Config conf = new Config();
		conf.setMaxTaskParallelism(24);
		conf.setNumWorkers(2);
		conf.setNumAckers(2);
		conf.setDebug(false);
		conf.put(Config.TOPOLOGY_OPTIMIZE, false);
		conf.put(Config.TOPOLOGY_DEBUG, false);
		conf.setMessageTimeoutSecs(10);
		Config.setMaxSpoutPending(conf, 6000);
		if (args.length > 1 && args.equals("realcluster")) {
			// Submit the topology to a real cluster
			try {
				StormSubmitter.submitTopology("SampleTopology", conf,
						tbuilder.createTopology());
			} catch (AlreadyAliveException e) {
				e.printStackTrace();
				System.exit(1);
			} catch (InvalidTopologyException e) {
				e.printStackTrace();
				System.exit(1);
			}

		} else {
			// Run the topology in local mode, very useful for debugging
			try {
			LocalCluster cluster = new LocalCluster();
			cluster.submitTopology("SampleTopology", conf,
					tbuilder.createTopology());
			} catch (Exception e){
				e.printStackTrace();
			}
		}
	}
}
