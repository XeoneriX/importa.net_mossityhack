package com.boots.controller;

import com.boots.entity.User;
import com.boots.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.validation.Valid;
import java.awt.print.Pageable;
import java.io.IOException;
import java.util.List;

@Controller
public class ManufactorController {

	@Autowired
	UserRepository userRepository;

	@GetMapping("/manufactor")
	public String registration(Model model) {


		return "manufactor";
	}

	@PostMapping("/manufactor")
	public String addUser(HttpServletRequest req, HttpServletResponse resp, Pageable pageable) throws ServletException, IOException {

		return "manufactor";
	}


}
