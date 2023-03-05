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

    var txt1 = "Debe seleccionar la fecha para el vuelo de ida.";
    var txt2 = "Debe seleccionar la fecha para el vuelo de retorno.";
    var txt3 = "Debe seleccionar vuelos que pertenescan a la misma agencia.";
    if(language === "en"){
        txt1 = "You must select the date for the outbound flight.";
        txt2 = "You must select the date for the return flight.";
        txt3 = "You must select flights that belong to the same agency.";
    }

    if ( flightBeginSelect.length === 0 ) {
        alert(txt1);
    }
    else if (flightReturnSelect.length === 0 && $("#selectRtOw").val() === "rt"){
        alert(txt2);
    }
    else if (flightBeginSelect.attr("agency") != flightReturnSelect.attr("agency") && $("#selectRtOw").val() === "rt"){
        alert(txt3);
    }
    else{
        $("#formFlights").submit()
    }
}