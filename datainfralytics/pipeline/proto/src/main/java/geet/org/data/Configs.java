package geet.org.data;

import java.util.Map;
import java.util.Properties;

public class Configs {

	private static Configs configs;
	private static final Object lock = new Object();
	private Properties props;

	private Configs(Map conf) {
		props = new Properties();
		for(Object key: conf.keySet()){
			props.put((String)key, conf.get(key));
		}
	}

	public static void initConfig(Map conf) {
		if (configs != null) 
			return;
		synchronized (lock) {
			if (configs != null)
				return;
			configs = new Configs(conf);
		}
	}
	
	public static Configs getConfigs(){
		return configs;
	}
	
	public String get(String key){
		return (String)props.get(key);
	}
}