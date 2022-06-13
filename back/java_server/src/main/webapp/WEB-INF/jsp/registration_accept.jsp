<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page language="java" contentType="text/html; charset=utf-8" pageEncoding="utf-8" %>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=`, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="${contextPath}/resources/css/registration_accept.css">
    <title>Registration success RegIm</title>
</head>
<body>
    <div class="reg_access_message">
        <div class="reg_access_message__image">
            <img src="/static/success.PNG" alt="success">
        </div>
        <h1 class="reg_access_message__title">
            Заявка на регистрацию принята
        </h1>
        <h2 class="reg_access_message__subtitle">
            В ближайшее время вы получите письмо с данными учетной записи
        </h2>
        <div class="button__to-login">
            <a href="/login.html">
                <input type="button" value="Вернуться">
            </a>
        </div>
    </div>
</body>
</html>