
// vistas
function showRegister(){
    document.getElementById("loginCard").style.display="none";
    document.getElementById("registerCard").style.display="block";
}

function showLogin(){
    document.getElementById("registerCard").style.display="none";
    document.getElementById("loginCard").style.display="block";
}

/* REGISTRO */
function register(){
    let name = document.getElementById("regName").value;
    let email = document.getElementById("regEmail").value;
    let pass = document.getElementById("regPass").value;

    let user = {
        name,
        email,
        password: pass,
        frauds: 0,
        assignedTests: [],
        prevTests: []
    };

    localStorage.setItem(email, JSON.stringify(user));

    document.getElementById("registerMsg").textContent = "Cuenta creada";
}

/* LOGIN */
function login(){
    let user = document.getElementById("loginUser").value.trim();
    let pass = document.getElementById("loginPass").value.trim();

    // ADMIN
    if(user.toUpperCase()==="ADMIN" && pass==="admin123"){
        localStorage.setItem("role","admin");
        window.location.href="admin.html";
        return;
    }

    // USER
    let data = JSON.parse(localStorage.getItem(user));

    if(!data || data.password!==pass){
        document.getElementById("loginMsg").textContent="Error login";
        return;
    }

    localStorage.setItem("activeUser",JSON.stringify(data));
    localStorage.setItem("role","user");

    window.location.href="dashboard.html";
}