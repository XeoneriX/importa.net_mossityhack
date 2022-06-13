<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Регистрация</title>
    <link rel="stylesheet" type="text/css" href="${contextPath}/resources/css/registration.css">
</head>

<body>
<div class="reg_form">
    <h1 class="reg_form__title">
        Реестр<br />импортозамещения
    </h1>
    <h2 class="reg_form__type">
        Регистрация
    </h2>
    <form action="/registration" name="registration" method="post">
        <div class="reg_form_fields">
            <div class="row">
                <div class="reg_form_fields__element">
                    <p>Название компании</p>
                    <input type="text" name="name" placeholder="ИП Иванов" required>
                </div>
                <div class="reg_form_fields__element">
                    <p>E-Mail</p>
                    <input type="text" name="email" placeholder="blabla@yandex.ru" pattern="([A-z0-9_.-]{1,})@([A-z0-9_.-]{1,}).([A-z]{2,8})" required>
                </div>
            </div>
            <div class="row">
                <div class="reg_form_fields__element">
                    <p>ИНН</p>
                    <input type="textr" name="inn" placeholder="1234567890" required>
                </div>
                <div class="reg_form_fields__element">
                    <p>Сайт</p>
                    <input type="text" name="site" placeholder="..." required>
                </div>
            </div>

            <div class="reg_form_fields_buttons">
                <div class="button__sumbit">
                    <input type="submit" value="Регистрация">
                </div>
                <div class="button__to-login">
                    <button onclick="window.location.href='/login.html'">Вход</button>
                </div>
            </div>
        </div>
    </form>
</div>
</body>
</html>