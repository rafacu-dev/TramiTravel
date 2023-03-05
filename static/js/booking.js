function selectCodeCity(num){
    document.getElementById("codePhoneNumber").textContent = num;
    document.getElementById("codePhoneNumberInput").value = num;
}

function selectCountry(v,name){
    document.getElementById(`countryFor-${name}`).textContent = v;
    document.getElementById(`country-${name}`).value = v;

    if(v ==="Cuba"){
        document.getElementById(`CubaDocuments-${name}`).classList.remove("hidden")
        document.getElementById(`textDocumentInformation-${name}`).textContent = "Foreign document information";

        document.getElementById(`checkboxCubaDocuments-${name}`).checked = false;
        document.getElementById(`alertNotCubaDocument-${name}`).classList.add("hidden")
        document.getElementById(`inputsCubaDocument-${name}`).classList.remove("hidden")
    }
    else{
        document.getElementById(`CubaDocuments-${name}`).classList.add("hidden")
        document.getElementById(`textDocumentInformation-${name}`).textContent = "Document information";
    }
}

function notAvailableSecondaryDocument(v,name){
    if(v.checked){
        if(document.getElementById("rute-flight").textContent.includes("Cuba") &&
        document.getElementById(`primaryCountryDocument-${name}`).value != "CU"){
            document.getElementById(`alertNotCubaDocument-${name}`).classList.remove("hidden");
        }
        document.getElementById(`secondaryDocument-${name}`).classList.add("hidden");
        document.getElementById(`secondaryDocumentNumber-${name}`).required = '';
        document.getElementById(`secondaryExpirationDocument-${name}`).required = '';
    }
    else{
        document.getElementById(`alertNotCubaDocument-${name}`).classList.add("hidden");
        document.getElementById(`secondaryDocument-${name}`).classList.remove("hidden");
        document.getElementById(`secondaryDocumentNumber-${name}`).required= 'required';
        document.getElementById(`secondaryExpirationDocument-${name}`).required= 'required';
    }
}

function setCities(cities=String,id){
    let listCities = cities.toString().replace("dict_values([['","").replace("']])","").split("', '");
    const select = document.getElementById(id);
    
    for (let i = select.options.length; i >= 0; i--) {
        select.remove(i);
    }

    listCities.forEach(city => {        
        const option = document.createElement('option');
        option.text = city;
        select.appendChild(option);
    })
}
function validator(){
    let emailContact = document.getElementById("emailContact").value;
    let confirmEmail = document.getElementById("confirmEmail").value;
    let errorMsgValidatePhone = document.querySelector("#errorMsgValidatePhone");

    var r = true;
    if ( emailContact != confirmEmail){
        r = false;
        document.getElementById("errorMsgConfirmEmail").innerHTML = "The email confirmation is not correct!";
    }
    else if(errorMsgValidatePhone.innerHTML !== "valid-phone"){
        errorMsgValidatePhone.classList.remove("hidden");        
        r = false;
    }
    else{
        document.getElementById("codePhoneNumberInput").value = document.getElementByClassName("iti__country iti__preferred iti__active").getAttribute("data-dial-code");
    }
    return r;
    
}
