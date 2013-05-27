package geet.simple.accumulatelog;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import org.apache.thrift.TException;
import geet.simple.accumulatelog.AccumulateLogService.Iface;

public class AccumulatorHandler implements Iface {

	private File file;
	private BufferedOutputStream bio;

	public AccumulatorHandler(String filePath) {
		file = new File(filePath);
		try {
			if (file.exists()) {
				if (!file.isFile() || !file.canWrite()) {
					throw new RuntimeException(filePath + "is not writtable");
				}
			} else if (!file.createNewFile()) {
				throw new RuntimeException(filePath + " couldn't be created");
			}

		} catch (IOException e) {
			throw new RuntimeException("Cannot initialize Log Accumulator ");
		}
		try {
			bio = new BufferedOutputStream(new FileOutputStream(file));
			new Thread() {
				public void run() {
					while (true) {
						try {
							Thread.sleep(1000);
						} catch (InterruptedException e) {
						}
						synchronized (bio) {
							try {
								bio.flush();
							} catch (IOException e) {
							}
						}
					}
				}
			}.start();
		} catch (FileNotFoundException e) {
			throw new RuntimeException("Could not open output stream");
		}
	}

	@Override
	public int addLog(LogData data) throws BadOperation, TException {
		if (data.op != Operation.ADDLOG) {
			throw new BadOperation(1);
		}
		try {
			synchronized (bio) {
				System.out.println("Got " + data.logData);
				bio.write(data.logData.getBytes());
			}
		} catch (IOException e) {
			throw new BadOperation(2);
		}
		return 0;
	}

	public void stop() {
		try {
			synchronized (bio) {
				bio.flush();
				bio.close();
			}
		} catch (IOException e) {
		}
	}
}
