

var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
var months_min = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
var weekday = ['Sun','Mon','Tue','Wed','Thur','Fri','Sat']

if(language === "es"){
    months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Augosto', 'Septiembre', 'Octubre', 'Noviembre', 'Deciembre']
    months_min = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    weekday = ['Dom','Lun','Mar','Mie','Jue','Vie','Sab']
}

var currentDate = new Date()


var dayMonth = 1

var dateInitial = document.getElementById("date_departure").value.split("/")

var currentMonth = new Date()
currentMonth.setFullYear(dateInitial[2],parseInt(dateInitial[0])-1,dateInitial[1])

var selectedDate = new Date()
selectedDate.setFullYear(dateInitial[2],parseInt(dateInitial[0])-1,dateInitial[1])


var dayInitial = parseInt(dateInitial[1])
if(dayInitial < 6){

}
else if(dayInitial < 11){
    dayMonth = 6
}
else if(dayInitial < 16){
    dayMonth = 11
}
else if(dayInitial < 21){
    dayMonth = 16
}
else if(dayInitial < 26){
    dayMonth = 21
}
else {
    dayMonth = 26
}

// Render
renderMonthSelection();
renderDaySelection(dayMonth);

function prevMonth() {
    dayMonth -= 5;
    if( dayMonth <= 0){
        currentMonth.addMonth(-1);
        dayMonth = 26;
        let totalDaysInMonth = daysInMonth(currentMonth.getMonth() + 1, currentMonth.getFullYear());
        if(totalDaysInMonth < 30){
            dayMonth = 21;
        }
    }
    renderMonthSelection();
    renderDaySelection(dayMonth);
}

function nextMonth() {
    dayMonth += 5;
    let totalDaysInMonth = daysInMonth(currentMonth.getMonth() + 1, currentMonth.getFullYear());
    
    if( dayMonth >= totalDaysInMonth || totalDaysInMonth - dayMonth < 4){
        currentMonth.addMonth(1);
        dayMonth = 1;
    }
    renderMonthSelection();
    renderDaySelection(dayMonth);
}

function showReturns(){    
    var elementos = document.getElementsByClassName("editable-return");
    document.getElementById("emptyReturnFlight").classList.remove("hidden");
    console.log(elementos)
    for (var i = 0; i < elementos.length; i++) {
        elementos[i].classList.remove("hidden");
        const radio = document.getElementById(elementos[i].getAttribute("for"));
        if (radio) {radio.checked = false;}
        document.getElementById("emptyReturnFlight").classList.add("hidden");
    }
}

