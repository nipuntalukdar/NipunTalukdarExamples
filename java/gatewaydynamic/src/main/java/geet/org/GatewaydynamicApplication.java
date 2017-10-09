package geet.org;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.netflix.zuul.EnableZuulProxy;

@EnableZuulProxy
@EnableDiscoveryClient
@SpringBootApplication
@EnableAutoConfiguration
public class GatewaydynamicApplication {

	public static void main(String[] args) {
		SpringApplication.run(GatewaydynamicApplication.class, args);
	}
}
