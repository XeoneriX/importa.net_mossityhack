package com.boots.config;

import lombok.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.JavaMailSenderImpl;

import java.util.Properties;

@Configuration
public class MailConfig {

	private String host = "smtp.yandex.ru";
	private String username = "mchimportanet";
	private String password= "Mqaj3VkX8JhY8de";
	private int port =456;
	private String protocol = "smtps";
	private String debug="true";

	@Bean
	public JavaMailSender getMailSender() {
		JavaMailSenderImpl mailSender = new JavaMailSenderImpl();

		mailSender.setHost(host);
		mailSender.setPort(port);
		mailSender.setUsername(username);
		mailSender.setPassword(password);

		Properties properties = mailSender.getJavaMailProperties();

		properties.setProperty("mail.transport.protocol", protocol);
		properties.setProperty("mail.debug", debug);

		return mailSender;
	}
}