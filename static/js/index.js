
if(!document.getElementById("preloader").classList.contains("hidden")){
    $('#navBar').addClass("hidden");
    $('.root-index').addClass("hidden");

    window.onload = function(){
        $('#preloader').fadeOut(1000);
        
        setTimeout(function(){
            $('.root-index').removeClass("hidden");
            $('#navBar').removeClass("hidden");},1000)
        
        if( document.getElementById("btnLogout").classList.contains("hidden")){
          setTimeout(function(){document.getElementById("close-authentication-modal").click();},2000)
        }
    };
}

function controlDateReturn(v){
    let date_return = document.getElementById("date_return")
    if(v === 'rt'){
        date_return.disabled = false;
        date_return.attributes['required'] = 'required';
        date_return.classList.remove("cursor-not-allowed");
    }else{
        date_return.disabled = true;
        date_return.attributes['required'] = '';
        date_return.value = "";
        date_return.classList.add("cursor-not-allowed");
    }
    
}

function selectFlichts(){
  document.getElementById("flights-tab").className = "flex p-4 bg-white/60 text-itravel-900 rounded-t-lg active font-bold";
  document.getElementById("hotels-tab").className = "flex p-4 text-itravel-600 hover:text-itravel-600 hover:bg-white/50 font-medium rounded-t-lg";
}

