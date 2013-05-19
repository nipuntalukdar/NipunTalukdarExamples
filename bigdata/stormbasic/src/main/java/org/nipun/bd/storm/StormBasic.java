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

		TopologyBuilder tbuilder = new TopologyBuilder();
		tbuilder.setSpout("spout", new BasicSpout(), 1);
		tbuilder.setBolt("bolt1", new BasicBolt(), 1).shuffleGrouping("spout");
		tbuilder.setBolt("bolt2", new BasicBolt(), 1).shuffleGrouping("spout");
		Config conf = new Config();
		conf.setMaxTaskParallelism(4);
		LocalCluster lc = new LocalCluster();
		lc.submitTopology("Topology1", conf, tbuilder.createTopology());

		try {
			StormSubmitter.submitTopology("Topology1", conf,
					tbuilder.createTopology());
		} catch (AlreadyAliveException e) {
			e.printStackTrace();
		} catch (InvalidTopologyException e) {
			e.printStackTrace();
		}

		try {
			while (true)
				Thread.sleep(3000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}

	}
}
