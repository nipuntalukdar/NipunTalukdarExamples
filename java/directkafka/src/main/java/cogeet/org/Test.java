package cogeet.org;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Test {

	public static void main(String[] args) {
		Logger logger = LoggerFactory.getLogger(Test.class);
		logger.error("Hello");
		logger.info("Yes you are");
	}
}
