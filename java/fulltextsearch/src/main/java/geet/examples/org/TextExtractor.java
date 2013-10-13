/*
 * ==================================================================================================================
 *  2013, Oct 6, 2013
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.examples.org;

import java.util.TreeMap;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.ParseContext;
import org.apache.tika.parser.Parser;
import org.apache.tika.parser.chm.ChmParser;
import org.apache.tika.parser.pdf.PDFParser;
import org.apache.tika.sax.BodyContentHandler;
import org.apache.tika.sax.ContentHandlerDecorator;
import org.xml.sax.SAXException;


/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class TextExtractor {

	private File inputFile = null;
	private boolean analyzed = false;
	private String data = null;
	private TreeMap<String, String> metaData = null;

	public TextExtractor() {
		inputFile = null;
		analyzed = false;
	}

	synchronized public File getFile() {
		return inputFile;
	}

	synchronized public void setFile(File inputFile) {
		this.inputFile = inputFile;
		analyzed = false;
	}

	public TextExtractor(File inputFile) {
		this.inputFile = inputFile;
	}

	synchronized public TreeMap<String, String> getMetaData() {
		if (inputFile == null)
			return null;
		if (analyzed == false) {
			analyze();
		}
		return metaData;
	}

	synchronized String getText() {
		if (inputFile == null)
			return null;
		if (analyzed == false) {
			analyze();
		}
		return data;
	}

	private void analyze() {
		if (!analyzed && inputFile != null) {
			data = null;
			metaData = new TreeMap<String, String>();
			boolean exceptionCaught = false;
			Parser parser = null;
			if (inputFile.getName().toLowerCase().endsWith(".chm"))
				parser = new ChmParser();
			else if (inputFile.getName().toLowerCase().endsWith(".pdf"))
				parser = new PDFParser();
			Metadata metadata = new Metadata();
			ParseContext parseContext = new ParseContext();
			FileInputStream in = null;
			try {
				in = new FileInputStream(inputFile);
				ContentHandlerDecorator handler = new BodyContentHandler(40960000);
				parser.parse(in, handler, metadata, parseContext);
				data = handler.toString();
				String[] names = metadata.names();
				for (String name : names) {
					metaData.put(name, metadata.get(name));
				}
			} catch (FileNotFoundException e) {
				e.printStackTrace();
				exceptionCaught = true;
			} catch (IOException e) {
				e.printStackTrace();
				exceptionCaught = true;
			} catch (SAXException e) {
				e.printStackTrace();
				exceptionCaught = true;
			} catch (TikaException e) {
				e.printStackTrace();
				exceptionCaught = true;
			}
			if (exceptionCaught)
				System.exit(1);
			try {
				if (in != null)
					in.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
			analyzed = true;
		}
	}

}
