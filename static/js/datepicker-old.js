function validDatepicker(element) {
    let date = element.value.split("/");
    let size = date.length;
    
    if(size > 0){
        if(date[0].charAt(0) > 1){
            element.value = "0" + date[0] + "/";
        }
        else if(date[0].charAt(0) > 0 && parseInt(date[0]) > 12){
            element.value = "12/";
        }
        else if(date[0].length === 2){
            element.value = date[0] + "/";
        }
    }
    if(size > 1){
        let dateObject = new Date();
        let monthSize = new Date(dateObject.getFullYear(), parseInt(date[0]), 0).getDate();
        
        if(date[1].length === 1 && parseInt(date[1]) > monthSize.toString().charAt(0)){
            element.value = date[0] + "/" + monthSize + "/";
        }

        if(parseInt(date[1]) > monthSize){
            element.value = date[0] + "/" + monthSize + "/";
        }

        else if(date[1].length === 2){
            element.value = element.value + "/";
        }
    } 
    if(size > 2){
        var year = parseInt(date[2]);
        if (isNaN(year)){
            year = "";
        }
        element.value = date[0] + "/" + date[1] + "/" + year;
    }
}


function setDateReturn() {
    let element = document.getElementById("date_departure");
    let dateObject = new Date();
    var date = element.value.split("/");
    var departure = new Date(parseInt(date[2]),parseInt(date[0]) - 1,parseInt(date[1]));

    if(departure < dateObject){
        var month = dateObject.getMonth() + 1;
        var day = dateObject.getDate();
        var year = dateObject.getFullYear();
        if(month < 10){month = "0"+month}
        if(day < 10){day = "0" + day}

        element.value = `${month}/${day}/${year}`
        date = element.value.split("/");
        departure = new Date(parseInt(date[2]),parseInt(date[0]) - 1,parseInt(date[1]));
    } 

    if( parseInt(date[0]) >= 1 && parseInt(date[0]) <= 12 && parseInt(date[1]) >= 1 &&
     parseInt(date[1]) <= 31 && parseInt(date[2]) >= dateObject.getFullYear()){

        let dateReturn = document.getElementById("date_return").value.split("/")
        let returnDate = new Date(parseInt(dateReturn[2]),parseInt(dateReturn[0]) - 1,parseInt(dateReturn[1]));

        if(returnDate < departure && document.getElementById("rt-radio").checked){
            document.getElementById("date_return").value = element.value;

            let dp = document.getElementById("datapicker-date_return");
            dp.classList.add("overflow-hidden");
            dp.classList.add("h-0");
            
            $(".next-btn").click();
            $(".prev-btn").click();
            
            dp.classList.remove("overflow-hidden");
            dp.classList.remove("h-0");
            //$('#datapicker-date_return').remove();
            //let e = document.getElementById("date_return")
        }
    }
}

function validDateReturn(element) {
    let dateObject = new Date();
    var date = element.value.split("/");
    var returnDate = new Date(parseInt(date[2]),parseInt(date[0]) - 1,parseInt(date[1]));

    let dateDeparture = document.getElementById("date_departure").value.split("/");
    var departure = new Date(parseInt(dateDeparture[2]),parseInt(dateDeparture[0]) - 1,parseInt(dateDeparture[1]));
    if(returnDate < departure){
        document.getElementById("date_return").value = document.getElementById("date_departure").value;
    }
}