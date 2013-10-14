/*
 * ==================================================================================================================
 *  2013, Oct 6, 2013
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.examples.org;

import java.io.File;
import java.util.Collection;
import java.util.TreeMap;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Set;
import java.util.concurrent.LinkedBlockingDeque;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.filefilter.DirectoryFileFilter;
import org.apache.commons.io.filefilter.SuffixFileFilter;

/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class FileSystemUtils {

	public static Collection<File> getFiles(String path, String[] suffixes) {
		SuffixFileFilter sFilter = new SuffixFileFilter(suffixes);
		Collection<File> files = FileUtils.listFiles(new File(path), sFilter,
				DirectoryFileFilter.INSTANCE);
		return files;
	}

	public static void main(String[] args) {
		if (args.length < 2)
			System.exit(1);
		try {
			Indexer indexer = new Indexer(new File(args[1]));
			IndexerPool.addIndexer(indexer);
		} catch (Exception e) {
			e.printStackTrace();
			System.exit(1);
		}
		String[] sfxes = { ".PDF", ".pdf" };
		Collection<File> files = FileSystemUtils.getFiles(args[0], sfxes);
		LinkedList<TextExtractorRunner> extractorRunners = new LinkedList<TextExtractorRunner>();
		LinkedList<Thread> threads = new LinkedList<Thread>();
		LinkedBlockingDeque<File> queue = new LinkedBlockingDeque<File>();
		int i = 0;
		while (i++ < 8) {
			extractorRunners.add(new TextExtractorRunner(new TextExtractor(),
					queue));
		}

		Iterator<TextExtractorRunner> rit = extractorRunners.iterator();
		while (rit.hasNext()) {
			Thread t = new Thread(rit.next());
			threads.add(t);
			t.start();
		}

		for (File f : files) {
			queue.offer(f);
		}
		while (true) {
			if (queue.isEmpty()) {
				break;
			}
			Utility.Sleep(100);
		}

		rit = extractorRunners.iterator();
		while (rit.hasNext()) {
			rit.next().stop();
		}

		Iterator<Thread> thIt = threads.iterator();
		while (thIt.hasNext()) {
			try {
				thIt.next().join();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		
		System.out.println("Done ....................");
	}
}
