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
import java.util.concurrent.LinkedBlockingDeque;

import com.sun.corba.se.impl.javax.rmi.CORBA.Util;


/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class TextExtractorRunner implements Runnable {

	public TextExtractor extractor = null;
	LinkedBlockingDeque<File> files = null;
	public boolean keepRunning = true;
	
	public TextExtractorRunner(TextExtractor extractor, LinkedBlockingDeque<File> files) {
		this.extractor = extractor;
		this.files = files;
	}
	
	public void stop(){
		keepRunning = false;
	}
	
	@Override
	public void run() {
		Indexer indexer = null;
		while (keepRunning){
			Utility.Sleep(100);
			File file = files.poll();
			if (file == null)
				continue;
			System.out.println("Got " + file.getName() + " " + Thread.currentThread().getName());
			extractor.setFile(file);
			TreeMap <String, String> metaData = extractor.getMetaData();
			indexer = null;
			while (indexer == null) {
				indexer = IndexerPool.getIndexer();
				if (indexer == null)
					Utility.Sleep(50);
			}
			indexer.addToIndex(metaData, extractor.getText(), file.getAbsolutePath());
			IndexerPool.returnIndexer(indexer);
		}
	}

}
