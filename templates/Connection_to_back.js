function signUp() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const user = {
        name: name,
        email: email,
        password: password
    };
    console.log(user)
    const data = JSON.stringify(user);
    const jsonhttp = new XMLHttpRequest();
    const url = "http://localhost:5000/register";
    jsonhttp.open("POST", url, true);
    jsonhttp.setRequestHeader("Content-Type", "application/json");
    jsonhttp.onreadystatechange = function () {
        alert(jsonhttp.status)
        if (this.status === 200) {
            alert("User created");

        }
        else {
            alert("Smth ERROR");
        }
    }

    jsonhttp.send(data);
}

function signIn() {
    const name = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    let jsonhttp = new XMLHttpRequest();
    const url = "http://localhost:5000/login";
    jsonhttp.open("GET", url, true);
    jsonhttp.setRequestHeader("Authorization", "Basic " + btoa(name+':'+password));
    jsonhttp.onreadystatechange = function () {
        if (jsonhttp.status === 200) {
            alert("You're logged in!");
            location.href = "home.html";
        } else if (jsonhttp.status >= 400) {
            alert("An error >=400")
        } else {
            alert("Smth ERROR");
        }
    }

    jsonhttp.send()
}

function createAuditorium() {
    const name = document.getElementById('name').value;
    const description = document.getElementById('description').value;

    let auditorium = {
        name: name,
        description: description
    };
    console.log(auditorium)
    let jsonhttp = new XMLHttpRequest();
    const url = "http://localhost:5000/auditorium/create";
    jsonhttp.open("POST", url, true);
    jsonhttp.setRequestHeader("Content-Type", "application/json");
    jsonhttp.onreadystatechange = function () {
        if (jsonhttp.status === 200) {
            alert("Auditorium registered");
            location.href = "profile.html";
        } else if (jsonhttp.status >= 400) {
            alert("An error >=400")
        } else {
            alert("Smth ERROR");
        }
    }
    let data = JSON.stringify(auditorium);
    jsonhttp.send(data);
}