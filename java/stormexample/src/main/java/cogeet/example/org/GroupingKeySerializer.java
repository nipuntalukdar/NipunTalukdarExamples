
package cogeet.example.org;

import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryo.Serializer;
import com.esotericsoftware.kryo.io.Input;
import com.esotericsoftware.kryo.io.Output;


public class GroupingKeySerializer extends Serializer<GroupingKey>{

	@Override
	public void write(Kryo kryo, Output output, GroupingKey object) {
		output.writeString(object.getKey());
	}

	@Override
	public GroupingKey read(Kryo kryo, Input input, Class<GroupingKey> type) {
		String key = input.readString();
		return new GroupingKey(key);
	}
}
