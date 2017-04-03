package com.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;


@SpringBootApplication
@EnableDiscoveryClient
@RestController
public class ConsulregisterApplication {

	@Autowired
	private X a;
	
	@Autowired
	private C c;
	
	@Value("${tbyb}")
	private String d;
	
	@RequestMapping("/myservice")
	public String home() {
		System.out.println("My Service is called");
		return "Hello world\n";
	}

	@RequestMapping("/health")
	public String health() {
		return "hello boss";
		
	}
	
	
	
	public static void main(String[] args) {
		SpringApplication.run(ConsulregisterApplication.class, args);
		//System.out.println("Running");
	}
}
