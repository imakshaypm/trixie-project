$(document).ready(function(){

  // var elem = document.getElementsByTagName("header")[0]
  // var elem1 = document.getElementsByTagName("footer")[0]
  // var elem2 = document.getElementsByTagName("body")[0]
  // elem2.style.marginTop = '0px'
  // elem.remove();
  // elem1.remove();

  $("#imageUpload").change(function(data){
    var imageFile = data.target.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(imageFile);
    reader.onload = function(evt){
      $('#imagePreview').attr('src', evt.target.result);
      $('#imagePreview').hide();
      $('#imagePreview').fadeIn(650);
    }
  });
});
