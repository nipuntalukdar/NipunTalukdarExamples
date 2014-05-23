/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: GuavaCache.java,v 1.0 May 23, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.gcache;

import com.google.common.cache.CacheBuilder;
import com.google.common.cache.LoadingCache;
import com.google.common.cache.CacheLoader;
import java.util.Random;

/*
 *  @author Nipun Talukdar
 *  @version $Id: GuavaCache.java,v 1.0 May 23, 2014 10:48:43 AM
 */

public class GuavaCache {

	public static void main(String[] args) {
		LoadingCache<String, String> cache = CacheBuilder.newBuilder()
				.maximumSize(100).build(new CacheLoader<String, String>() {
					@Override
					public String load(String key) throws Exception {
						return "val-" + System.currentTimeMillis() + "-"
								+ Math.abs(new Random().nextInt());
					}
				});
		try {
			System.out.println(cache.get("hello2"));
			System.out.println(cache.get("hello2"));
			System.out.println(cache.get("hello2"));
			System.out.println(cache.get("hello3"));
			System.out.println(cache.get("hello3"));
			System.out.println(cache.get("hello3"));
		} catch (Exception e){
			e.printStackTrace();
		}
	}

}
