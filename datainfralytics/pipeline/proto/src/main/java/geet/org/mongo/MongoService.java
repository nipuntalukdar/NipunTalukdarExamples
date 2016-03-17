package geet.org.mongo;

import geet.org.data.Person;

import org.bson.Document;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.mongodb.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;

public class MongoService {

	private static MongoService MSERVICE = null;
	private static Object lock = new Object();
	private MongoClient mcl;
	private MongoDatabase mdb;
	private Logger logger;

	public static MongoService getMongoService() {
		if (MSERVICE != null)
			return MSERVICE;
		synchronized (lock) {
			if (MSERVICE == null)
				MSERVICE = new MongoService();
		}
		return MSERVICE;
	}

	private MongoService() {
		mcl = new MongoClient("localhost", 27017);
		mdb = mcl.getDatabase("analytics");
		logger = LoggerFactory.getLogger(MongoService.class);
	}

	public boolean updatePerson(Person person) {
		MongoCollection<Document> col = mdb.getCollection("person");
		try {
			col.insertOne(new Document("name", person.getName()).append("age", person.getAge())
					.append("_id", person.getId()));
		} catch (Exception e) {
			return false;
		}
		return true;
	}
}
