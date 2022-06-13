package com.boots.service;

import com.boots.entity.Role;
import com.boots.entity.User;
import com.boots.repository.RoleRepository;
import com.boots.repository.UserRepository;
import com.github.javafaker.service.FakeValuesService;
import com.github.javafaker.service.RandomService;
import lombok.Value;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import java.util.Properties;

@Service
public class UserService implements UserDetailsService {

	@Autowired
	private JavaMailSender mailSender;

	private String username = "uw@dru.su";
	@PersistenceContext
	private EntityManager em;
	@Autowired
	UserRepository userRepository;
	@Autowired
	RoleRepository roleRepository;
	@Autowired
	BCryptPasswordEncoder bCryptPasswordEncoder;

	@Override
	public UserDetails loadUserByUsername(String email) throws UsernameNotFoundException {
		User user = userRepository.findByEmail(email);

		if (user == null) {
			throw new UsernameNotFoundException("User not found");
		}

		return user;
	}

	public Boolean findUserByLogin(String login, String password) {
		User userFromDb = userRepository.findByUsernameAndPassword(login, bCryptPasswordEncoder.encode(password));
		return userFromDb != null;
	}

	public List<User> allUsers() {
		return userRepository.findAll();
	}

	public boolean saveUser(User user) {
		User userFromDB = userRepository.findByEmail(user.getEmail());

		if (userFromDB != null) {
			return false;
		}
		userFromDB = new User();
		FakeValuesService fakeValuesService = new FakeValuesService(
				new Locale("en-GB"), new RandomService());

		String login = fakeValuesService.bothify("?????????");
		String password = fakeValuesService.bothify("#####");

		userFromDB.setRoles(Collections.singleton(new Role(1L, "ROLE_USER")));
		userFromDB.setUsername(login);
		userFromDB.setPassword(bCryptPasswordEncoder.encode(password));
		userFromDB.setEmail(user.getEmail());
		userFromDB.setName(user.getName());
		userFromDB.setInn(user.getInn());
		userFromDB.setSite(user.getSite());

		userRepository.save(userFromDB);
		//sendMessage(userFromDB.getEmail() , "Спасибо за регистрацию!\nlogin: " + login +"\npassword: " + password);
		return true;
	}

	public boolean deleteUser(Long userId) {
		if (userRepository.findById(userId).isPresent()) {
			userRepository.deleteById(userId);
			return true;
		}
		return false;
	}

	public List<User> usergtList(Long idMin) {
		return em.createQuery("SELECT u FROM User u WHERE u.id > :paramId", User.class)
				.setParameter("paramId", idMin).getResultList();
	}

	public void sendMessage(String to, String text) {
		SimpleMailMessage mailMessage = new SimpleMailMessage();

		mailMessage.setFrom(username);
		mailMessage.setTo(to);
		mailMessage.setSubject("importanet");
		mailMessage.setText(text);

		mailSender.send(mailMessage);
	}

}


