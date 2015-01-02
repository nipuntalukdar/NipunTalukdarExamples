/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: Mapper.java,v 1.0 Sep 7, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.org;

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

/*
 *  @author Nipun Talukdar
 *  @version $Id: Mapper.java,v 1.0 Sep 7, 2014 9:39:25 AM
 */

public class DataMapperRR extends MapReduceBase implements
		Mapper<Text, Text, Text, IntWritable> {
	private Text fileType = new Text();

	@Override
	public void map(Text key, Text value,
			OutputCollector<Text, IntWritable> collector, Reporter reporter)
			throws IOException {
		String data = value.toString();
		int i = 0, linecount = 0;
		boolean breakFound = false;
		while (i < data.length()) {
			if ((data.charAt(i) == '\r') || data.charAt(i) == '\n') {
				if (!breakFound) {
					linecount++;
					breakFound = true;
				}
			} else {
				breakFound = false;
			}
			i++;
		}
		data = key.toString();
		i = data.lastIndexOf(".");
		if (i != -1 && i < (data.length() - 1)) {
			collector.collect(new Text(data.substring(i + 1)), new IntWritable(
					linecount));
		} else {
			collector.collect(key, new IntWritable(linecount));
		}
	}
}
