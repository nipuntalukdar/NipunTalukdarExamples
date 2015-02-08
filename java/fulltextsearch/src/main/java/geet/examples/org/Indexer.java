/*
 * ==================================================================================================================
 *  2013, Oct 13, 2013
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.examples.org;

import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.Set;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.store.NIOFSDirectory;
import org.apache.lucene.util.Version;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.ImmutableSet;

/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class Indexer implements Comparable<Indexer>{

	private String indexDirectory = null;
	FSDirectory dir = null;
	IndexWriter writer = null;
	private static final String CONTENT_FIELD = "contentoffile";
	private static final String FILEPATH_FIELD = "filepathfile";
	
	private static final ImmutableMap<String, String> fields = new ImmutableMap.Builder<String, String>()
			.put("author", "author").put("content-type", "content-type")
			.put("cp:subject", "subject").put(" dc:subject", "subject")
			.put("dc:title", "title").put("title", "title")
			.put("meta:autho", "author").put("subject", "subject").build();

	private static final ImmutableSet<String> analyzedFields = ImmutableSet.of(
			"author", "subject", "title");

	public Indexer(File indxDirectory) throws IOException {
		indexDirectory = indxDirectory.getAbsolutePath();
		dir = new NIOFSDirectory(indxDirectory);
		writer = new IndexWriter(dir, new IndexWriterConfig(Version.LUCENE_45,
				new StandardAnalyzer(Version.LUCENE_45)));

	}

	public boolean addToIndex(Map<String, String> metaData, String content, String filePath) {
		System.out.println("Indexing " + filePath);
		Set<String> keys = metaData.keySet();
		Document doc = new Document();
		for (String key : keys) {
			if (fields.containsKey(key.toLowerCase())) {
				if (analyzedFields.contains(fields.get(key.toLowerCase()))) {
					doc.add(new TextField(fields.get(key.toLowerCase()), metaData
							.get(key), Field.Store.NO));
				} else {
					doc.add(new StringField(fields.get(key.toLowerCase()), metaData
							.get(key), Field.Store.NO));
				}
			}
		}
		
		doc.add(new TextField(FILEPATH_FIELD, filePath, Field.Store.NO));
		doc.add(new TextField(CONTENT_FIELD, content, Field.Store.NO));
		try {
			writer.addDocument(doc);
			writer.commit();
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
		return true;
	}

	public boolean deleteIndex(String content) {
		return true;
	}

	public boolean updateIndex(Map<String, String> metaData, String content) {
		return true;
	}
	


	public void cleanUp() {
		dir.close();
	}
	
	public String getIndexDirectory(){
		return indexDirectory;
	}

	@Override
	public int compareTo(Indexer o) {
		return indexDirectory.compareTo(o.getIndexDirectory());
	}
}
