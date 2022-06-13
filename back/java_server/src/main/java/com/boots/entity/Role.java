package com.boots.entity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.Setter;
import org.springframework.security.core.GrantedAuthority;

import javax.persistence.*;
import java.util.Set;
@Entity
@Getter
@Setter
@Table(name = "t_role")
public class Role implements GrantedAuthority {
	@Id
	private Long id;
	private String name;
	@Transient
	@ManyToMany(mappedBy = "roles")
	private Set<User> users;

	public Role(Long id, String name) {
		this.id = id;
		this.name = name;
	}
	public Role() {
	}

	public Role(Long id) {
		this.id = id;
	}
	@Override
	public String getAuthority() {
		return getName();
	}
}