function renderDaySelection(dm) {
    let daySelectionNode = document.getElementById("day-selection");

    while (daySelectionNode.firstChild) {
        daySelectionNode.removeChild(daySelectionNode.firstChild)
    }

    // Get total days in month
    let totalDaysInMonth = daysInMonth(currentMonth.getMonth() + 1, currentMonth.getFullYear())

    var sum = 5
    if(totalDaysInMonth - dm > 4 && totalDaysInMonth - dm < 9){
        sum = totalDaysInMonth - dm + 1
    }

    // Append new nodes
    for (i = dm; i < dm + sum; i++) {
        
        var textColor = "";
        var cursor = " cursor-pointer";

        let tempDate = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), i);

        if(tempDate <= currentDate){
            textColor = " text-gray-400 disabled";
            cursor = "";
            
            if (i == dm){
                let prevMonth = document.getElementById("prevMonth");                
                prevMonth.classList.remove("text-itravel-200");
                prevMonth.classList.remove("hover:text-itravel-400");
                prevMonth.classList.add("text-gray-400");
                prevMonth.disabled = true;
            }
        }
        else if (i == dm){
            let prevMonth = document.getElementById("prevMonth");            
            prevMonth.classList.add("text-itravel-200");
            prevMonth.classList.add("hover:text-itravel-400");
            prevMonth.classList.remove("text-gray-400");
            prevMonth.disabled = false;
        }

        let btn = document.createElement('button');
        btn.className = 'day w-full text-center inline-block rounded-lg mr-2 py-1 day-selection ' + cursor;
        btn.type = "button";
        

        let el = document.createElement('div');
        el.className = 'w-full text-center text-xs font-serif' + textColor;
        el.textContent = weekday[getWeekday(i, currentMonth.getMonth(), currentMonth.getFullYear())];
        
        btn.appendChild(el);


        let el2 = document.createElement('div');
        el2.className = 'w-full text-center font-bold text-xs sm:text-xl ' + textColor;
        el2.textContent = i;
        btn.appendChild(el2);
        
        if(textColor == ""){
            btn.addEventListener('click', function(e) {
                document.querySelectorAll('.day-selection').forEach((element) => {
                    element.classList.remove('bg-itravel-900/20');
                    element.classList.remove('border');
                    element.classList.remove('border-solid');
                    element.classList.remove('day-selected');
                });
                btn.classList.add('bg-itravel-900/20');
                    btn.classList.add('border');
                    btn.classList.add('border-solid');
                    btn.classList.add('day-selected');

                var m = currentMonth.getMonth() + 1;
                if(parseFloat(m) < 10){
                    m = "0" + m;
                }
                var d = el2.textContent;

                if(parseFloat(d) < 10){
                    d = "0" + d
                }
                

                selectedDate.setFullYear(currentMonth.getFullYear(),currentMonth.getMonth(),parseInt(d))
                var dateSend = currentMonth.getFullYear() + "-"  + m + "-" + d;

                var begin = document.getElementById("begin").value;
                var to = document.getElementById("to").value;              

                if (selectedDate2 < selectedDate){
                    selectedDate2.setFullYear(currentMonth.getFullYear(),currentMonth.getMonth(),parseInt(d));
                    dayMonth2 = dayMonth;
                    currentMonth2.setFullYear(currentMonth.getFullYear(),currentMonth.getMonth(),dayMonth2);
                    
                    try {renderMonthSelection2()} catch (error) {}
                    try {renderDaySelection2(dayMonth2)} catch (error) {}
                    try {getFlights("day-selection2",dateSend,begin,to);} catch (error) {}
                        
                }
                else{
                    
                    try {renderMonthSelection2()} catch (error) {}
                    try {renderDaySelection2(dayMonth2)} catch (error) {}
                }

                getFlights("day-selection",dateSend,begin,to);  

            })
        }

        daySelectionNode.appendChild(btn)

        if (selectedDate.getDate() == i && selectedDate.getMonth() == currentMonth.getMonth() &&
        selectedDate.getFullYear() == currentMonth.getFullYear()) {
            btn.classList.add('border')
            btn.classList.add('border-solid')
            btn.classList.add('bg-itravel-900/20');
            btn.classList.add('day-selected');
        }

    }

}

function renderMonthSelection() {
    document.getElementById('month-selection').textContent = months[currentMonth.getMonth()] + ' ' + currentMonth.getFullYear();
}

try {

    var dayMonth2 = 1;
    var dateInitial2 = document.getElementById("date_return").value.split("/");
    
    var currentMonth2 = new Date()
    currentMonth2.setFullYear(dateInitial2[2],parseInt(dateInitial2[0])-1,dateInitial2[1])
    
    var selectedDate2 = new Date()
    selectedDate2.setFullYear(dateInitial2[2],parseInt(dateInitial2[0])-1,dateInitial2[1])

    
    var dayInitial2 = parseInt(dateInitial2[1])
    var currentMonth2 = new Date()
    currentMonth2.setFullYear(dateInitial2[2],parseInt(dateInitial2[0])-1,dateInitial2[1])
    if(dayInitial2 < 6){

    }
    else if(dayInitial2 < 11){
        dayMonth2 = 6
    }
    else if(dayInitial2 < 16){
        dayMonth2 = 11
    }
    else if(dayInitial2 < 21){
        dayMonth2 = 16
    }
    else if(dayInitial2 < 26){
        dayMonth2 = 21
    }
    else {
        dayMonth2 = 26
    }
    
    renderMonthSelection2();
    renderDaySelection2(dayMonth2);

} catch (error) {
    console.log("error al crear el selector 2");
}



