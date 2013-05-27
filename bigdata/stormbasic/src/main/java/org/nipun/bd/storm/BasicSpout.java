package org.nipun.bd.storm;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

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
	static final long serialVersionUID = 42L;
	TTransport tr = null;
	TProtocol proto = null;
	scribe.Client client = null;
	SystemInformation syinfo = null;

	@Override
	public void open(@SuppressWarnings("rawtypes") Map conf,
			TopologyContext context, SpoutOutputCollector collector) {
		_collector = collector;
		tr = new TFramedTransport(new TSocket("192.168.117.215", 1463));
		proto = new TBinaryProtocol(tr);
		client = new scribe.Client(proto);
		syinfo = new SystemInformation();
	}

	@Override
	public void nextTuple() {
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {	

		}
		_collector.emit(new Values("This is my value"));
		List<LogEntry> list = new ArrayList<LogEntry>();
		LogEntry log = new LogEntry();
		log.setCategory("Storm");
		String message = "Spout " + Thread.currentThread().getName() + 
				" " + syinfo.getProcessId() + " " +syinfo.getFQDN();
		log.setMessage(message);
		list.add(log);
		try {
			if (!tr.isOpen())
				tr.open();
			client.Log(list);
		} catch (org.apache.thrift.TException e) {
			e.printStackTrace();
		}
	}

	@Override
	public void declareOutputFields(OutputFieldsDeclarer declarer) {
		declarer.declare(new Fields("filepath"));
	}

	@Override
	public void ack(Object id) {
	}

	@Override
	public void fail(Object id) {
	}

}