function selectHotels(){
  document.getElementById("hotels-tab").className = "flex p-4 bg-white/60 text-itravel-900 rounded-t-lg active font-bold";
  document.getElementById("flights-tab").className = "flex p-4 text-itravel-600 hover:text-itravel-600 hover:bg-white/50 font-medium rounded-t-lg";
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


function selectFrom(id_select){
	const select = document.getElementById("to-hotels");
	
	for (let i = select.options.length; i >= 1; i--) {
		select.remove(i);
	}

	window.objTo.forEach(obj => {       
		if(obj.id_from == id_select) {
			const option = document.createElement('option');
			option.text = obj.name;
			option.value = obj.id;
			select.appendChild(option);
		}
	})
}
function selectTo(id_select){
	const select = document.getElementById("hotel");
	
	for (let i = select.options.length; i >= 1; i--) {
		select.remove(i);
	}
	window.objHotels.forEach(obj => {       
		if(obj.id_to == id_select) {
			const option = document.createElement('option');
			option.text = obj.name;
			option.value = obj.id;
			select.appendChild(option);
		}
	})
  const option = document.createElement('option');
  option.text = "All";
  option.value = "All";
  select.appendChild(option);
}
function selectHotel(id_select){
	const select = document.getElementById("room-type");
	
	for (let i = select.options.length; i >= 1; i--) {
		select.remove(i);
	}
	
	window.objHotels.forEach(obj => { 
		if(obj.id == id_select) {
			document.getElementById("textClientsHotels").innerText = "Rooms:1  Clientes: 1";
            
            var htmlAdults = '<option value = "1" selected="true">1</option>'
            for (let i = 2; i <= obj.max_adults; i++) {
                htmlAdults += `<option value = "${i}">${i}</option>`
            }
            for (let i = 1; i <= 9; i++) {
                document.getElementById(`adults-room-${i}`).innerHTML = htmlAdults;
            }
            
            var htmlChildrens = '<option value = "0" selected="true">0</option>'
            for (let i = 1; i <= obj.max_childrens; i++) {
                htmlChildrens += `<option value = "${i}">${i}</option>`
            }
            var htmlInfants = '<option value = "0" selected="true">0</option>'
            for (let i = 1; i <= obj.max_infants; i++) {
                htmlInfants += `<option value = "${i}">${i}</option>`
            }

            for (let i = 1; i <= 9; i++) {
                document.getElementById(`childrens-room-${i}`).innerHTML = htmlChildrens;
                document.getElementById(`infants-room-${i}`).innerHTML = htmlInfants;
            }
			//document.getElementById("adultsLabelClientsHotels").setAttribute("max",obj.max_adults);
			//document.getElementById("childrenLabelClientsHotels").setAttribute("max",obj.max_childrens);
			//document.getElementById("infantsLabelClientsHotels").setAttribute("max",obj.max_infants);
		}
	})
	window.objRoomType.forEach(obj => {       
		if(obj.id_hotel == id_select) {
			const option = document.createElement('option');
			option.text = obj.name;
			option.value = obj.id;
			select.appendChild(option);
		}
	})
  const option = document.createElement('option');
  option.text = "All";
  option.value = "All";
  select.appendChild(option);
}

function selectRooms(c){
    let cant = parseInt(c);
    for (let i = 2; i <= cant; i++) {
        document.getElementById(`lbl-room-${i}`).classList.remove("hidden");
        document.getElementById(`div-adults-room-${i}`).classList.remove("hidden");
        document.getElementById(`div-childrens-room-${i}`).classList.remove("hidden");
        document.getElementById(`div-infants-room-${i}`).classList.remove("hidden");
    }
    for (let i = cant+1; i <= 9; i++) {
        document.getElementById(`lbl-room-${i}`).classList.add("hidden");
        document.getElementById(`div-adults-room-${i}`).classList.add("hidden");
        document.getElementById(`div-childrens-room-${i}`).classList.add("hidden");
        document.getElementById(`div-infants-room-${i}`).classList.add("hidden");
        
        document.getElementById(`adults-room-${i}`).value = 1;
        document.getElementById(`childrens-room-${i}`).value = 0;
        document.getElementById(`infants-room-${i}`).value = 0;
    }
    calculateClientsPackage()
}

function calculateClientsPackage(){
    let cant = parseInt(document.getElementById("cant-rooms").value);
    var adults = 0;
    var childrens = 0;
    var infants = 0;
    var room_clients = "";
    for (let i = 1; i <= cant; i++) {
        let adult = parseInt(document.getElementById(`adults-room-${i}`).value);
        let children = parseInt(document.getElementById(`childrens-room-${i}`).value);
        let infant = parseInt(document.getElementById(`infants-room-${i}`).value);

        room_clients += `${adult}-${children}-${infant}%`;

        adults += adult
        childrens += children
        infants += infant
    }
    
    document.getElementById("input-room-clients").value = room_clients;

    let cllients = adults + childrens + infants;
    document.getElementById("textClientsHotels").innerText = "Rooms: " + cant + "  Clientes: " + cllients;
}

//**************************************************** */
// CARRUCEL

var cont=0;
function loopSlider(){
  var xx= setInterval(function(){

        switch(cont){
            case 0:{
                $('#slider').fadeTo('slow', 0.2, function() {
                  if(screen.width < screen.height){
                    $(this).css('background-image', 'url(/static/images/bg-homepage-2-sm.jpg)');
                  }else{
                    $(this).css('background-image', 'url(/static/images/bg-homepage-2.webp)');
                  }
                  }).fadeTo('slow', 1);
                  if(language === "es"){
                    changedText("Vuelos a todo el mundo","Los mejores precios de Miami"); //ADD_CUBA- Vuelos a Cuba","Los mejores precios de Miami
                  }
                  else{
                    changedText("Flights to the whole world","The best prices in Miami");//ADD_CUBA- Flights to Cuba
                  }
                cont=1;        
                break;
            }
            case 1:{
                $('#slider').fadeTo('slow', 0.2, function() {
                  if(screen.width < screen.height){
                    $(this).css('background-image', 'url(/static/images/bg-homepage-3-sm.jpg)');
                  }else{
                    $(this).css('background-image', 'url(/static/images/bg-homepage-3.jpg)');
                  }
                  }).fadeTo('slow', 1);
                  if(language === "es"){
                    changedText("Trámites Consulares","Pasaportes, Visas y Repatriación");
                  }
                  else{
                    changedText("Consular procedures","Passports, Visas and Repatriation");
                  }
                cont=2;
                break;
            }
            case 2:{
                $('#slider').fadeTo('slow', 0.2, function() {
                  if(screen.width < screen.height){
                    $(this).css('background-image', 'url(/static/images/bg-homepage-4-sm.jpg)');
                  }else{
                    $(this).css('background-image', 'url(/static/images/bg-homepage-4.jpg)');
                  }
                  }).fadeTo('slow', 1)
                  if(language === "es"){
                    changedText("Viaja a Punta Cana","Paquetes de verano desde $ 1057");
                  }
                  else{
                    changedText("Trips to Punta Cana","Summer packages from $1057");
                  }
                cont=3;
                break;
            }  
            case 3:{
                $('#slider').fadeTo('slow', 0.2, function() {
                  if(screen.width < screen.height){
                    $(this).css('background-image', 'url(/static/images/bg-homepage-5-sm.webp)');
                  }else{
                    $(this).css('background-image', 'url(/static/images/bg-homepage-5.webp)');
                  }
                  }).fadeTo('slow', 1);
                  if(language === "es"){
                    changedText("Trámites de imigración","Permiso de trabajo y Residencia Americana");
                  }
                  else{
                    changedText("Immigration procedures","Work permit and American Residence");
                  }
                cont=4;
                break;
            }  
            case 4:{
                $('#slider').fadeTo('slow',0.2, function() {
                  if(screen.width < screen.height){
                    $(this).css('background-image', 'url(/static/images/bg-homepage-1-sm.jpg)');
                  }else{
                    $(this).css('background-image', 'url(/static/images/bg-homepage-1.jpg)');
                  }
                  }).fadeTo('slow', 1);
                  if(language === "es"){
                    changedText("Viajes a multiples destinos con","Aerolíneas Regulares Charters");
                  }
                  else{
                    changedText("Flights to multiple destination with","Regular Airlines And Charters");
                  }
                cont=0;
                break;
            }  
        }
        
    },20000);

}

function changedText(text1,text2){
    var content_text = document.getElementById("content_text");
    content_text.replaceChildren();
    
    var html = ` <h1 class="font-semibold capitalize text-md text-5xl  xl:text-6xl mt-20 text-white w-auto">
                      <span class="animate-letra  h-20"><span class="w-full font-serif text-shadow" >${text1}</span></span>
                  </h1>
                  <h1 class="font-bold capitalize text-xs md:text-3xl mb-12">
                      <span class="animate-letra"><span class="w-full font-serif text-shadow-sm">${text2}</span></span>
                  </h1>`

    content_text.innerHTML = html;
    
    
    var content_text_sm = document.getElementById("content_text_sm");
    content_text_sm.replaceChildren();
    var html = `
    <h1 class="font-serif font-semibold capitalize text-md text-3xl md:text-4xl mt-12 md:mt-20 mb-6 text-white w-auto lg:hidden text-shadow-sm">${text1}</h1>
    <h1 class="font-serif font-bold capitalize text-xs text-2xl md:text-3xl lg:hidden text-shadow-sm">${text2}</h1>`

    content_text_sm.innerHTML = html;
}
function reinitLoop(time){
  clearInterval(xx);
  setTimeout(loopSlider(),time);
}

$(window).ready(function(){
    loopSlider();

});






