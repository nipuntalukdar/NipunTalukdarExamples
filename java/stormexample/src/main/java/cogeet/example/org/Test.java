package cogeet.example.org;

import java.lang.reflect.Field;
import java.util.ArrayList;


public class Test implements Cloneable{
	private String x ;
	private int y = -100;
	private Sample z ;
	public Test(String x, int y, Sample z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}

	public String getX() {
		return x;
	}

	public void setX(String x) {
		this.x = x;
	}


	public int getY() {
		return y;
	}


	public void setY(int y) {
		this.y = y;
	}

	public Sample getZ() {
		return z;
	}

	public void setZ(Sample z) {
		this.z = z;
	}

	@Override
	public String toString() {
		return "Test [x=" + x + ", y=" + y + ", z=" + z + "]";
	}

	public static void main(String []args){
		ArrayList<String> ar = new ArrayList<String>();
		ar.add("aradata");
		Sample s = new Sample(1, "sam", ar);
		Test x = new Test("Hello", 1, s);
		System.out.println(x);
		try {
			Test y = (Test)x.clone();
			System.out.println(y);
			y.setX("Hello world");
			Test z = x;
			z.setX("hi");
			s.setName("hhhhh");
			System.out.println(x);
			System.out.println(y);
		} catch (CloneNotSupportedException e) {
			e.printStackTrace();
		}
	}

}
