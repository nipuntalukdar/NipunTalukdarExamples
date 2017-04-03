package geet.org;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.cloud.netflix.ribbon.RibbonClient;
import org.springframework.context.annotation.Bean;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@EnableDiscoveryClient
@EnableAutoConfiguration
@SpringBootApplication
@RestController
@RibbonClient(name = "registeringapp", configuration = SayHelloConfiguration.class)
public class ClientloadbalancingApplication {
	@LoadBalanced
	@Bean
	RestTemplate restTemplate() {
		return new RestTemplate();
	}

	@Autowired
	RestTemplate restTemplate;

	@RequestMapping("/health")
	public String health() {
		return "I am ok";
	}

	@RequestMapping("/url1")
	public String url() {
		String greeting = this.restTemplate.getForObject("http://registeringapp/myservice", String.class);
	    return String.format("%s", greeting);
	}

	public static void main(String[] args) {
		SpringApplication.run(ClientloadbalancingApplication.class, args);
	}
}
