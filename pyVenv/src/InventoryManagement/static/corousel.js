
// Set the corousel from the cookie
function setCorousel(cookie){
    var corouselState = getCookie(cookie.name);
    if (corouselState==cookie.valueLeft){
        $('#' + cookie.leftCorouselID).addClass('active')
        $('#' + cookie.rightCorouselID).removeClass('active')
    }
    else{
        $('#' + cookie.leftCorouselID).removeClass('active')
        $('#' + cookie.rightCorouselID).addClass('active')
    }
}

// Sets the cookie value
function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}


// Fetches the cookie value
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

// Erases the cookie
function eraseCookie(name) {   
    document.cookie = name+'=; Max-Age=-99999999;';  
}


// Toggle the cookie
function toggleCorouselCookie(cookie){
  var corouselState = getCookie(cookie.name);          
  if (corouselState==cookie.valueLeft){
    setCookie(cookie.name,cookie.valueRight,1)
  }
  else{
    setCookie(cookie.name,cookie.valueLeft, 1)
  }
}


// Toogle the corousel
function toggleCorousel(cookie){
  var corouselState = getCookie(cookie.name);          
  if (corouselState==cookie.valueLeft){
    setCookie(cookie.name,cookie.valueRight,1)
    $('#' + cookie.parent).carousel("next")
  }
  else{
    setCookie(cookie.name, cookie.valueLeft,1)
    $('#' + cookie.parent).carousel("prev")
  }
}


// Toggle the corousel using arrow keys (left and right)
function toogle_corousel_using_arrow_keys(e,cookie){
    var code = e.code || e.which;
    console.log(code)
    console.log(cookie.parent)
    var corouselState = getCookie(cookie.name);
    if (code == 'ArrowRight'){// left arrow key is pressed
      if(corouselState==cookie.valueRight){
        toggleCorousel(cookie);
      }
    }
    else if (code=='ArrowLeft'){// right arrow key is pressed
      if(corouselState==cookie.valueLeft){
        toggleCorousel(cookie);
      }
    }
  }