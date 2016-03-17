package geet.org.data;

import java.io.Serializable;

import com.google.gson.Gson;

public class Person implements Serializable{
	private static final long serialVersionUID = 123456L;
	private String name;
	private double age;
	private String id;

	public String getName() {
		return name;
	}

	public double getAge() {
		return age;
	}

	public String getId() {
		return id;
	}

	@Override
	public String toString() {
		return "Person [name=" + name + ", age=" + age + ", id=" + id + "]";
	}
	
	public Person(String id, String name, float age){
		this.id = id;
		this.name = name;
		this.age = age;
	}

	public static void main(String[] args) {
		Gson gs = new Gson();
		Person person = gs.fromJson("{\"name\": \"a\", \"age\": 100, \"id\" : \"x\"}",
				Person.class);
		System.out.println(person);
	}
}
