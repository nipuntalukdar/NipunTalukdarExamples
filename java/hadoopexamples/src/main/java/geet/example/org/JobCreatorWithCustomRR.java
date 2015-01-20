/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: JobCreator.java,v 1.0 Sep 7, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.org;

import java.io.IOException;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;
import org.apache.hadoop.io.Text;

/*
 *  @author Nipun Talukdar
 *  @version $Id: JobCreator.java,v 1.0 Sep 7, 2014 9:56:37 AM
 */

public class JobCreatorWithCustomRR {

	public static void main(String[] args) {
		
		JobConf conf = new JobConf(JobCreatorWithCustomRR.class);
		conf.setJobName("customrr");
		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(IntWritable.class);
		conf.setMapperClass(DataMapperRR.class);
		conf.setCombinerClass(DataReducer.class);
		conf.setReducerClass(DataReducer.class);
		conf.setInputFormat(WholeFileInputFormat.class);
		conf.setOutputFormat(TextOutputFormat.class);
		
		String inputPath = "input";
		String outputPath = "output";
		
		if (args.length > 1){
			inputPath = args[1];
		}
		if (args.length > 2){
			outputPath = args[2];
		}
		
		FileInputFormat.setInputPaths(conf, new Path(inputPath));
		FileOutputFormat.setOutputPath(conf, new Path(outputPath));
		
		try {
			JobClient.runJob(conf);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
