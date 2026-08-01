/*
RoomChat V2

Admin JavaScript

Handles:
- Admin login
- User creation
- Room creation
- Room management
*/



// ==================================================
// ADMIN LOGIN
// ==================================================


const loginForm = document.getElementById(

    "adminLoginForm"

);



if(loginForm){



loginForm.addEventListener(

"submit",

async function(event){



event.preventDefault();





const password = document.getElementById(

    "adminPassword"

).value;





const response = await fetch(

    "/admin/login",

    {


        method:"POST",


        headers:{


            "Content-Type":

            "application/json"


        },


        body:JSON.stringify({


            username:"admin",


            password:password


        })


    }

);





const data = await response.json();





if(response.ok){



    localStorage.setItem(

        "admin",

        "true"

    );



    window.location.href="/admin/dashboard";



}

else{


    alert(

        data.detail || "Login failed"

    );


}



}

);



}









// ==================================================
// CREATE USER
// ==================================================


const createUserBtn=document.getElementById(

    "createUserBtn"

);



if(createUserBtn){



createUserBtn.onclick=async function(){



const username=document.getElementById(

    "newUsername"

).value;



const password=document.getElementById(

    "newUserPassword"

).value;





await fetch(

"/admin/users",

{


method:"POST",


headers:{


"Content-Type":

"application/json"


},


body:JSON.stringify({


username:username,


password:password


})


}

);





alert(

"User created"

);



};



}









// ==================================================
// CREATE ROOM
// ==================================================


const createRoomBtn=document.getElementById(

    "createRoomBtn"

);



if(createRoomBtn){



createRoomBtn.onclick=async function(){



const name=document.getElementById(

    "newRoomName"

).value;



const password=document.getElementById(

    "newRoomPassword"

).value;





await fetch(

"/admin/rooms",

{


method:"POST",


headers:{


"Content-Type":

"application/json"


},


body:JSON.stringify({


name:name,


password:password


})


}

);





alert(

"Room created"

);



};



}









// ==================================================
// ASSIGN USER
// ==================================================


const assignBtn=document.getElementById(

    "assignBtn"

);



if(assignBtn){



assignBtn.onclick=async function(){



const user_id=document.getElementById(

    "assignUserId"

).value;



const room_id=document.getElementById(

    "assignRoomId"

).value;





await fetch(

"/admin/assign",

{


method:"POST",


headers:{


"Content-Type":

"application/json"


},


body:JSON.stringify({


user_id:Number(user_id),


room_id:Number(room_id)


})


}

);





alert(

"User assigned"

);



};



}









// ==================================================
// CHANGE ROOM PASSWORD
// ==================================================


const changePasswordBtn=document.getElementById(

    "changePasswordBtn"

);



if(changePasswordBtn){



changePasswordBtn.onclick=async function(){



const room_id=document.getElementById(

    "changeRoomId"

).value;



const password=document.getElementById(

    "changePassword"

).value;





await fetch(

"/admin/rooms/password",

{


method:"PUT",


headers:{


"Content-Type":

"application/json"


},


body:JSON.stringify({


room_id:Number(room_id),


password:password


})


}

);





alert(

"Password changed"

);



};



}









// ==================================================
// DELETE ROOM
// ==================================================


const deleteRoomBtn=document.getElementById(

    "deleteRoomBtn"

);



if(deleteRoomBtn){



deleteRoomBtn.onclick=async function(){



const room_id=document.getElementById(

    "deleteRoomId"

).value;





await fetch(

`/admin/rooms/${room_id}`,

{


method:"DELETE"


}

);





alert(

"Room deleted"

);



};



}