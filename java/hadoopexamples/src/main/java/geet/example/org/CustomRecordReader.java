package geet.example.org;

import java.io.IOException;

import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.compress.CodecPool;
import org.apache.hadoop.io.compress.CompressionCodec;
import org.apache.hadoop.io.compress.CompressionCodecFactory;
import org.apache.hadoop.io.compress.CompressionInputStream;
import org.apache.hadoop.io.compress.Decompressor;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.RecordReader;
import org.apache.hadoop.mapred.FileSplit;

public class CustomRecordReader implements RecordReader<Text, Text> {

	private CompressionCodecFactory compressionCodecs = null;
	private boolean readAll = false;
	private CompressionCodec codec;
	private Decompressor decompressor;
	private CompressionInputStream fin2 = null;
	private FSDataInputStream fileIn = null;
	private String splitPath = null;
	private long pos = 0;

	public CustomRecordReader(FileSplit split2, JobConf job) throws IOException {
		FileSplit split = (FileSplit) split2;
		final Path file = split.getPath();
		splitPath = file.getName();
		compressionCodecs = new CompressionCodecFactory(job);
		codec = compressionCodecs.getCodec(file);

		// open the file and seek to the start of the split
		FileSystem fs = file.getFileSystem(job);
		fileIn = fs.open(split.getPath());

		if (codec != null) {
			decompressor = CodecPool.getDecompressor(codec);
			fin2 = codec.createInputStream(fileIn, decompressor);
		}

	}

	@Override
	public void close() throws IOException {
		try {
			if (fin2 != null) {
				fin2.close();
			} else if (fileIn != null) {
				fileIn.close();
			}
		} finally {
			if (decompressor != null) {
				CodecPool.returnDecompressor(decompressor);
			}
		}
	}

	@Override
	public boolean next(Text key, Text value) throws IOException {
		if (readAll) {
			return false;
		}
		key.set(splitPath);
		readAll = true;
		if (fin2 != null) {
			byte[] b = new byte[8192];
			int len = 0;
			int start = 0;
			while (true && start < 8388608) {
				len = fin2.read(b, start, b.length);
				if (len < 0)
					break;
				value.append(b, start, len);
				start += len;
			}
		} else {
			byte[] b = new byte[8192];
			int len = 0;
			int start = 0;
			while (true && start < 8388608) {
				len = fileIn.read(b, 0, b.length);
				if (len < 0)
					break;
				value.append(b, start, len);
				start += len;
			}
		}
		return true;
	}

	@Override
	public Text createKey() {
		return new Text();
	}

	@Override
	public Text createValue() {
		return new Text();
	}

	@Override
	public long getPos() throws IOException {

		return pos;
	}

	@Override
	public float getProgress() throws IOException {
		return readAll ? 1.0f : 0.0f;
	}

}
