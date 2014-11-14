package cogeet.example.org;

import java.util.ArrayList;
import java.util.List;

import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryo.Serializer;
import com.esotericsoftware.kryo.io.Input;
import com.esotericsoftware.kryo.io.Output;


public class Sample2Serializer extends Serializer<Sample2> {

	@Override
	public void write(Kryo kryo, Output output, Sample2 object) {
		output.writeInt(object.getVal());
		output.writeString(object.getName());
		List<String> ids = object.getIds();
		output.writeInt(ids.size());
		for (String id : ids){
			output.writeString(id);
		}		
		System.out.println("Sample2 serialize");
	}

	@Override
	public Sample2 read(Kryo kryo, Input input, Class<Sample2> type) {
		int val = input.readInt();
		String name = input.readString();
		ArrayList<String> a = new ArrayList<String>();
		int length = input.readInt();
		int i = 0;
		while (i++ < length){
			a.add(input.readString());
		}
		System.out.println("Sample2 deserialize");
		return new Sample2(val, name, a);
	}
}
