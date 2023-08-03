function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "en";
  }

const language = getCookie("language")



function login(){
    let csrf_token = document.getElementById("csrf_token");
    let csrf = csrf_token.children[0];

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    
    document.getElementById("close-authentication-modal").classList.add("hidden");
    document.getElementById("textLogin").classList.add("hidden");
    document.getElementById("loadingLogin").classList.remove("hidden");

    $.ajax({
        url:"/login/",
        type:"post",
        data:{
            'email': email,
            'password' : password,
            "csrfmiddlewaretoken" : csrf.value
        },
        dataType:"json",
        success:function(response){
            document.getElementById("close-authentication-modal").classList.remove("hidden");
            document.getElementById("textLogin").classList.remove("hidden");
            document.getElementById("loadingLogin").classList.add("hidden");

            if(response.login == "error"){
                document.getElementById("errorDataLogin").classList.remove("hidden");
            }else{

                document.querySelector('[name=csrfmiddlewaretoken]').value = response.csrf
                document.getElementById("accountEmail").textContent = response.user

                
                if(response.redirect){
                    window.location.href = window.location.origin + response.redirect;
                }else if (response.register == "admin"){
                    document.getElementById("panel-admin").classList.remove("hidden");
                }
                document.getElementById("btnLogout").classList.remove("hidden");
                document.getElementById("btnLogin").classList.add("hidden");
                document.getElementById("btnRegisterUser").classList.remove("xl:flex");
                
                document.getElementById("close-authentication-modal").click();
                
                if(window.location.pathname === "/booking/") {
                    let btn = document.getElementById("btnContinue");
                    btn.classList.remove("hidden");
                    document.getElementById("btnLoginForContinue").classList.add("hidden");
                }
                else if(window.location.pathname === "/refills/") {
                    document.getElementById("btnRegisterRefills").classList.remove("hidden");
                    document.getElementById("btnLoginForContinue").classList.add("hidden");
                }
                
            }
        },
        error:function(response){
            document.getElementById("close-authentication-modal").classList.remove("hidden");
            document.getElementById("textLogin").classList.remove("hidden");
            document.getElementById("loadingLogin").classList.add("hidden");
        },
    });
}

function register(){
    let csrf_token = document.getElementById("csrf_token_register");
    let csrf = csrf_token.children[0];

    let email = document.getElementById("emailRegister").value;
    let password = document.getElementById("passwordRegister").value;
    let passwordConfirm = document.getElementById("passwordConfirm").value;
    let newsLetter = document.getElementById("newsLetter").checked;
    
    if(password !== passwordConfirm){
        if(language === "es"){
            document.getElementById("textErrorDataRegister").textContent = "Confirme correctamente la contraseña";
        }else{
            document.getElementById("textErrorDataRegister").textContent = "Confirm the password correctly";
        }
        document.getElementById("errorDataRegister").classList.remove("hidden");
    }
    else{
        
        document.getElementById("close-register-modal").classList.add("hidden");
        document.getElementById("textRegister").classList.add("hidden");
        document.getElementById("loadingRegister").classList.remove("hidden");
        var radios = document.getElementsByName('rool-logup');
        var rool;
        for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            rool = radios[i].value;
            break;
        }
        }

        $.ajax({
            url:"/register/",
            type:"post",
            data:{
                'rool': rool,
                'email': email,
                'password' : password,
                'newsLetter':newsLetter,
                "csrfmiddlewaretoken" : csrf.value
            },
            dataType:"json",
            success:function(response){
                document.getElementById("close-register-modal").classList.remove("hidden");
                document.getElementById("textRegister").classList.remove("hidden");
                document.getElementById("loadingRegister").classList.add("hidden");

                if(response.register == "error"){
                    if(language === "es"){
                        document.getElementById("textErrorDataRegister").textContent = "Error al realizar registro";
                    }else{
                        document.getElementById("textErrorDataRegister").textContent = "Error while registering";
                    }
                    document.getElementById("errorDataRegister").classList.remove("hidden");
                }else if(response.register == "user-exists"){
                    if(language === "es"){
                        document.getElementById("textErrorDataRegister").textContent = "El correo ya esta siendo usado";
                    }else{
                        document.getElementById("textErrorDataRegister").textContent = "The email is already registered";
                    }
                    document.getElementById("errorDataRegister").classList.remove("hidden");
                }else{
                    document.getElementById("close-register-modal").click();
                    document.getElementById("close-confirm-code-modal").setAttribute("url","/register-confirm/");
                    document.getElementById("close-confirm-code-modal").click();
                    
                }
            },
            error:function(response){
                document.getElementById("close-register-modal").classList.remove("hidden");
                document.getElementById("textRegister").classList.remove("hidden");
                document.getElementById("loadingRegister").classList.add("hidden");
            },
        });

    }
}


