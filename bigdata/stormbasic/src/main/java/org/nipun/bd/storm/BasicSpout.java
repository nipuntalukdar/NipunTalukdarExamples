package org.nipun.bd.storm;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Random;

import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TFramedTransport;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;

import backtype.storm.spout.SpoutOutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.topology.base.BaseRichSpout;
import backtype.storm.tuple.Fields;
import backtype.storm.tuple.Values;

public class BasicSpout extends BaseRichSpout {

	private SpoutOutputCollector _collector;
	private static final long serialVersionUID = 141443242L;
	private TTransport tr = null;
	private TProtocol proto = null;
	private scribe.Client client = null;
	private SystemInformation syinfo = null;
	private String name = "Spout ";
	private Random rand = null;

	public BasicSpout(String spoutName) {
		name += spoutName;
	}

	@Override
	public void open(@SuppressWarnings("rawtypes") Map conf,
			TopologyContext context, SpoutOutputCollector collector) {
		_collector = collector;
		tr = new TFramedTransport(new TSocket("192.168.117.215", 1463));
		proto = new TBinaryProtocol(tr);
		client = new scribe.Client(proto);
		syinfo = new SystemInformation();
		rand = new Random();
	}

	@Override
	public void nextTuple() {
		try {
			Thread.sleep(100);
		} catch (InterruptedException e) {
		}
		String msgId = name + System.currentTimeMillis() + "---" + rand.nextInt();
		_collector.emit(new Values(name + " sent this message msgId = " + msgId), msgId);

//		List<LogEntry> list = new ArrayList<LogEntry>();
//		LogEntry log = new LogEntry();
//		log.setCategory("Storm");
//		String message = name + Thread.currentThread().getName() + " "
//				+ syinfo.getProcessId() + " " + syinfo.getFQDN() + " " + name
//				+ " sent this message id = " + msgId;
//		log.setMessage(message);
//		list.add(log);
//		try {
//			if (!tr.isOpen())
//				tr.open();
//			client.Log(list);
//		} catch (org.apache.thrift.TException e) {
//			e.printStackTrace();
//		}
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("filepath"));
	}

	@Override
	public void ack(Object id) {
//		List<LogEntry> list = new ArrayList<LogEntry>();
//		LogEntry log = new LogEntry();
//		log.setCategory("Storm");
//		String message = (String) id;
//		log.setMessage("ACK " + message + " " + syinfo.getFQDN());
//		list.add(log);
//		try {
//			if (!tr.isOpen())
//				tr.open();
//			client.Log(list);
//		} catch (org.apache.thrift.TException e) {
//			e.printStackTrace();
//		}
	}

	@Override
	public void fail(Object id) {
		List<LogEntry> list = new ArrayList<LogEntry>();
		LogEntry log = new LogEntry();
		log.setCategory("Storm");
		String message = (String) id;
		log.setMessage("FAIL " + message + " " + syinfo.getFQDN()
		+ " CURTIME=" + System.currentTimeMillis());
		list.add(log);
		try {
			if (!tr.isOpen())
				tr.open();
			client.Log(list);
		} catch (org.apache.thrift.TException e) {
			e.printStackTrace();
		}
	}
}
