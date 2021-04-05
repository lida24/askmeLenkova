
var user = document.getElementById('user')
var password = document.getElementById('password')

var user_error = document.getElementById('user_error');
var pass_error = document.getElementById('pass_error');

user.addEventListener('textInput', user_Verify);
password.addEventListener('textInput', pass_Verify);

function validated(){
	if (user.value === '' || user.value == null) {
		user.style.border = "1px solid red";
		user_error.style.display = "block";
		user.focus();
		return false;
	}
	if (password.value.length < 6 || password.value === '' || password.value == null) {
		password.style.border = "1px solid red";
		pass_error.style.display = "block";
		password.focus();
		return false;
	}
}
function user_Verify(){
	if (user.value.length >= 0) {
		user.style.border = "1px solid silver";
		user_error.style.display = "none";
		return true;
	}
}
function pass_Verify(){
	if (password.value.length >= 6) {
		password.style.border = "1px solid silver";
		pass_error.style.display = "none";
		return true;
	}
}