function confirmCode(){
    let csrf_token = document.getElementById("csrf_token_confirm_code");
    let csrf = csrf_token.children[0];

    let code = document.getElementById("confirm-code").value;
    
    document.getElementById("close-confirm-code-modal").classList.add("hidden");
    document.getElementById("textConfirmCode").classList.add("hidden");
    document.getElementById("loadingConfirmCode").classList.remove("hidden");
    let url = document.getElementById("close-confirm-code-modal").getAttribute("url");
    let email;
    if(url ==="/register-confirm/"){
        email = document.getElementById("emailRegister").value;
    }
    else{
        email = document.getElementById("emailRecreatePassword").value;
    }

    $.ajax({
        url:url,
        type:"post",
        data:{
            'email': email,
            'code' : code,
            "csrfmiddlewaretoken" : csrf.value
        },
        dataType:"json",
        success:function(response){
            document.getElementById("close-confirm-code-modal").classList.remove("hidden");
            document.getElementById("textConfirmCode").classList.remove("hidden");
            document.getElementById("loadingConfirmCode").classList.add("hidden");

            if(response.redirect){
                window.location.href = window.location.origin + response.redirect;
            }else if(response.register == "error"){
                if(language === "es"){
                    document.getElementById("textErrorDataConfirmCode").textContent = "Error al realizar registro";
                }else{
                    document.getElementById("textErrorDataConfirmCode").textContent = "Error while registering";
                }
                document.getElementById("errorDataConfirmCode").classList.remove("hidden");
            }else if(response.register == "error-code"){
                if(language === "es"){
                    document.getElementById("textErrorDataConfirmCode").textContent = "El código es incorrecto";
                }else{
                    document.getElementById("textErrorDataConfirmCode").textContent = "The code is wrong";
                }
                document.getElementById("errorDataConfirmCode").classList.remove("hidden");
            }else if(response.register == "many-failures"){
                document.getElementById("close-confirm-code-modal").click();
                if(language === "es"){
                    alert("Demasiado intentos erroneos, por favor vuelva a registrar su correo electronico.");
                }else{
                    alert("Too many wrong attempts, please re-register your email.");
                }
            }else{
                
                document.querySelector('[name=csrfmiddlewaretoken]').value = response.csrf
                document.getElementById("accountEmail").textContent = response.user
                
                if (response.success == "admin"){
                    document.getElementById("panel-admin").classList.remove("hidden");
                }
                document.getElementById("btnLogout").classList.remove("hidden");
                document.getElementById("btnLogin").classList.add("hidden");
                document.getElementById("btnRegisterUser").classList.remove("xl:flex");
                
                document.getElementById("close-confirm-code-modal").click();
                

                if(window.location.pathname === "/booking/") {
                    let btn = document.getElementById("btnContinue");
                    btn.classList.remove("hidden");
                    document.getElementById("btnLoginForContinue").classList.add("hidden");
                    //btn.click();
                }
                else if(window.location.pathname === "/refills/") {
                    document.getElementById("btnRegisterRefills").classList.remove("hidden");
                    document.getElementById("btnLoginForContinue").classList.add("hidden");
                }
                
            }
        },
        error:function(response){
            document.getElementById("close-register-modal").classList.remove("hidden");
            document.getElementById("textRegister").classList.remove("hidden");
            document.getElementById("loadingRegister").classList.add("hidden");
        },
    });
}


function recreatePassword(){
    let csrf_token = document.getElementById("csrf_token_recreate_password");
    let csrf = csrf_token.children[0];

    let email = document.getElementById("emailRecreatePassword").value;
    let password = document.getElementById("passwordRecreate").value;
    let passwordConfirm = document.getElementById("passwordRecreateConfirm").value;

    if(password !== passwordConfirm){
        if(language === "es"){
            document.getElementById("textErrorDataRecreatePassword").textContent = "Confirme correctamente la contraseña";
        }else{
            document.getElementById("textErrorDataRecreatePassword").textContent = "Confirm the password correctly";
        }
        document.getElementById("errorDataRecreatePassword").classList.remove("hidden");
    }
    else{
        document.getElementById("close-recreate-password-modal").classList.add("hidden");
        document.getElementById("textRecreatePassword").classList.add("hidden");
        document.getElementById("loadingRecreatePassword").classList.remove("hidden");

        $.ajax({
            url:"/recreate-password/",
            type:"post",
            data:{
                'email': email,
                'password' : password,
                "csrfmiddlewaretoken" : csrf.value
            },
            dataType:"json",
            success:function(response){
                document.getElementById("close-recreate-password-modal").classList.remove("hidden");
                document.getElementById("textRecreatePassword").classList.remove("hidden");
                document.getElementById("loadingRecreatePassword").classList.add("hidden");

                if(response.recreate == "error"){
                    if(language === "es"){
                        document.getElementById("textErrorDataRecreatePassword").textContent = "Error al recrear contraseña";
                    }else{
                        document.getElementById("textErrorDataRecreatePassword").textContent = "Failed to recreate password";
                    }
                    document.getElementById("errorDataRecreatePassword").classList.remove("hidden");
                }else if(response.recreate == "user-no-registered"){
                    if(language === "es"){
                        document.getElementById("textErrorDataRecreatePassword").textContent = "El correo no esta registrado";
                    }else{
                        document.getElementById("textErrorDataRecreatePassword").textContent = "The email is not registered";
                    }
                    document.getElementById("errorDataRecreatePassword").classList.remove("hidden");
                }else{
                    
                    document.getElementById("close-recreate-password-modal").click();
                    document.getElementById("close-confirm-code-modal").setAttribute("url","/recreate-confirm/");
                    document.getElementById("close-confirm-code-modal").click();
                    
                }
            },
            error:function(response){
                document.getElementById("close-recreate-password-modal").classList.remove("hidden");
                document.getElementById("textRecreatePassword").classList.remove("hidden");
                document.getElementById("loadingRecreatePassword").classList.add("hidden");
            },
        });

    }
}

function closeModal(btnClose){
    document.getElementById(btnClose).click();
}


function openClose(id){
    let element = document.getElementById(id);
    if(element.classList.contains("hidden")){
        element.classList.remove("hidden")
    }else{
        element.classList.add("hidden")
    }
}

