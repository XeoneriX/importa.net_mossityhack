package com.boots.entity;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import java.util.Set;

@Getter
@Setter
@Entity
@Table(name = "t_company")
public class Company {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;

	@Column(nullable = false)
	private String inn;

	@Column(nullable = false)
	private String egurl;

	@Column(nullable = false)
	private String site;

	@Column(name = "company_name")
	private String companyName;

	@OneToMany(mappedBy = "company", fetch = FetchType.LAZY)
	private Set<User> user;
}
