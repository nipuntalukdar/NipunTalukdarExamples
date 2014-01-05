/*
 * ==================================================================================================================
 *  2014, Jan 4, 2014
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.example.eventbus;

/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class Counter {
	private String counterName = null;
	private Integer counterDelta = null;
	public Counter(String counterName, Integer counterDelta) {
		this.counterName = counterName;
		this.counterDelta = counterDelta;
	}
	public String getCounterName() {
		return counterName;
	}
	public void setCounterName(String counterName) {
		this.counterName = counterName;
	}
	public Integer getCounterDelta() {
		return counterDelta;
	}
	public void setCounterDelta(Integer counterDelta) {
		this.counterDelta = counterDelta;
	}
	@Override
	public String toString() {
		return "Counter [counterName=" + counterName + ", counterDelta="
				+ counterDelta + "]";
	}

}
