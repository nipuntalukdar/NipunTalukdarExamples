package geet.example.org;

import java.io.IOException;

import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileSplit;
import org.apache.hadoop.mapred.InputSplit;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.RecordReader;
import org.apache.hadoop.mapred.Reporter;

public class WholeFileInputFormat extends FileInputFormat<Text, Text> {

	@Override
	public RecordReader<Text, Text> getRecordReader(InputSplit split,
			JobConf job, Reporter reporter) throws IOException {
		return new CustomRecordReader((FileSplit)split, job);
	}
	
	@Override
	protected boolean isSplitable(FileSystem fs, Path filename){
		return false;
	}

}
