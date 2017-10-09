package com.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class C {
	@Autowired
	public X a;
	
	public C(){
	}
}
