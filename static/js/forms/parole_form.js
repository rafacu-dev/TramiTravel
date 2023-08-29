
function checkInputLengthSS() {
    var input = document.getElementById('input-n-security');
    var value = input.value.replace(/\D/g, ''); // Eliminar cualquier carácter que no sea un dígito
    var formatted = '';
    
    for (var i = 0; i < value.length; i++) {
        if (i === 3 || i === 5) {
        formatted += '-';
        }
        formatted += value[i];
    }
    formatted = formatted.slice(0, 11);
    
    input.value = formatted;
}

function checkInputLength(id,l) {
    var input = document.getElementById(id);
    if (input.value.length > l) {
        input.value = input.value.slice(0, l); 
    }
}

function showHidenDependientes(numero) {

    var divs = document.querySelectorAll('[id^="dependiente"]');        
    for (var i = 0; i < divs.length; i++) {
        if (i <= numero) {
        divs[i].classList.remove("hidden");
        } else {
        divs[i].classList.add("hidden");
        }
    }
    if (numero == "0") {
        console.log(numero)
        document.getElementById("dependientes-lbl").classList.add("hidden");
    }
    else{
        document.getElementById("dependientes-lbl").classList.remove("hidden");
    }
    const elements = document.querySelectorAll('.header-text');
    var index = 1;
    elements.forEach((element) => {
    if (!element.classList.contains('hidden')) {
        element.innerHTML = element.innerHTML.replace(element.innerHTML.split(".")[0],(index).toString());
        index += 1;
    }
    }); 

}

function showHiden(ids,show) {
    
    ids.forEach(id => {
        var element = document.getElementById(id)
        if (show) {
            element.classList.remove("hidden");
            var inputs = element.querySelectorAll('input');
            
            for (var i = 0; i < inputs.length; i++) {
                var input = inputs[i];
                if (input.hasAttribute('norequired')) {
                    input.required = false; 
                } else {
                    input.required = true;
                }
            }
        }
        else{
            element.classList.add("hidden");
            var inputs = element.querySelectorAll('input');
            
            for (var i = 0; i < inputs.length; i++) {
                var input = inputs[i];
                input.required = false;
            }
        }
    })

    const elements = document.querySelectorAll('.header-text');

    var index = 1;
    elements.forEach((element) => {
    if (!element.classList.contains('hidden')) {
        element.innerHTML = element.innerHTML.replace(element.innerHTML.split(".")[0],(index).toString());
        index += 1;
    }
    }); 
    
}

function getStates(countrie,id="") {
    const selectElement = document.getElementById(`statesSelect${id}`); 
    while (selectElement.firstChild) {
        selectElement.removeChild(selectElement.firstChild);
    }

    const option = document.createElement("option");
    option.text = "Cargando estados...";
    option.disabled = "disabled";
    option.selected = "selected";
    selectElement.appendChild(option); 
    
    const citiesSelect = document.getElementById(`citiesSelect${id}`); 
    while (citiesSelect.firstChild) {
        citiesSelect.removeChild(citiesSelect.firstChild);
    }
    const optionCity = document.createElement("option");
    optionCity.text = "Seleccione la ciudad";
    optionCity.disabled = "disabled";
    optionCity.selected = "selected";
    citiesSelect.appendChild(optionCity);  
    $.ajax({
        url: `/service/countries/states/`,
        method: 'post',
        data:{
            'countrie': countrie
        },
        dataType: 'json',
        success: function(data) {
            console.log(data);
            while (selectElement.firstChild) {
                selectElement.removeChild(selectElement.firstChild);
            }
            const option = document.createElement("option");
            option.text = "Seleccione el estado";
            option.disabled = true;
            option.selected = true;
            selectElement.appendChild(option);

            data.names.forEach(country => {
                const option = document.createElement("option");
                option.value = country;
                option.text = country;
                selectElement.appendChild(option);
            });
        },
        error: function(error) {
            console.log(error);
            while (selectElement.firstChild) {
                selectElement.removeChild(selectElement.firstChild);
            }
            const option = document.createElement("option");
            option.text = "Seleccione el estado";
            option.disabled = true;
            option.selected = true;
            selectElement.appendChild(option);
        }
    });
}

function getCities(state,id="") {
    const selectElement = document.getElementById(`citiesSelect${id}`);
    while (selectElement.firstChild) {
        selectElement.removeChild(selectElement.firstChild);
    }

    const option = document.createElement("option");
    option.text = "Cargando ciudades...";
    option.disabled = "disabled";
    option.selected = "selected";
    selectElement.appendChild(option); 

    var countrie = document.getElementById(`countrySelect${id}`).value;
    $.ajax({
        url: `/service/countries/cities/`,
        method: 'post',
        data:{
            'countrie': countrie,
            'state': state
        },
        dataType: 'json',
        success: function(data) {
            console.log(data);
            while (selectElement.firstChild) {
                selectElement.removeChild(selectElement.firstChild);
            }
            const option = document.createElement("option");
            option.text = "Seleccione la ciudad";
            option.disabled = true;
            option.selected = true;
            selectElement.appendChild(option);

            data.names.forEach(country => {
                const option = document.createElement("option");
                option.value = country;
                option.text = country;
                selectElement.appendChild(option);
            });
        },
        error: function(error) {
            console.log(error);
            while (selectElement.firstChild) {
                selectElement.removeChild(selectElement.firstChild);
            }
            const option = document.createElement("option");
            option.text = "Seleccione la ciudad";
            option.disabled = true;
            option.selected = true;
            selectElement.appendChild(option);
        }
    });
}
