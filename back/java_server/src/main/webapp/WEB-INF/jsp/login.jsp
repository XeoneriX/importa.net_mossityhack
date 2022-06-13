<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>
<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8"%>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=`, initial-scale=1.0">
    <link rel="stylesheet" href="${contextPath}/resources/css/registration.css">
    <title>Login RegIm</title>
</head>
<body>
<sec:authorize access="isAuthenticated()">
    <% response.sendRedirect("/registration"); %>
</sec:authorize>
<div class="login_form">
    <h1 class="login_form__title">
        Реестр<br />импортозамещения
    </h1>
    <h2 class="login_form__type">
        Вход
    </h2>
    <form action="/login" method="post">
        <div class="login_form_fields">
            <div class="login_form_fields__login">
                <input type="text" name="login" placeholder="login" required>
            </div>
            <div class="login_form_fields__password">
                <input type="password" name="password" placeholder="password" required>
            </div>
            <div class="login_form__reset-password">
                <a href="/reset_password">Восстановить пароль</a>
            </div>
            <div class="login_form_fields_buttons">
                <div class="button__sumbit">
                    <input type="submit" value="Войти">
                </div>
                <div class="button__to-registration">
                    <button onclick="window.location.href='/registration'">Регистрация</button>
                </div>
            </div>
        </div>
    </form>
</div>
</body>
</html>