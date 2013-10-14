/*
 * ==================================================================================================================
 *  2013, Oct 14, 2013
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.examples.org;

import java.util.TreeSet;
import java.util.Iterator;

/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class IndexerPool {
	private static TreeSet<Indexer> allIndexes = new TreeSet<Indexer>();
	private static Object lock = new Object();
	
	public static Indexer getIndexer(){
		Indexer retIndexer = null;
		synchronized (lock) {
			if (!allIndexes.isEmpty()){
				Iterator<Indexer> indexIt = allIndexes.iterator();
				retIndexer = indexIt.next();
				allIndexes.remove(retIndexer);
			}
		}
		return retIndexer;
	}

	public static void returnIndexer(Indexer indexer){
		synchronized (lock) {
			allIndexes.add(indexer);
		}
	}
	
	public static void addIndexer(Indexer indexer){
		returnIndexer(indexer);
	}
}
