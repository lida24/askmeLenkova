jQuery.validator.addMethod("noSpace", function(value, element) {
  return value == '' || value.trim().length != 0;
}, "No space please and don't leave it empty");
jQuery.validator.addMethod("customEmail", function(value, element) {
  return this.optional(element) || /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test(value);
}, "Please enter valid email address!");
$.validator.addMethod("alphanumeric", function(value, element) {
  return this.optional(element) || /^\w+$/i.test(value);
}, "Letters, numbers, and underscores only please");
var $registerForm = $('#register');

if ($registerForm.length) {
  $registerForm.validate({
    rules: {
      login: {
        required: true,
        alphanumeric: true
      },
      email: {
        required: true,
        customEmail: true
      },
      nickname: {
        required: true,
        alphanumeric: true
      },
      password: {
        required: true
      },
      confirm: {
        required: true,
        equalTo: '#password'
      }
    },
    messages: {
      login: {
        required: 'Please enter login!'
      },
      email: {
        required: 'Please enter email!',
        email: 'Please enter valid email!'
      },
      nickname: {
        required: 'Please enter nickname!'
      },
      password: {
        required: 'Please enter password!'
      },
      confirm: {
        required: 'Please enter confirm password!',
        equalTo: 'Please enter same password!'
      }
    },
  });
}

function imgVal(el, lim) {
  var doc = el.parentNode.lastChild;
  if (el.files[0].size <= lim) {
    var file = new FileReader();
    file.onloadend = function(e) {
      var arr = (new Uint8Array(e.target.result)).subarray(0, 4);
      for (var i = 0, l = arr.length, header = ''; i < l; i++)
        header += arr[i].toString(16);
      var type = false;
      switch (header) {
        case '89504e47':
          type = 'PNG';
          break;
        case '47494638':
          type = 'GIF';
          break;
        case 'ffd8ffe0':
        case 'ffd8ffe1':
        case 'ffd8ffe2':
          type = 'JPG';
          break;
      }
      if (type) {
        doc.setAttribute('class', 'good');
        doc.innerHTML = Math.round(el.files[0].size / 1024) + 'kB' + ' ' + type;
      } else {
        el.value = null;
        doc.setAttribute('class', 'bad');
        doc.value = 'Supported image only JPG PNG GIF';
      }
    };
    file.readAsArrayBuffer(el.files[0]);
  } else {
    el.value = null;
    doc.setAttribute('class', 'bad');
    doc.value = 'File size should be less than 10 MB';
  }
}
