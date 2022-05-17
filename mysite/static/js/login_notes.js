let username = document.getElementById('id_username');
    password = document.getElementById('id_password');    

function removePlaceholderUsername(input_name)  {
    if (input_name.value == "Login") {
        input_name.value = "";
    }
}

function replacePlaceholderUsername(input_name)  {
    if (input_name.value == "") {
        input_name.value = "Login";
    }
}

function removePlaceholderPassword(password)  {
    if (password.value == "Password") {
        password.value = "";
        password.type = "password";
    }
}

function replacePlaceholderPassword(password)  {
    if (password.value == "") {
        password.value = "Password";
        password.type = "text";
    }
}

username.blur();
username.setAttribute('value', "Login");
username.setAttribute('onBlur', "replacePlaceholderUsername(this)");
username.setAttribute('onFocus', "removePlaceholderUsername(this)");
username.className = "login-input w-100";
password.setAttribute('value', "Password");
password.blur()
password.setAttribute('onBlur', "replacePlaceholderPassword(this)");
password.setAttribute('onFocus', "removePlaceholderPassword(this)");
password.className = "login-input w-100";
password.setAttribute('type', 'text');