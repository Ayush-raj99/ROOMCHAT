/*
RoomChat V2
Main JavaScript

Handles:
- Common functions
- Local storage
- Navigation helpers
- User session
*/





// =====================================================
// GET CURRENT USER
// =====================================================

function getCurrentUser(){


    return JSON.parse(

        localStorage.getItem("user")

    );


}





// =====================================================
// SAVE USER
// =====================================================

function saveUser(user){


    localStorage.setItem(

        "user",

        JSON.stringify(user)

    );


}





// =====================================================
// REMOVE USER
// =====================================================

function logout(){


    localStorage.removeItem(

        "user"

    );


    window.location.href = "/";

}





// =====================================================
// CHECK LOGIN
// =====================================================

function isLoggedIn(){


    return localStorage.getItem(

        "user"

    ) !== null;


}





// =====================================================
// API HELPER
// =====================================================

async function apiRequest(

    url,

    method = "GET",

    data = null

){


    let options = {


        method: method,


        headers:{}


    };



    if(data){


        options.headers[

            "Content-Type"

        ] =

        "application/json";



        options.body =

        JSON.stringify(data);


    }





    let response = await fetch(

        url,

        options

    );



    return await response.json();

}





// =====================================================
// SHOW MESSAGE
// =====================================================

function showAlert(

    message,

    type="success"

){


    let alertBox =

    document.createElement(

        "div"

    );



    alertBox.className =

    "alert " + type;



    alertBox.innerHTML =

    message;



    document.body.prepend(

        alertBox

    );



    setTimeout(

        ()=>{


            alertBox.remove();


        },

        3000

    );


}





// =====================================================
// DARK MODE READY
// =====================================================

function toggleTheme(){


    document.body.classList.toggle(

        "light-mode"

    );


}





console.log(

    "RoomChat frontend loaded"

);