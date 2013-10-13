/*
 * ==================================================================================================================
 *  2013, Oct 13, 2013
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.examples.org;

import java.io.File;
import java.util.TreeMap;
import java.util.Set;
import java.util.concurrent.LinkedBlockingDeque;


/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class TextExtractorRunner implements Runnable {

	public TextExtractor extractor = null;
	LinkedBlockingDeque<File> files = null;
	public boolean keepRunning = true;
	private TreeMap<String, Integer> vals = null;
	private static final Object lock = new Object();
	
	public TextExtractorRunner(TextExtractor extractor, LinkedBlockingDeque<File> files, 
			TreeMap<String, Integer> vals) {
		this.extractor = extractor;
		this.files = files;
		this.vals = vals;
	}
	
	public void stop(){
		keepRunning = false;
	}
	@Override
	public void run() {
		while (keepRunning){
			Utility.Sleep(100);
			File file = files.poll();
			if (file == null)
				continue;
			System.out.println("Got " + file.getName() + " " + Thread.currentThread().getName());
			extractor.setFile(file);
			TreeMap <String, String> metaData = extractor.getMetaData();
			Set<String> keys = metaData.keySet();
			for (String key : keys){
				synchronized (lock) {
					if (vals.containsKey(key)){
						Integer value = vals.get(key);
						value++;
						vals.put(key, value);
					} else {
						vals.put(key, new Integer(1));
					}
				}
			}
		}
	}

}
