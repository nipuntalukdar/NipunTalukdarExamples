/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: DataReducer.java,v 1.0 Sep 7, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.org;

import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;

/*
 *  @author Nipun Talukdar
 *  @version $Id: DataReducer.java,v 1.0 Sep 7, 2014 9:50:37 AM
 */

public class DataReducer extends MapReduceBase implements
		Reducer<Text, IntWritable, Text, IntWritable> {

	@Override
	public void reduce(Text key, Iterator<IntWritable> values,
			OutputCollector<Text, IntWritable> collector, Reporter reporter)
			throws IOException {
		int sum = 0;
		while (values.hasNext()){
			sum += values.next().get();
		}
		collector.collect(key, new IntWritable(sum));
	}

}
