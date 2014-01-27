/*
 * ==================================================================================================================
 *  2013, Oct 15, 2013
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.examples.org;

import java.io.File;
import java.io.IOException;

import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;


/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class Searcher {
	private String indexDir = null;
	IndexSearcher searcher = null;
	IndexReader reader = null;
	
	public Searcher(String indexLoc) throws IOException{
		indexDir = indexLoc;
		reader = DirectoryReader.open(FSDirectory.open(new File(indexDir)));
		searcher = new IndexSearcher(reader);
	}
	
	public void termQuery(String term){
		Term t = new Term("contentoffile", term);
		TermQuery tq = new TermQuery(t, 30);
		try {
			TopDocs docs = searcher.search(tq, 30);
			System.out.println(docs.totalHits);
			for (ScoreDoc s: docs.scoreDocs){
				System.out.println(s);
				Document doc = searcher.doc(s.doc);
				System.err.println(doc.get("filepathfile"));
			}
		} catch (IOException e) {
		}
	}
	
}