// Func2
function prevMonth2() {
    dayMonth2 -= 5
    if( dayMonth2 <= 0){
        currentMonth2.addMonth(-1)
        dayMonth2 = 26
        let totalDaysInMonth = daysInMonth(currentMonth2.getMonth() + 1, currentMonth2.getFullYear())
        if(totalDaysInMonth < 30){
            dayMonth2 = 21
        }
    }
    renderMonthSelection2()
    renderDaySelection2(dayMonth2)
}

function nextMonth2() {
    dayMonth2 += 5
    let totalDaysInMonth = daysInMonth(currentMonth2.getMonth() + 1, currentMonth2.getFullYear())
    if( dayMonth2 >= totalDaysInMonth || totalDaysInMonth - dayMonth2 < 5){
        currentMonth2.addMonth(1)
        dayMonth2 = 1
    }
    renderMonthSelection2()
    renderDaySelection2(dayMonth2)
}

function renderMonthSelection2() {
    document.getElementById("month-selection2").textContent = months[currentMonth2.getMonth()] + ' ' + currentMonth2.getFullYear()
}

function renderDaySelection2(dm) {
    
    // Clear existing nodes first
    let daySelectionNode = document.getElementById("day-selection2");

    while (daySelectionNode.firstChild) {
        daySelectionNode.removeChild(daySelectionNode.firstChild)
    }

    // Get total days in month
    let totalDaysInMonth = daysInMonth(currentMonth2.getMonth() + 1, currentMonth2.getFullYear())

    var sum = 5
    if(totalDaysInMonth - dm > 4 && totalDaysInMonth - dm < 9){
        sum = totalDaysInMonth - dm + 1
    }


    // Append new nodes
    for (i = dm; i < dm + sum; i++) {
        
        var textColor = "";
        var cursor = " cursor-pointer";

        let tempDate = new Date(currentMonth2.getFullYear(), currentMonth2.getMonth(), i);

        if(tempDate <= currentDate){
            textColor = " text-gray-400 disabled";
            cursor = "";
            
            if (i == dm){
                let prevMonth = document.getElementById("prevMonth-2");
                
                prevMonth.classList.remove("text-itravel-200");
                prevMonth.classList.remove("hover:text-itravel-400");
                prevMonth.classList.add("text-gray-400");
                prevMonth.disabled = true;
            }
        }
        else if (i == dm){
            let prevMonth = document.getElementById("prevMonth-2");
            
            prevMonth.classList.add("text-itravel-200");
            prevMonth.classList.add("hover:text-itravel-400");
            prevMonth.classList.remove("text-gray-400");
            prevMonth.disabled = false;
        }
        
        tempDate.getTime()
        if(tempDate < selectedDate.setHours(0,0,0,0)){
            textColor = " text-gray-400 disabled";
            cursor = "";
            
            if (i == dm){
                let prevMonth = document.getElementById("prevMonth-2");
                
                prevMonth.classList.remove("text-itravel-200");
                prevMonth.classList.remove("hover:text-itravel-400");
                prevMonth.classList.add("text-gray-400");
                prevMonth.disabled = true;
            }
        }

        let btn = document.createElement('button');
        btn.className = 'day w-full ' + sum + ' text-center inline-block rounded-lg mr-2 py-1 day-selection2 ' + cursor;
        btn.type = "button";
        

        let el = document.createElement('div');
        el.className = 'w-full text-center text-xs font-serif' + textColor;
        el.textContent = weekday[getWeekday(i, currentMonth2.getMonth(), currentMonth2.getFullYear())];
        
        btn.appendChild(el);


        let el2 = document.createElement('div');
        el2.className = 'w-full text-center font-bold text-xs sm:text-xl' + textColor;
        el2.textContent = i;
        btn.appendChild(el2);
        
        if(textColor == ""){
            btn.addEventListener('click', function(e) {
                document.querySelectorAll('.day-selection2').forEach((element) => {
                    element.classList.remove('bg-itravel-900/20');
                    element.classList.remove('border');
                    element.classList.remove('border-solid');
                    element.classList.remove('day-selected');
                });
                btn.classList.add('bg-itravel-900/20');
                    btn.classList.add('border');
                    btn.classList.add('border-solid');
                    btn.classList.add('day-selected');

                var m = currentMonth2.getMonth() + 1;
                if(parseFloat(m) < 10){
                    m = "0" + m;
                }
                var d = el2.textContent;

                if(parseFloat(d) < 10){
                    d = "0" + d
                }
                selectedDate2.setFullYear(currentMonth2.getFullYear(),currentMonth2.getMonth(),parseInt(d))
                var dateSend = currentMonth2.getFullYear() + "-"  + m + "-" + d;

                var begin = document.getElementById("begin").value;
                var to = document.getElementById("to").value;

                getFlights("day-selection2",dateSend,begin,to);
            })
        }
        
        // Customise Tailwind classes here
        document.getElementById("day-selection2").appendChild(btn);

        if (selectedDate2.getDate() == i && selectedDate2.getMonth() == currentMonth2.getMonth() &&
        selectedDate2.getFullYear() == currentMonth2.getFullYear()) {
            btn.classList.add('bg-itravel-900/20');
            btn.classList.add('border');
            btn.classList.add('border-solid');
            btn.classList.add('day-selected');
        }

    }

}













