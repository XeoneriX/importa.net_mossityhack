<%@ page import="com.boots.repository.UserRepository" %>
<%@ page import="com.boots.entity.User" %>
<%@ page import="java.util.List" %>
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8" %>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="${contextPath}/resources/css/manufactor.css">

    <title>RegIm</title>
</head>
<body>
    <div class="navigation">
        <div class="navigation_logo">
            <a href="/home">
                <p>RegIm</p>
            </a>
        </div>
        <div class="navigation_lk">
            <div class="dropdown">
                <p>Личный кабинет</p>
                <div class="dropdown-content">
                    <a href="/login.html">Выйти</a>
                </div>
            </div>
        </div>
    </div>
    <div class="main">
        <div class="main_title">
            <p>Компания «МЕДПЛАНТ»</p>
        </div>
        <div class="main_buttons">
            <button onclick="window.location.href='/manufactor.html'" class="main_btn list active">Мои товары</button>
            <button onclick="window.location.href='/requests.html'" class="main_btn requests">Товары на рассмотрении</button>
            <button onclick="window.location.href='/add.html'" class="main_btn add">+ Добавить товар</button>
        </div>
        <div>
        <table>
            <thead>
            <th>ID</th>
            <th>UserName</th>
            <th>Password</th>
            <th>Roles</th>
            </thead>
            <c:forEach items="${allUsers}" var="user">
                <tr>
                    <td>${user.id}</td>
                    <td>${user.name}</td>
                    <td>${user.password}</td>
                    <td>
                        <c:forEach items="${user.roles}" var="role">${role.name}; </c:forEach>
                    </td>
                    <td>
                        <form action="${pageContext.request.contextPath}/admin" method="post">
                            <input type="hidden" name="userId" value="${user.id}"/>
                            <input type="hidden" name="action" value="delete"/>
                            <button type="submit">Delete</button>
                        </form>
                    </td>
                </tr>
            </c:forEach>
        </table>
            </div>
        <div class="select_page">
            <button onclick="window.location.href='/???'" class="page_btn back">Назад</button>
            <button onclick="window.location.href='/???'" class="page_btn page">1</button>
            <button onclick="window.location.href='/???'" class="page_btn page">2</button>
            <div class="dots">
                <p>. . .</p>
            </div>
            <button onclick="window.location.href='/???'" class="page_btn page">10</button>
            <button onclick="window.location.href='/???'" class="page_btn forward">Вперед</button>
        </div>
    </div>
</body>
</html>