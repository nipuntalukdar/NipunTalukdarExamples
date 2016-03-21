package geet.org.topolgy;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;
import java.util.Set;

import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.StormSubmitter;
import backtype.storm.generated.AlreadyAliveException;
import backtype.storm.generated.InvalidTopologyException;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.tuple.Fields;
import geet.org.dbbolt.MongoBolt;
import geet.org.indexbolt.EsBolt;
import geet.org.spout.DataSpout;

public class StartTopology {
	private static final String TOPOLOGY = "DemoTopolgy";

	public static void main(String[] args) {
		if (args.length < 1) {
			System.err.println("Please provide the proprty file name");
			System.exit(1);
		}
		TopologyBuilder tbuilder = new TopologyBuilder();
		tbuilder.setSpout("dataspout", new DataSpout(), 16);
		Fields groupingField = new Fields("person");
		tbuilder.setBolt("boltdb", new MongoBolt(), 16).fieldsGrouping("dataspout", groupingField);
		tbuilder.setBolt("boltindex", new EsBolt(), 32).fieldsGrouping("boltdb", groupingField);
		Config conf = new Config();
		conf.setMaxTaskParallelism(128);
		conf.setNumWorkers(2);
		conf.setNumAckers(2);
		conf.setDebug(false);
		conf.put(Config.TOPOLOGY_DEBUG, false);
		conf.setMaxSpoutPending(64);
		conf.setMessageTimeoutSecs(300);

		Properties props = new Properties();
		try {
			FileInputStream inf = new FileInputStream(args[0]);
			props.load(inf);
			Set<Object> propnames = props.keySet();
			for (Object x : propnames) {
				conf.put((String) x, props.get(x));
			}
			inf.close();
			props.list(System.out);
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(1);
		}
		try {
			StormSubmitter.submitTopology(TOPOLOGY, conf, tbuilder.createTopology());
		} catch (AlreadyAliveException | InvalidTopologyException e) {
			e.printStackTrace();
			System.exit(1);
		}
	}
}
