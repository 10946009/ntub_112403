function previewAvatar(event) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function () {
        var avatarPreview = document.getElementById('avatar-preview');
        avatarPreview.src = reader.result;
    };
    reader.readAsDataURL(input.files[0]);
}
function password_validation() {
    var password = document.getElementById("passwordInput").value;

    var lowercaseIcon = document.getElementById("lowercaseIcon");
    var uppercaseIcon = document.getElementById("uppercaseIcon");
    var numberIcon = document.getElementById("numberIcon");
    var specialCharIcon = document.getElementById("specialCharIcon");
    var lengthIcon = document.getElementById("lengthIcon");

    lowercaseIcon.classList.toggle("valid", password.match(/[a-z]/g));
    uppercaseIcon.classList.toggle("valid", password.match(/[A-Z]/g));
    numberIcon.classList.toggle("valid", password.match(/[0-9]/g));
    specialCharIcon.classList.toggle("valid", password.match(/[^a-zA-Z\d]/g));
    lengthIcon.classList.toggle("valid", password.length >= 8);
}
function password_validation1() {
    var password = document.getElementById("passwordInput1").value;

    var lowercaseIcon = document.getElementById("lowercaseIcon");
    var uppercaseIcon = document.getElementById("uppercaseIcon");
    var numberIcon = document.getElementById("numberIcon");
    var specialCharIcon = document.getElementById("specialCharIcon");
    var lengthIcon = document.getElementById("lengthIcon");

    lowercaseIcon.classList.toggle("valid", password.match(/[a-z]/g));
    uppercaseIcon.classList.toggle("valid", password.match(/[A-Z]/g));
    numberIcon.classList.toggle("valid", password.match(/[0-9]/g));
    specialCharIcon.classList.toggle("valid", password.match(/[^a-zA-Z\d]/g));
    lengthIcon.classList.toggle("valid", password.length >= 8);
}
const togglePassword = document.getElementById('checkEye');
const passwordField = document.getElementById('passwordInput');

togglePassword.addEventListener('click', function () {
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        togglePassword.classList.remove('fa-eye');
        togglePassword.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        togglePassword.classList.remove('fa-eye-slash');
        togglePassword.classList.add('fa-eye');
    }
});

const togglePassword1 = document.getElementById('checkEye1');
const passwordField1 = document.getElementById('passwordInput1');

togglePassword1.addEventListener('click', function () {
    if (passwordField1.type === 'password') {
        passwordField1.type = 'text';
        togglePassword1.classList.remove('fa-eye');
        togglePassword1.classList.add('fa-eye-slash');
    } else {
        passwordField1.type = 'password';
        togglePassword1.classList.remove('fa-eye-slash');
        togglePassword1.classList.add('fa-eye');
    }
});

const togglePassword2 = document.getElementById('checkEye2');
const passwordField2 = document.getElementById('passwordInput2');

togglePassword2.addEventListener('click', function () {
    if (passwordField2.type === 'password') {
        passwordField2.type = 'text';
        togglePassword2.classList.remove('fa-eye');
        togglePassword2.classList.add('fa-eye-slash');
    } else {
        passwordField2.type = 'password';
        togglePassword2.classList.remove('fa-eye-slash');
        togglePassword2.classList.add('fa-eye');
    }
});


function showPasswordToggle() {
    // var eyeIcon = document.getElementById("checkEye");
    // eyeIcon.style.display = "inline";
    var showval = document.getElementById("validationIcons");
    showval.style.display = "block";
}

function hidePasswordToggle() {
    // var eyeIcon = document.getElementById("checkEye");
    // eyeIcon.style.display = "none";
    var showval = document.getElementById("validationIcons");
    showval.style.display = "none";
}

// function showPasswordToggle1() {
//     var eyeIcon1 = document.getElementById("checkEye1");
//     eyeIcon1.style.display = "inline";
// }

// function hidePasswordToggle1() {
//     var eyeIcon1 = document.getElementById("checkEye1");
//     eyeIcon1.style.display = "none";
// }

// function showPasswordToggle2() {
//     var eyeIcon2 = document.getElementById("checkEye2");
//     eyeIcon2.style.display = "inline";
// }

// function hidePasswordToggle2() {
//     var eyeIcon2 = document.getElementById("checkEye2");
//     eyeIcon2.style.display = "none";
// }