function daysInMonth(month, year) {
    return new Date(year, month, 0).getDate();
}

function getWeekday(day,month, year) {
    return new Date(year, month, day).getDay();
}

function getFlightsForAvailableDate(id,year,month,day,begin,to){
    if(id == 'day-selection'){
        dateInitial = [month,day,year];
        dayInitial = day;

        let _day = parseInt(day);
        if(_day < 6){
            dayMonth = 1
        }
        else if(_day < 11){
            dayMonth = 6
        }
        else if(_day < 16){
            dayMonth = 11
        }
        else if(_day < 21){
            dayMonth = 16
        }
        else if(_day < 26){
            dayMonth = 21
        }
        else {
            dayMonth = 26
        }

        selectedDate.setFullYear(year,month-1,day);
        currentMonth.setFullYear(year,month-1,day);
        renderMonthSelection();
        renderDaySelection(dayMonth);
        let ds = year + "-"  + month + "-" + day;
        getFlights(id,ds,begin,to);

        if (selectedDate2 < selectedDate){
            selectedDate2.setFullYear(year,month-1,day);
            dayMonth2 = dayMonth;
            currentMonth2.setFullYear(year,month-1,day);
            
            try {renderMonthSelection2()} catch (error) {}
            try {renderDaySelection2(dayMonth2)} catch (error) {}
            try {
                let ds = year + "-"  + month + "-" + day;
                getFlights('day-selection2',ds,begin,to);
            } catch (error) {}
        }
        else if (document.getElementById("emptyReturnFlight").classList.contains("hidden") == false ){
            try {renderMonthSelection2()} catch (error) {}
            try {renderDaySelection2(dayMonth2)} catch (error) {}
            try {
                let ds = selectedDate2.getFullYear() + "-"  + (selectedDate2.getMonth() + 1) + "-" + selectedDate2.getDate();
                console.log(ds)
                getFlights('day-selection2',ds,begin,to);
            } catch (error) {}
        }

    }else{
        dateInitial2 = [month,day,year];
        dayInitial2 = day;
        
        let _day = parseInt(day);
        if(day < 6){
            dayMonth2 = 1
        }
        else if(_day < 11){
            dayMonth2 = 6
        }
        else if(_day < 16){
            dayMonth2 = 11
        }
        else if(_day < 21){
            dayMonth2 = 16
        }
        else if(_day < 26){
            dayMonth2 = 21
        }
        else {
            dayMonth2 = 26
        }

        selectedDate2.setFullYear(year,month-1,day);
        currentMonth2.setFullYear(year,month-1,day);
        
        try {renderMonthSelection2()} catch (error) {}
        try {renderDaySelection2(dayMonth2)} catch (error) {}
        try {
            let ds = year + "-"  + month + "-" + day;
            getFlights('day-selection2',ds,begin,to); 
        } catch (error) {}
    }

}

