package org.nipun.bd.storm;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.generated.AlreadyAliveException;
import backtype.storm.generated.InvalidTopologyException;
import backtype.storm.topology.TopologyBuilder;

/**
 * Hello world!
 * 
 */
public class StormBasic {
	public static void main(String[] args) {

		if (args.length < 1) {
			System.out.println("Please provide topology name");
			System.exit(1);
		}
		TopologyBuilder tbuilder = new TopologyBuilder();
		tbuilder.setSpout("spout1", new BasicSpout("SPOUT1 "), 1);
		tbuilder.setSpout("spout2", new BasicSpout("SPOUT2 "), 1);
		tbuilder.setSpout("spout3", new BasicSpout("SPOUT3 "), 1);
		tbuilder.setBolt("bolt1", new BasicBolt("BOLT1 "), 4).shuffleGrouping(
				"spout1");
		tbuilder.setBolt("bolt2", new BasicBolt("BOLT2 "), 4)
				.shuffleGrouping("spout1").shuffleGrouping("spout3");
		tbuilder.setBolt("bolt3", new BasicBolt("BOLT3 "), 4)
				.shuffleGrouping("spout1").shuffleGrouping("spout2");
		Config conf = new Config();
		conf.setMaxTaskParallelism(8);
		conf.setNumWorkers(4);
		conf.setNumAckers(8);
		conf.setMessageTimeoutSecs(120);

//		LocalCluster lc = new LocalCluster();
//		lc.submitTopology("Topology1", conf, tbuilder.createTopology());

		try {
			StormSubmitter.submitTopology(args[0], conf,
					tbuilder.createTopology());
		} catch (AlreadyAliveException e) {
			e.printStackTrace();
		} catch (InvalidTopologyException e) {
			e.printStackTrace();
		}

		// try {
		// while (true)
		// Thread.sleep(3000);
		// } catch (InterruptedException e) {
		// e.printStackTrace();
		// }

	}
}
