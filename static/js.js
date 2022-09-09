
function sendJSON(){
    var email = document.getElementById("email").value;
    var regEmail = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/;
    if (regEmail.test(email) == true){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/add', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        "email" : email
    }));
    document.getElementById("email").value = '';
    }
    else {
        alert("올바른 이메일 주소를 입력해주세요")
    }
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var myArr = JSON.parse(this.responseText);
            const element = document.getElementById("message")
            console.log(myArr);
            element.innerHTML = '<h3><div id = "message" class = "align">' + myArr.message + '</div></h3>';
        }
    };
}