function getFlights(id,dateSend,begin,to){
    var table = "";
    var emptyOut = "";
    var loading = "";
    var available_dates = "";
    var date_departure,date_return;

    if(id == 'day-selection'){
        table = "tableOutboundFlights";
        emptyOut = "emptyOutboundFlight";
        loading = "contentLoadingOutboundFlight";
        available_dates = "available_dates";
        date_departure = dateSend;
        date_return = "none";
        try {
            showReturns();
        } catch (error) {
            console.log("Elemento de retorno no existe");
        }
    }
    else{
        table = "tableReturnFlights";
        emptyOut = "emptyReturnFlight";
        loading = "contentLoadingReturnFlight";
        available_dates = "available_dates_return";

        let t = begin;
        let b = to;
        begin = b;
        to = t;

        date_return = dateSend;
        date_departure = `${selectedDate.getFullYear()}-${selectedDate.getMonth()+1}-${selectedDate.getDate()}`
    }

    $('#' + table + ' .editable').empty();
    document.getElementById(emptyOut).classList.add("hidden");
    document.getElementById(available_dates).classList.add("hidden");
    $('#' + available_dates).empty();

    document.getElementById(loading).classList.remove("hidden");
    document.getElementById(loading).classList.remove("hidden");

    $.ajax({
        url:`/fligths/get/${date_departure}/${date_return}/${begin}/${to}/${document.getElementById("adults").value}/${document.getElementById("children").value}/${document.getElementById("infants").value}/${class_types}`,
        type:"get",
        dataType:"json",
        success:function(response){
            document.getElementById(loading).classList.add("hidden");


            if(response.available_dates){
                let empty = document.getElementById(emptyOut);
                empty.classList.remove("hidden");
                
                if(language === "es"){
                    empty.textContent = "No hay vuelos disponibles para esta fecha";
                }else{
                    empty.textContent = "There are no flights available for this date";
                }
                
                let ad = document.getElementById(available_dates);
                if(response.available_dates.length > 0){
                    ad.classList.remove("hidden");
                    if(language === "es"){
                        ad.textContent = "Las fechas más próximas con vuelos disponibles son:"; 
                    }else{
                        ad.textContent = "The closest dates with available flights are:"; 
                    }           
                    let br = document.createElement('br');
                    ad.appendChild(br);
                }else{
                    ad.classList.add("hidden");
                }

                response.available_dates.forEach(element => {

                    let btn = document.createElement('button');
                    btn.className = "text-blue-600 mx-3";
                    btn.textContent = `${months_min[parseInt(element[1]) - 1]}. ${element[2]}, ${element[0]}`;
                    btn.type = "button";
                    btn.addEventListener("click",function(){

                        if(id == 'day-selection'){
                            dateInitial = [element[1],element[2],element[0]];
                            dayInitial = element[2];

                            let day = parseInt(element[2]);
                            if(day < 6){
                                dayMonth = 1
                            }
                            else if(day < 11){
                                dayMonth = 6
                            }
                            else if(day < 16){
                                dayMonth = 11
                            }
                            else if(day < 21){
                                dayMonth = 16
                            }
                            else if(day < 26){
                                dayMonth = 21
                            }
                            else {
                                dayMonth = 26
                            }

                            selectedDate.setFullYear(element[0],element[1]-1,element[2]);
                            currentMonth.setFullYear(element[0],element[1]-1,element[2]);
                            renderMonthSelection()
                            renderDaySelection(dayMonth);
                            let ds = element[0] + "-"  + element[1] + "-" + element[2];
                            getFlights(id,ds,begin,to);
                            
                            if (selectedDate2 < selectedDate){
                                selectedDate2.setFullYear(element[0],element[1]-1,element[2]);
                                dayMonth2 = dayMonth;
                                currentMonth2.setFullYear(element[0],element[1]-1,element[2]);
                                
                                try {renderMonthSelection2()} catch (error) {}
                                try {renderDaySelection2(dayMonth2)} catch (error) {}
                                try {getFlights('day-selection2',ds,begin,to);} catch (error) {}
                            }
                            else{
                                renderMonthSelection2()
                                renderDaySelection2(dayMonth2)
                            }
                            

                        }else{
                            dateInitial2 = [element[1],element[2],element[0]];
                            dayInitial2 = element[2];
                            
                            let day = parseInt(element[2]);
                            if(day < 6){
                                dayMonth2 = 1
                            }
                            else if(day < 11){
                                dayMonth2 = 6
                            }
                            else if(day < 16){
                                dayMonth2 = 11
                            }
                            else if(day < 21){
                                dayMonth2 = 16
                            }
                            else if(day < 26){
                                dayMonth2 = 21
                            }
                            else {
                                dayMonth2 = 26
                            }

                            selectedDate2.setFullYear(element[0],element[1]-1,element[2]);
                            currentMonth2.setFullYear(element[0],element[1]-1,element[2]);
                            
                            try {renderMonthSelection2()} catch (error) {}
                            try {renderDaySelection2(dayMonth2)} catch (error) {}
                            try {
                                let ds = element[0] + "-"  + element[1] + "-" + element[2];
                                getFlights(id,ds,to,begin);
                            } catch (error) {}
                        }
                    })
                    ad.appendChild(btn);
                });
            }
            else{
                response.flights.forEach(element => {
                    addRowTableOutboundFlights(table,element);
                });
            }
            
        },
        error:function(response){
            document.getElementById(loading).classList.add("hidden");
            let empty = document.getElementById(emptyOut);
            empty.classList.remove("hidden");
            empty.textContent = "Connection error. Try again";
        },
    });
}

