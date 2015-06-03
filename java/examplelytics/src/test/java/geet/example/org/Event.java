package geet.example.org;

import java.io.Serializable;

public class Event implements Serializable{

	private static final long serialVersionUID = 1234567L;
	private String data1;
	private String data2;
	
	public Event(){
		data1 = "";
		data2 = "";
	}

	public Event(String data1, String data2) {
		this.data1 = data1;
		this.data2 = data2;
	}

	public String getData1() {
		return data1;
	}

	public void setData1(String data1) {
		this.data1 = data1;
	}

	public String getData2() {
		return data2;
	}

	public void setData2(String data2) {
		this.data2 = data2;
	}

	@Override
	public String toString() {
		return "Event [data1=" + data1 + ", data2=" + data2 + "]";
	} 
}
