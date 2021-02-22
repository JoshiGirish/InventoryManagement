
$( function() {
  $( "#id_date__lt" ).datepicker();
  $( "#id_date__gt" ).datepicker();
} );

function getPageSize(){
  const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0)
  const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0)
  return [vh,vw];
}
