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
        document.getElementById(`country-document-primary-${name}`).value != "CUB"){
            document.getElementById(`alertNotCubaDocument-${name}`).classList.remove("hidden");
        }
        document.getElementById(`secondaryDocument-${name}`).classList.add("hidden");
        document.getElementById(`number-document-secondary-${name}`).required = '';
        document.getElementById(`expiration-document-secondary-${name}`).required = '';
    }
    else{
        document.getElementById(`alertNotCubaDocument-${name}`).classList.add("hidden");
        document.getElementById(`secondaryDocument-${name}`).classList.remove("hidden");
        document.getElementById(`number-document-secondary-${name}`).required= 'required';
        document.getElementById(`expiration-document-secondary-${name}`).required= 'required';
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
    r = validateBirthdays();
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

function validateBirthdays(){
    const date_flight = new Date(document.getElementById("date-compare-flight").innerText);
    
    var retorno = true;
    const children = document.querySelectorAll('.children-dateBirth');
    for (let i = 0; i < children.length; i++) {
        const partes = children[i].value.split('/');
        const date = new Date(partes[2], partes[0] - 1, partes[1]);
        const diff = Math.floor((date_flight.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));

        const num = children[i].id.substring('dateBirth-Children'.length);
        if (diff < 730 ){
            retorno = false;
            alert(`La eddad del niño ${num} para el momento del vuelo es menor a 2 años, por favor corrija la fecha de nacimiento.`);
        }
        else if ( diff > 4379){
            retorno = false;
            alert(`La eddad del niño ${num} para el momento del vuelo es mayor a 11 años, por favor corrija la fecha de nacimiento.`);
        }
    }

    const infant = document.querySelectorAll('.infant-dateBirth');
    for (let i = 0; i < infant.length; i++) {
        const partes = infant[i].value.split('/');
        const date = new Date(partes[2], partes[0] - 1, partes[1]);
        const diff = Math.floor((date_flight.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));

        const num = infant[i].id.substring('dateBirth-Infant'.length);
        if (diff < 730 ){
            retorno = false;
            alert(`La eddad del infante ${num} para el momento del vuelo es menor a 2 años, por favor corrija la fecha de nacimiento.`);
        }
        else if ( diff > 4379){
            retorno = false;
            alert(`La eddad del infante ${num} para el momento del vuelo es mayor a 11 años, por favor corrija la fecha de nacimiento.`);
        }
      }

    return retorno;
}
