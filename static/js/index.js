
if(!document.getElementById("preloader").classList.contains("hidden")){
    $('#navBar').addClass("hidden");
    $('.root-index').addClass("hidden");

    
    $('#preloader').fadeOut(1000);
        
    setTimeout(function(){
        $('.root-index').removeClass("hidden");
        $('#navBar').removeClass("hidden");},1000)

    //window.onload = function(){
    //    $('#preloader').fadeOut(1000);
        
    //    setTimeout(function(){
    //        $('.root-index').removeClass("hidden");
    //        $('#navBar').removeClass("hidden");},1000)
    //};
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


//**************************************************** */
// CARRUCEL

var cont=0;
function loopSlider(){
  var xx= setInterval(function(){

        switch(cont){
            case 0:{
                $('#slider').fadeTo('slow', 0.2, function() {
                  if(screen.width < screen.height){
                    $(this).css('background-image', 'url(/static/images/bg-homepage-2-sm.webp)');
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
                    $(this).css('background-image', 'url(/static/images/bg-homepage-3.webp)');
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
                $('#slider').fadeTo('slow', 0.2, function() {
                  if(screen.width < screen.height){
                    $(this).css('background-image', 'url(/static/images/bg-homepage-1-sm.jpg)');
                  }else{
                    $(this).css('background-image', 'url(/static/images/bg-homepage-1.webp)');
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
                  <h1 class="font-bold capitalize text-xs text-3xl mb-12">
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






