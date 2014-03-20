package geet.disruptor.examples;

public class SampleEvent {
	private long value;
	
	public SampleEvent(long value) {
		this.value = value;
	}

	public long getValue() {
		return value;
	}

	public void setValue(long value) {
		this.value = value;
	}

	@Override
	public String toString() {
		return "SampleEvent [value=" + value + "]";
	}

}