// Prototypes
Date.prototype.addMonth = function(n) {
    return new Date(this.setMonth(this.getMonth() + n, 1));
}



function addRowTableOutboundFlights(table,element) {
    var Id = "rReturn_";
    var n = "flightReturnSelect";
    var cn = "editable  editable-return";
    if(table == "tableOutboundFlights"){
        Id = "rbegin_";
        n = "flightBeginSelect";
        cn = "editable";
    }
    
    let id = element["id"];
    let date = element["date"];
    let ability = element["ability"];
    let price = element["price"];
    let actived = element["actived"];
    let priceMoney = element["priceMoney"];
    let begin = element["begin"];
    let to = element["to"];
    let airline = element["airline"];
    let airlineImage = element["airlineImage"];
    let departure = element["departure"].split(":");
    let arrival = element["arrival"].split(":");
    let duration = element["duration"];
    
    // Obtiene una referencia a la tabla
    var tableOutboundFlights = document.getElementById(table);

    // Inserta una fila en la tabla, en el índice 0
    var newRow = tableOutboundFlights.insertRow(1);
    newRow.className = cn;
    if(Id === "rReturn_"){
        newRow.setAttribute("date-time",element["departureMS"]);   
        newRow.setAttribute("agency",element["airline_id"]);
        newRow.setAttribute("for",Id + id);
    }

    // Inserta una celda en la fila, en el índice 0
    let newCell0  = newRow.insertCell(0);
    newCell0.className = 'align-middle font-light text-sm whitespace-nowrap md:px-2 pt-4 text-left';
    
    
    let div0 = document.createElement('div');
    div0.className = "flex items-center space-x-4";
    
    let div01 = document.createElement('div');
    div01.className = "hidden lg:flex lg:w-auto";
    
    let img = document.createElement('img');
    img.className = "w-8 h-8 rounded-full bg-gray-50";
    img.src = airlineImage;
    div01.appendChild(img);
    
    div0.appendChild(div01);


    let div02 = document.createElement('div');
    div02.className = "flex-1 min-w-0";

    
    let div_airline = document.createElement('div');
    div_airline.className = "flex";

    let p = document.createElement('p');
    p.className = "text-sm font-medium text-gray-900 truncate";
    p.textContent = airline;
    div_airline.appendChild(p);
    
    if(element["baggagePolicy"]){
        let baggagePolicy = element["baggagePolicy"];
        let a = document.createElement('a');
        a.className = "material-icons text-gray-500 text-sm ml-3";
        a.href=`/baggage-policy/${baggagePolicy}`;
        a.textContent = "business_center";
        a.target="_blank";
        a.rel="noreferrer";
        div_airline.appendChild(a);
    }
    
    div02.appendChild(div_airline);
    
    let div03 = document.createElement('div');
    div03.className = "flex";

    let span = document.createElement('span');
    span.className = "text-md md:text-lg font-bold truncate";
    span.textContent = `${departure[0]}:${departure[1]}`;
    div03.appendChild(span);

    
    let span1 = document.createElement('span');
    span1.className = "text-xs pt-1 md:pt-2";
    span1.textContent = departure[2];
    div03.appendChild(span1);

    let span2 = document.createElement('span');
    span2.className = "md:text-lg font-bold truncate md:mx-5";
    span2.textContent = " ➜ ";
    div03.appendChild(span2);

    let span3 = document.createElement('span');
    span3.className = "text-md md:text-lg font-bold truncate";
    span3.textContent = `${arrival[0]}:${arrival[1]}`;
    div03.appendChild(span3);

    let span4 = document.createElement('span');
    span4.className = "text-xs pt-1 md:pt-2";
    span4.textContent = arrival[2];
    div03.appendChild(span4);

    div02.appendChild(div03);
    
    div0.appendChild(div02);

    let label1 = document.createElement('label');
    label1.appendChild(div0);
    label1.htmlFor = Id + id;
    newCell0.appendChild(label1);




    var newCell1  = newRow.insertCell(1);
    newCell1.className = "align-middle font-light text-sm whitespace-nowrap px-1 md:px-2 pt-4 text-center";
    let label2 = document.createElement('label');
    label2.textContent = duration;
    newCell1.appendChild(label2);

    var newCell2  = newRow.insertCell(2);
    newCell2.className = "align-middle font-light text-xs md:text-sm whitespace-nowrap px-1 md:px-2 pt-4 text-center"; 
    
    let div = document.createElement('div');
    div.className = 'inline-flex justify-center items-center p-0.5 rounded-lg cursor-pointer border-select-flight';
    div.setAttribute("style",class_types_css)
    
    let input = document.createElement('input');
    input.className = 'hidden peer';
    input.id = Id + id;
    input.type="radio";
    input.value= id;
    input.required= 'required';
    input.name = n;
    input.setAttribute("agency",element["airline_id"]);
    if(Id !== "rReturn_"){
        input.onchange = function() {
            selectFlight(element["arrivalMS"],element["airline_id"]);
            input.classList.add("flight-select")
        }
        input.setAttribute("date-time",element["arrivalMS"]);
        input.setAttribute("agency",element["airline_id"]);
    }else{
        const elemento = document.querySelector('.flight-select');
        if (elemento !== null) {         
            selectFlight(elemento.getAttribute("date-time"),elemento.getAttribute("agency"));
        }
    }
    div.appendChild(input);


    let label = document.createElement('label');
    label.className = 'w-full text-gray-900 relative w-full px-1.5 md:px-5 py-1.5 md:py-2.5 transition-all ease-in duration-75 rounded-md bg-white peer-checked:text-white peer-checked:bg-transparent font-bold cursor-pointer';
    label.htmlFor = Id + id;
    label.textContent = priceMoney;

    div.appendChild(label);
    
    newCell2.appendChild(div);

    

};