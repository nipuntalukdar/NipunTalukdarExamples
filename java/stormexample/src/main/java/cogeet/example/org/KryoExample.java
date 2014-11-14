package cogeet.example.org;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.util.ArrayList;

import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryo.io.Input;
import com.esotericsoftware.kryo.io.Output;


public class KryoExample {

	public static void main(String[] args) {
		try {
			Kryo kr = new Kryo();
			Output output = new Output(new FileOutputStream(
					"/home/apcuser/test/kryout.bin"));
			ArrayList<String> ids = new ArrayList<String>();
			ids.add("one");
			ids.add("two");
			ids.add("three");
			Sample s = new Sample(11, "SampleOne", ids);
			kr.writeObject(output, s);
			output.close();

			Input input = new Input(new FileInputStream(
					"/home/apcuser/test/kryout.bin"));
			Sample s2 = kr.readObject(input, Sample.class);
			input.close();
			System.out.println(s2);

			Kryo kr2 = new Kryo();
			kr2.register(Sample.class, new SampleSerializer());
			kr2.register(Sample.class, new SampleSerializer());
			kr2.register(Sample2.class, new Sample2Serializer());

			ByteArrayOutputStream a = new ByteArrayOutputStream();
			Output output2 = new Output(a);
			a.flush();
			Sample2 s3 = new Sample2(100, "Sample2", ids);
			kr2.writeObject(output2, s3);
			output2.close();
			ByteArrayInputStream bin = new ByteArrayInputStream(a.toByteArray());
			Sample2 s4 = kr2.readObject(new Input(bin), Sample2.class);
			System.out.println(s4);

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
