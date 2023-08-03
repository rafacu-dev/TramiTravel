
function liquidateBooking(id){
    let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.getElementById(`btn-liquidated-${id}`).classList.add("hidden");
    document.getElementById(`loading-liquidated-${id}`).classList.remove("hidden");

    $.ajax({
        url:"/bookings-agency/",
        type:"post",
        data:{
            'booking_id': id,
            "csrfmiddlewaretoken" : csrf
        },
        dataType:"json",
        success:function(response){
            if(response.success === "YES"){                
                document.getElementById(`btn-liquidated-${id}`).classList.add("hidden");
                document.getElementById(`loading-liquidated-${id}`).classList.add("hidden");
                document.getElementById(`liquidated-${id}`).classList.remove("hidden");

                document.getElementById(`amount-liquidated-${id}`).innerText = response.amount_liquidated;

                if(language === "es"){
                    document.getElementById("total-credit").innerText = "Crédito Total Restante: " + response.total_credit;
                }
                else{
                    document.getElementById("total-credit").innerText = "Total Credit Remaining: " + response.total_credit;
                }
                
            }
            else  if(response.success === "NO_CREDIT"){ 
                alert("no credit");
                document.getElementById(`loading-liquidated-${id}`).classList.add("hidden");
                document.getElementById(`btn-liquidated-${id}`).classList.remove("hidden");
            }
            else{
                document.getElementById(`loading-liquidated-${id}`).classList.add("hidden");
                document.getElementById(`btn-liquidated-${id}`).classList.remove("hidden");
            }            
        },
        error:function(response){
        },
    });
}


function registerPayment(){
    if(document.getElementById("emailPayment").value == "" && document.getElementById("phonePayment").value == ""){
        document.getElementById("alertZelleRequired").classList.remove("hidden");
    }
    else{
        document.getElementById("loadingRegisterPayment").classList.remove("hidden");
        document.getElementById("textRegisterPayment").classList.add("hidden");
        document.getElementById("formPaymentRegister").submit();
    }        
}