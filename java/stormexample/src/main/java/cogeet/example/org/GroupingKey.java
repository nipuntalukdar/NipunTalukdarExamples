package cogeet.example.org;

import java.nio.ByteBuffer;

public class GroupingKey {
	private int hashVal = -1;
	private String groupingKey = null;
	private final static int SEED = 4099;	
	public GroupingKey(String key) {
		groupingKey = key;
		hashVal = MurmurHash.hash32(ByteBuffer.wrap(groupingKey.getBytes()),
				0, groupingKey.getBytes().length, SEED);
	}

	public String getKey(){
		return groupingKey;
	}
	
	@Override
	public int hashCode() {
		return hashVal;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		GroupingKey other = (GroupingKey) obj;
		if (hashVal != other.hashVal)
			return false;
		if (groupingKey == null) {
			if (other.groupingKey != null)
				return false;
		} else if (!groupingKey.equals(other.groupingKey))
			return false;
		return true;
	}

	@Override
	public String toString() {
		return "GroupingKey [groupingKey=" + groupingKey + "]";
	}
}
