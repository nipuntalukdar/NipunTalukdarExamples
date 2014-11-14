package cogeet.example.org;

import java.util.ArrayList;


public class Sample2 {
	private int val = -1;
	private String name = null;
	private ArrayList<String> ids  = null;
	
	public Sample2() {
	}

	public Sample2(int val, String name, ArrayList<String> ids) {
		this.val = val;
		this.name = name;
		this.ids = ids;
	}

	public int getVal() {
		return val;
	}

	public void setVal(int val) {
		this.val = val;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public ArrayList<String> getIds() {
		return ids;
	}

	public void setIds(ArrayList<String> ids) {
		this.ids = ids;
	}

	@Override
	public String toString() {
		return "Sample2 [val=" + val + ", name=" + name + ", ids=" + ids + "]";
	}
	
}
