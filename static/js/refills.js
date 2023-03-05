function calculateRefills(value){
    let porcent = parseFloat(document.getElementById("porcent-refills").value);
    if(document.getElementById("coin-deposit-calculate").textContent == "USD"){
        document.getElementById("quantity-deposit").textContent = `$${value} USD`;
        document.getElementById("quantity-deposit-input").value = value;
        let _value = parseFloat(value);
        let razon = 100/(100 + (100 * porcent));
        var result = parseInt(_value * razon);
        if(result.toString() == "NaN"){result = "-"}
        document.getElementById("quantity-receibe-calculate").textContent = result;
    }else{
        let _value = parseFloat(value);
        var result = _value + (_value * porcent);
        if(result.toString() == "NaN"){
            result = "-"
            document.getElementById("quantity-deposit").textContent = "-";
            document.getElementById("quantity-deposit-input").value = 0;
        }
        else{
            document.getElementById("quantity-deposit").textContent = `$${result} USD`;
            document.getElementById("quantity-deposit-input").value = result;
        }
        document.getElementById("quantity-receibe-calculate").textContent = result;
    }
}

function copyToClickBoard(content,id){

    navigator.clipboard.writeText(content)
        .then(() => {
        console.log("Text copied to clipboard... " + content)
    })
        .catch(err => {
        console.log('Something went wrong', err);
    })

    let copy = document.getElementById(`copy${id}`);
    copy.classList.add("hidden")
    let success = document.getElementById(`successCopy${id}`);
    success.classList.remove("hidden")

    setTimeout(function(){
        success.classList.add("hidden")
        copy.classList.remove("hidden")
    }, 500);
    
}

function calculateChange(){
    if(document.getElementById("coin-deposit-calculate").textContent == "USD"){
        let usd = document.getElementById("quantity-deposit-calculate").value;

        document.getElementById("deposit-calculate").textContent = "Receibe in Cuba";
        document.getElementById("quantity-deposit-calculate").value = document.getElementById("quantity-receibe-calculate").textContent;
        document.getElementById("coin-deposit-calculate").textContent = "MLC";
        
        document.getElementById("receibe-calculate").textContent = "If deposit in USA";
        document.getElementById("quantity-receibe-calculate").textContent = usd;
        document.getElementById("coin-receibe-calculate").textContent = "USD";
    }
    else{
        let usd = document.getElementById("quantity-deposit-calculate").value;

        document.getElementById("deposit-calculate").textContent = "If deposit in USA";
        document.getElementById("quantity-deposit-calculate").value = document.getElementById("quantity-receibe-calculate").textContent;
        document.getElementById("coin-deposit-calculate").textContent = "USD";

        
        document.getElementById("receibe-calculate").textContent = "Receibe in Cuba";
        document.getElementById("quantity-receibe-calculate").textContent = usd;
        document.getElementById("coin-receibe-calculate").textContent = "MLC";
    }
}
