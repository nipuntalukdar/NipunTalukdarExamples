package geet.org.es;

import static org.elasticsearch.common.xcontent.XContentFactory.jsonBuilder;
import geet.org.data.Configs;
import geet.org.data.Person;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.TreeMap;
import java.util.concurrent.ExecutionException;

import org.elasticsearch.action.ActionFuture;
import org.elasticsearch.action.admin.indices.create.CreateIndexRequest;
import org.elasticsearch.action.admin.indices.create.CreateIndexResponse;
import org.elasticsearch.action.admin.indices.mapping.put.PutMappingRequest;
import org.elasticsearch.action.admin.indices.mapping.put.PutMappingResponse;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.Client;
import org.elasticsearch.client.transport.NoNodeAvailableException;
import org.elasticsearch.client.transport.TransportClient;
import org.elasticsearch.common.settings.Settings;
import org.elasticsearch.common.transport.InetSocketTransportAddress;
import org.elasticsearch.common.unit.TimeValue;
import org.elasticsearch.index.IndexNotFoundException;
import org.elasticsearch.indices.IndexAlreadyExistsException;
import org.elasticsearch.transport.RemoteTransportException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class EsService {
	private Client client;
	private static Object lock = new Object();
	private static EsService service;
	private Logger logger;

	public static EsService getInstance() {
		if (service != null)
			return service;
		synchronized (lock) {
			if (service == null) {
				try {
					service = new EsService();
				} catch (UnknownHostException e) {
				}
			}
		}
		return service;
	}

	private EsService() throws UnknownHostException {
		logger = LoggerFactory.getLogger(EsService.class);
		try {
			Configs cfgs = Configs.getConfigs();
			String esHost = cfgs.get("es.host");
			String esCluster = cfgs.get("es.cluster");
			int esPort = Integer.parseInt(cfgs.get("es.port"));
			Settings settings = Settings.settingsBuilder().put("cluster.name", esCluster).build();
			client = TransportClient
					.builder()
					.settings(settings)
					.build()
					.addTransportAddress(
							new InetSocketTransportAddress(InetAddress.getByName(esHost), esPort));
		} catch (UnknownHostException e) {
			throw e;
		}
	}

	public boolean indexDocument(Person person, String index, String itype) {
		try {
			TimeValue timeout = new TimeValue(2000);
			IndexResponse response = client
					.prepareIndex(index, itype, person.getId())
					.setSource(
							jsonBuilder().startObject().field("name", person.getName())
									.field("age", person.getAge()).endObject()).setTimeout(timeout)
					.get();
			return true;
		} catch (IndexNotFoundException e) {
			int retry = 0;
			while (retry < 3) {
				if (createIndex(index)) {
					break;
				}
				retry++;
			}
			if (retry == 3) {
				// Failed to create index,
				return false;
			} else {
				return indexDocument(person, index, itype);
			}
		} catch (NoNodeAvailableException e) {
			logger.error("ES Failure", e);
		} catch (IOException e) {
		}
		return false;
	}

	public boolean createIndex(String index) {
		TreeMap<String, String> settingsVals = new TreeMap<>();
		settingsVals.put("number_of_shards", "10");
		settingsVals.put("number_of_replicas", "1");
		Settings settings = Settings.builder().put(settingsVals).build();
		CreateIndexRequest request = new CreateIndexRequest(index, settings);

		ActionFuture<CreateIndexResponse> response = client.admin().indices().create(request);
		try {
			if (response.get().isAcknowledged()) {
				logger.info("Created successfully index: {}", index);
			} else {
				logger.info("Failed to create index: {}", index);
				return false;
			}
		} catch (InterruptedException | ExecutionException e) {
			if (!(e.getCause() instanceof RemoteTransportException)) {
				return false;
			}
			if (!(e.getCause().getCause() instanceof IndexAlreadyExistsException)) {
				return false;
			}
		}
		ClassLoader classLoader = getClass().getClassLoader();
		File file = new File(classLoader.getResource("mapping.json").getFile());
		BufferedReader br = null;
		String data = "";
		try {
			br = new BufferedReader(new FileReader(file));
			String temp = null;
			while (true) {
				temp = br.readLine();
				if (temp == null)
					break;
				data += temp;
			}
		} catch (FileNotFoundException e) {
			return false;
		} catch (IOException e) {
			return false;
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
				}
			}
		}
		PutMappingRequest prq = new PutMappingRequest(index);
		prq.type("demo");
		prq.source(data);
		ActionFuture<PutMappingResponse> apresp = client.admin().indices().putMapping(prq);
		PutMappingResponse prep;
		try {
			prep = apresp.get();
		} catch (InterruptedException | ExecutionException e) {
			e.printStackTrace();
			return false;
		}
		if (!prep.isAcknowledged()) {
			System.out.println("Failed");
			return false;
		}
		return true;
	}
}
