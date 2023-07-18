function controlSeeBooking(value){

    document.querySelectorAll('.booking-btn').forEach((element) => {
        element.className = "p-2 my-1 hover:bg-itravel-200 hover:text-black text-gray-700 text-sm w-56 text-left font-serif rounded-md booking-btn flex";
    });
    
    document.getElementById(value).className = "p-2 my-1 hover:bg-itravel-200 hover:text-black bg-itravel-200 text-sm text-black w-56 text-left font-serif rounded-md booking-btn flex";
    
    let x = document.getElementsByClassName('booking');

    for (var i = 0; i < x.length; i++) {
        x[i].classList.add('hidden');
    }
    
    let s = document.getElementsByClassName('booking-'+value);

    document.getElementById('panel-control-pdf').classList.remove('hidden');
    document.getElementById("text-booking").classList.add("hidden");
    
    document.getElementById('download-tickets').href="/download_pdf_ticket/" + value + "/0";
    document.getElementById('view-tickets').href="/download_pdf_ticket/" + value + "/1";

    for (var i = 0; i < s.length; i++) {
        s[i].classList.remove('hidden');
    }
}

function deleteBooking(reservationCode){    
    document.getElementById('toast-delete-booking').setAttribute("booking-delete", reservationCode);
    //document.getElementById('btnDelete-' + reservationCode).classList.add("hidden")
    //document.getElementById('loadingDelete-' + reservationCode).classList.remove("hidden")
}


function deleteBookingAjax(){
    let reservationCode = document.getElementById('toast-delete-booking').getAttribute("booking-delete");
    let csrf = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    document.getElementById('btnDelete-' + reservationCode).classList.add("hidden")
    document.getElementById('loadingDelete-' + reservationCode).classList.remove("hidden")
    
    document.getElementById("cancelDeleteBooking").click()

    $.ajax({
        url:"/tickets/booking-delete/",
        type:"post",
        data:{
            'reservationCode': reservationCode,
                "csrfmiddlewaretoken" : csrf
        },
        dataType:"json",
        success:function(response){
            if(response.success === "YES"){
                console.log("YES");
                document.getElementById(reservationCode).remove();

                let pending_bookings = document.getElementsByClassName("pending-bookings");
                if(document.getElementById(`booking-${reservationCode}01`).classList.contains("hidden") == false){
                    document.getElementById("panel-control-pdf").classList.add("hidden");
                    document.getElementById("text-booking").classList.remove("hidden");
                    
                }

                document.getElementById(`booking-${reservationCode}01`).remove();
                document.getElementById(`booking-${reservationCode}02`).remove();

                if(pending_bookings.length == 0){
                    document.getElementById('pending-bookings-line').classList.add("hidden");
                    document.getElementById('pending-bookings-header').classList.add("hidden");
                }
            }
            else{
                console.log("NO");
            }            
        },
        error:function(response){
        },
    });
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

// Create Countdown
var Countdown = {
  
    // Backbone-like structure
    $el: $('.countdown'),
    
    // Params
    countdown_interval: null,
    total_seconds     : 0,
    
    // Initialize the countdown  
    init: function() {
      
      // DOM
          this.$ = {
          hours  : this.$el.find('.bloc-time.hours .figure'),
          minutes: this.$el.find('.bloc-time.min .figure'),
          seconds: this.$el.find('.bloc-time.sec .figure')
         };
  
      // Init countdown values
      this.values = {
            hours  : this.$.hours.parent().attr('data-init-value'),
          minutes: this.$.minutes.parent().attr('data-init-value'),
          seconds: this.$.seconds.parent().attr('data-init-value'),
      };
      
      // Initialize total seconds
      this.total_seconds = this.values.hours * 60 * 60 + (this.values.minutes * 60) + this.values.seconds;
  
      // Animate countdown to the end 
      this.count();    
    },
    
    count: function() {
      
      var that    = this,
          $hour_1 = this.$.hours.eq(0),
          $hour_2 = this.$.hours.eq(1),
          $min_1  = this.$.minutes.eq(0),
          $min_2  = this.$.minutes.eq(1),
          $sec_1  = this.$.seconds.eq(0),
          $sec_2  = this.$.seconds.eq(1);
      
          this.countdown_interval = setInterval(function() {
  
          if(that.total_seconds > 0) {
  
              --that.values.seconds;              
  
              if(that.values.minutes >= 0 && that.values.seconds < 0) {
  
                  that.values.seconds = 59;
                  --that.values.minutes;
              }
  
              if(that.values.hours >= 0 && that.values.minutes < 0) {
  
                  that.values.minutes = 59;
                  --that.values.hours;
              }
  
              // Update DOM values
              // Hours
              that.checkHour(that.values.hours, $hour_1, $hour_2);
  
              // Minutes
              that.checkHour(that.values.minutes, $min_1, $min_2);
  
              // Seconds
              that.checkHour(that.values.seconds, $sec_1, $sec_2);
  
              --that.total_seconds;
          }
          else {
              clearInterval(that.countdown_interval);
          }
      }, 1000);    
    },
    
    animateFigure: function($el, value) {
      
       var that         = this,
               $top         = $el.find('.top'),
           $bottom      = $el.find('.bottom'),
           $back_top    = $el.find('.top-back'),
           $back_bottom = $el.find('.bottom-back');
  
      // Before we begin, change the back value
      $back_top.find('span').html(value);
  
      // Also change the back bottom value
      $back_bottom.find('span').html(value);
  
      // Then animate
      TweenMax.to($top, 0.8, {
          rotationX           : '-180deg',
          transformPerspective: 300,
            ease                : Quart.easeOut,
          onComplete          : function() {
  
              $top.html(value);
  
              $bottom.html(value);
  
              TweenMax.set($top, { rotationX: 0 });
          }
      });
  
      TweenMax.to($back_top, 0.8, { 
          rotationX           : 0,
          transformPerspective: 300,
            ease                : Quart.easeOut, 
          clearProps          : 'all' 
      });    
    },
    
    checkHour: function(value, $el_1, $el_2) {
      
      var val_1       = value.toString().charAt(0),
          val_2       = value.toString().charAt(1),
          fig_1_value = $el_1.find('.top').html(),
          fig_2_value = $el_2.find('.top').html();
  
      if(value >= 10) {
  
          // Animate only if the figure has changed
          if(fig_1_value !== val_1) this.animateFigure($el_1, val_1);
          if(fig_2_value !== val_2) this.animateFigure($el_2, val_2);
      }
      else {
  
          // If we are under 10, replace first figure with 0
          if(fig_1_value !== '0') this.animateFigure($el_1, 0);
          if(fig_2_value !== val_1) this.animateFigure($el_2, val_1);
      }    
    }
  };
  
  // Let's go !
  Countdown.init();