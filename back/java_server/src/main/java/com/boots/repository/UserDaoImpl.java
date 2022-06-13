package com.boots.repository;

import com.boots.entity.User;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;

public class UserDaoImpl {
	JdbcTemplate template;

	public void setTemplate(JdbcTemplate template) {
		this.template = template;
	}

	public List<User> getEmployeesByPage(int pageid, int total){
		String sql="select * from emp limit "+(pageid-1)+","+total;
		return template.query(sql, new RowMapper<User>(){
			public User mapRow(ResultSet rs, int row) throws SQLException {
				User e=new User();
				e.setId(rs.getLong(1));
				e.setName(rs.getString("sdfsd"));
				e.setSite(rs.getString("sdf3"));
				return e;
			}
		});
	}
}

