function signup_verification()
{
    let name_field = document.getElementById("name");
    let email_field = document.getElementById("email");
    let password_field = document.getElementById("password");
    let confirm_password_field = document.getElementById("confirm");
    let name = name_field.value.trim()
    let email = email_field.value.trim()
    let password = password_field.value.trim()
    let confirm_password = confirm_password_field.value.trim()
    if(name != "" && email != ""  && password != ""  && confirm_password !="")
    {
        if(password === confirm_password)
        {
            if(password.length < 7)
            {
                let password_error = document.getElementById("password-error")
                password_error.innerHTML = "Please Enter Minimum 8 Digits"
                password_error.className = "mt-2 p-1 alert alert-danger text pl-3"
                password_field.className += " is-invalid"
                confirm_password_field.className += " is-invalid"
            }
            else
            {
                return true;
            }
        }
        else
        {
            password_field.className += " is-invalid"
            confirm_password_field.className += " is-invalid"
            let password_error = document.getElementById("password-error")
            password_error.innerHTML = "Password Not Match"
            password_error.className = "mt-2 p-1 alert alert-danger text pl-3"
        }
    }
    if(name == "")
    {
        name_field.value = ""
        name_field.className += " is-invalid"
    }
    if(email == "")
    {
        email_field.value = ""
        email_field.className += " is-invalid"
    }
    if(password == "")
    {
        password_field.value = ""
        password_field.className += " is-invalid"
    }
    if(confirm_password == "")
    {
        confirm_password_field.value = ""
        confirm_password_field.className += " is-invalid"
    }
    return false;
}

function login_verification()
{
    let email_field = document.getElementById("email");
    let password_field = document.getElementById("password");
    let email = email_field.value.trim()
    let password = password_field.value.trim()
    if(password != "" && email != "" && password.length>7)
    {
        return true;
    }
    if(email == "")
    {
        email_field.value = ""
        email_field.className += " is-invalid"
    }
    if(password == "" || password.length<8)
    {
        password_field.value = ""
        password_field.className += " is-invalid"
        let password_error = document.getElementById("password-error")
        password_error.innerHTML = "Please Enter a Valid Password"
        password_error.className = "mt-2 p-1 alert alert-danger text pl-3"
    }
    return false;
}

function forgot_password_verification()
{
    let email_field = document.getElementById("email");
    let email = email_field.value.trim();
    if(email != "")
    {
        return true;
    }
    email_field.value = ""
    email_field.className += " is-invalid"
    return false;
}

function update_password_verification()
{
    let password_field = document.getElementById("password");
    let confirm_password_field = document.getElementById("confirm");
    let password = password_field.value.trim()
    let confirm_password = confirm_password_field.value.trim()
    if(password != ""  && confirm_password !="")
    {
        if(password === confirm_password)
        {
            if(password.length < 7)
            {
                let password_error = document.getElementById("password-error")
                password_error.innerHTML = "Please Enter Minimum 8 Digits"
                password_error.className = "mt-2 p-1 alert alert-danger text pl-3"
                password_field.className += " is-invalid"
                confirm_password_field.className += " is-invalid"
            }
            else
            {
                return true;
            }
        }
        else
        {
            password_field.className += " is-invalid"
            confirm_password_field.className += " is-invalid"
            let password_error = document.getElementById("password-error")
            password_error.innerHTML = "Password Not Match"
            password_error.className = "mt-2 p-1 alert alert-danger text pl-3"
        }
    }
    if(password == "")
    {
        password_field.value = ""
        password_field.className += " is-invalid"
    }
    if(confirm_password == "")
    {
        confirm_password_field.value = ""
        confirm_password_field.className += " is-invalid"
    }
    return false;
}