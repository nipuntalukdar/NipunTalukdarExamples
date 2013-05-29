package org.nipun.bd.storm;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TFramedTransport;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.hyperic.sigar.cmd.SysInfo;

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
	private OutputCollector _collector;
	private TTransport tr = null;
	private TProtocol proto = null;
	private scribe.Client client = null;
	private SystemInformation syinfo = null;
	private String name = "Bolt ";

	public BasicBolt(String boltname) {
		name += boltname;
	}

	@Override
	public void prepare(@SuppressWarnings("rawtypes") Map stormConf,
			TopologyContext context, OutputCollector collector) {
		_collector = collector;
		System.out.println("Prepared");
		tr = new TFramedTransport(new TSocket("192.168.117.215", 1463));
		proto = new TBinaryProtocol(tr);
		client = new scribe.Client(proto);
		syinfo = new SystemInformation();
	}

	@Override
	public void execute(Tuple input) {
//		String path = (String) input.getValueByField("filepath");
//		// _collector.emit(new Values(path, "CalculatedMD5"));
//		List<LogEntry> list = new ArrayList<LogEntry>();
//		LogEntry log = new LogEntry();
//		log.setCategory("Storm");
//		String message = name + Thread.currentThread().getName() + " "
//				+ syinfo.getProcessId() + " " + syinfo.getFQDN() + " "
//				+ System.currentTimeMillis();
//		log.setMessage(message + " " + path);
//		list.add(log);
//		try {
//			if (!tr.isOpen())
//				tr.open();
//			client.Log(list);
//		} catch (org.apache.thrift.TException e) {
//			e.printStackTrace();
//		}
		_collector.ack(input);
	}

	@Override
	public void cleanup() {
		System.out.println("Doing clean up");
		if (tr.isOpen())
			tr.close();
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
