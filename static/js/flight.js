function controlDateReturn(v){
    if(v === 'rt'){
        document.getElementById("date_return").disabled = false
    }else{
        document.getElementById("date_return").disabled = true
        document.getElementById("date_return").value = ""
    }

}

function upPassenger(label){
    let lbl = document.getElementById(`${label}Label`);
    let actualValue = parseInt(lbl.textContent);
    if( actualValue < 10){
        lbl.textContent = actualValue + 1;
        let input = document.getElementById(label);
        input.value = actualValue + 1;
        
        let textDropdownPassenger = document.getElementById("textDropdownPassenger");
        let count = parseInt(textDropdownPassenger.textContent)
        textDropdownPassenger.textContent = count + 1;
    }

}

function downPassenger(label){
    let lbl = document.getElementById(`${label}Label`);
    let actualValue = parseInt(lbl.textContent);
    if( actualValue > 1){
        lbl.textContent = actualValue - 1;
        let input = document.getElementById(label);
        input.value = actualValue - 1;

        let textDropdownPassenger = document.getElementById("textDropdownPassenger");
        let count = parseInt(textDropdownPassenger.textContent)
        textDropdownPassenger.textContent = count - 1;
    }
    else if( label !== "adults" && actualValue > 0){
        lbl.textContent = actualValue - 1;
        let input = document.getElementById(label);
        input.value = actualValue - 1;
        
        let textDropdownPassenger = document.getElementById("textDropdownPassenger");
        let count = parseInt(textDropdownPassenger.textContent)
        textDropdownPassenger.textContent = count - 1;
    }

}

function submitForm(){
    let flightBeginSelect = $('input:radio[name=flightBeginSelect]:checked');
    let flightReturnSelect = $('input:radio[name=flightReturnSelect]:checked');

    var txt0 = "Debe seleccionar una de las fechas con disponibilidad de vuelos.";
    var txt1 = "Debe seleccionar el vuelo de ida para continuar.";
    var txt2 = "Debe seleccionar el vuelo de retorno para continuar.";
    var txt3 = "Debe seleccionar vuelos que pertenescan a la misma agencia.";
    if(language === "en"){
        txt0 = "You must select one of the dates with flight availability.";
        txt1 = "You must select the date for the outbound flight.";
        txt2 = "You must select the return flight to continue.";
        txt3 = "You must select flights that belong to the same agency.";
    }
    console.log(document.getElementById("available_dates").classList)
    if(!document.getElementById("available_dates").classList.contains("hidden")){
        document.getElementById("btn-messagge-modal").click();
        document.getElementById("content-messagge").innerHTML = `        
        <p class="text-gray-700 font-light text-md w-full mb-2 font-serif">${txt0}</p>
        <img src="/static/images/select_flight_date.png" class="w-full h-auto border mb-6" alt="...">
        `;
    }
    else if ( flightBeginSelect.length === 0 ) {
        document.getElementById("btn-messagge-modal").click();
        document.getElementById("content-messagge").innerHTML = `        
        <p class="text-gray-700 font-light text-md w-full mb-2 font-serif">${txt1}</p>
        <img src="/static/images/select_flight_required.png" class="w-full h-auto border mb-6" alt="...">
        `;
    }
    else if (flightReturnSelect.length === 0 && $("#selectRtOw").val() === "rt"){
        document.getElementById("btn-messagge-modal").click()
        document.getElementById("content-messagge").innerHTML = `        
        <p class="text-gray-700 font-light text-md w-full mb-2 font-serif">${txt2}</p>
        <img src="/static/images/select_flight_required_2.png" class="w-full h-auto border mb-6" alt="...">
        `;
    }
    else if (flightBeginSelect.attr("agency") != flightReturnSelect.attr("agency") && $("#selectRtOw").val() === "rt"){
        document.getElementById("btn-messagge-modal").click()
        document.getElementById("content-messagge").innerHTML = `        
        <p class="text-gray-700 font-light text-md w-full mb-2 font-serif">${txt3}</p>
        <img src="/static/images/select_flight_required_3.png" class="w-full h-auto border mb-6" alt="...">
        `;
    }
    else{
        $("#formFlights").submit()
    }
}



function onchangeFlight(e,arrivalMS,airline){
    var elementos = document.getElementsByClassName("flight-select");
    for (var i = 0; i < elementos.length; i++) {
        elementos[i].classList.remove("flight-select");
    }

    e.classList.add("flight-select");
    selectFlight(arrivalMS,airline)
}

function selectFlight(arrivalMS,airline){
    var elementos = document.getElementsByClassName("editable-return");
    
    for (var i = 0; i < elementos.length; i++) {
        
        const arrival = new Date(parseInt(arrivalMS)); 
        const departure = new Date(parseInt(elementos[i].getAttribute("date-time")));
        arrival.setHours(arrival.getHours() + 8);
        
        const airline_return = elementos[i].getAttribute("agency");
        
        if (arrival.getTime() <= departure.getTime() && airline == airline_return) {
            elementos[i].classList.remove("hidden");
        } else {
            const radio = document.getElementById(elementos[i].getAttribute("for"));
            if (radio) {radio.checked = false;}
            elementos[i].classList.add("hidden");
        }
    }
    
    document.getElementById("emptyReturnFlight").classList.remove("hidden");
    var elementos2 = document.getElementsByClassName("editable-return");    
    for (var i = 0; i < elementos2.length; i++) {
        if(!elementos[i].classList.contains("hidden") && elementos[i].innerHTML != ""){
            document.getElementById("emptyReturnFlight").classList.add("hidden");
            break;
        }
    }
}

