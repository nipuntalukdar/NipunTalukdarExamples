package geet.org.spout;

import java.lang.Comparable;

public class KafkaMessage implements Comparable<KafkaMessage> {
	private final String topic;
	private final int partition;
	private final long offset;
	private final byte[] data;

	public KafkaMessage(String topic, int partition, long offset, byte[] msg) {
		this.topic = topic;
		this.partition = partition;
		this.offset = offset;
		data = msg;
	}

	public String getTopic() {
		return topic;
	}

	public int getPartition() {
		return partition;
	}

	public long getOffset() {
		return offset;
	}

	public byte[] getData() {
		return data;
	}

	@Override
	public String toString() {
		return "KafkaMessage [topic=" + topic + ", partition=" + partition + ", offset=" + offset
				+ ", data=" + new String(data) + "]";
	}

	@Override
	public int compareTo(KafkaMessage o) {
		if (offset != o.getOffset()) {
			if ((offset - o.getOffset()) < 0) {
				return -1;
			}
			return 1;
		}
		if (partition != o.getPartition()) {
			if ((partition - o.getPartition()) < 0) {
				return -1;
			}
			return 1;
		}
		if (!topic.equals(o.getTopic())) {
			return topic.compareTo(o.getTopic());
		}
		return 0;
	}

}
