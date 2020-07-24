window.onload = function(){
    $.ajax({
          url: 'https://localhost:8000/history',
          type: 'GET'
      });
    }