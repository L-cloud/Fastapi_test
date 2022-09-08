
function sendJSON(){
    var email = document.getElementById("email").value;
    var regEmail = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/;
    if (regEmail.test(email) == true){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        "email" : email
    }));
    document.getElementById("email").value = '';}
    else {
        alert("올바른 이메일 주소를 입력해주세요")
    }
}

