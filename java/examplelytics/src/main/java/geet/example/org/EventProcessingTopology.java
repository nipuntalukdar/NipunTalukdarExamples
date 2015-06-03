package geet.example.org;

import org.slf4j.LoggerFactory;

import ch.qos.logback.classic.LoggerContext;
import ch.qos.logback.classic.joran.JoranConfigurator;
import ch.qos.logback.core.joran.spi.JoranException;

public class EventProcessingTopology {
	public static void main(String[] args) {
		System.setProperty("logfile.name", "eventlytics.log");
		String log4jConfigFile = System.getProperty("storm.home") + "/logback/cluster.xml";
		LoggerContext context = (LoggerContext) LoggerFactory.getILoggerFactory();
		JoranConfigurator configurator = new JoranConfigurator();
		configurator.setContext(context);
		try {
			context.reset();
			configurator.doConfigure(log4jConfigFile);
		} catch (JoranException e) {
			e.printStackTrace();
		}
	}
}
