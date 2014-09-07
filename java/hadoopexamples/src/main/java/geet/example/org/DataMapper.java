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
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

/*
 *  @author Nipun Talukdar
 *  @version $Id: Mapper.java,v 1.0 Sep 7, 2014 9:39:25 AM
 */

public class DataMapper extends MapReduceBase implements Mapper<LongWritable , Text,Text, IntWritable> {
	private final static IntWritable one = new IntWritable(1);
	private Text word = new Text();
	@Override
	public void map(LongWritable key, Text value,
			OutputCollector<Text, IntWritable> collector, Reporter reporter)
			throws IOException {
		String line = value.toString();
		StringTokenizer tokener = new StringTokenizer(line);
		while (tokener.hasMoreTokens()){
			word.set(tokener.nextToken());
			collector.collect(word, one);
		}
	}
}
