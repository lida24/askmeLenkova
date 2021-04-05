var $registerForm = $('#ask');

if($registerForm.length){
  $registerForm.validate({
    rules:{
      title:{
        required: true
      },
    text: {
              required: true
          },
          tags:{
            required: true
          }
        },
    messages:{
      title: {
        required: 'Please enter title!'
      },
      text: {
              required: 'Please enter text!',
          },
          tags: {
            required: 'Please enter tags!'
          }
    },
});
}
