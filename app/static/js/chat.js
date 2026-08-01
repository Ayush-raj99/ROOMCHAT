/*
RoomChat V2

Chat JavaScript

Features:
- WebSocket chat
- Left/right messages
- WhatsApp style bubbles
- Double tick
- Image messages
- Message history
*/


let socket = null;

let messageBox = null;
let messageInput = null;
let sendBtn = null;



// =====================================
// GET USER
// =====================================

function getCurrentUser(){

    const user =
        localStorage.getItem("user");


    if(!user){
        return null;
    }


    return JSON.parse(user);

}





// =====================================
// START
// =====================================


document.addEventListener(
"DOMContentLoaded",
()=>{


    messageBox =
        document.getElementById(
            "messageBox"
        );


    messageInput =
        document.getElementById(
            "messageInput"
        );


    sendBtn =
        document.getElementById(
            "sendBtn"
        );



    const user =
        getCurrentUser();



    if(!user){

        alert(
            "User not found"
        );

        return;

    }



    connectSocket(user);



});








// =====================================
// WEBSOCKET
// =====================================


function connectSocket(user){



    const protocol =
        window.location.protocol === "https:"
        ? "wss"
        : "ws";



    const url =
    `${protocol}://${window.location.host}/ws/${user.room_id}/${user.id}`;



    console.log(
        "Socket:",
        url
    );



    socket =
        new WebSocket(url);




    socket.onopen = ()=>{


        updateStatus(
            "Connected 🟢"
        );


    };




    socket.onmessage =
    (event)=>{


        const data =
            JSON.parse(
                event.data
            );


        console.log(
            "Received:",
            data
        );


        displayMessage(
            data
        );


    };




    socket.onclose = ()=>{


        updateStatus(
            "Disconnected 🔴"
        );


    };



    socket.onerror =
    (e)=>{

        console.log(
            "Socket error",
            e
        );

    };



    loadOldMessages(
        user.room_id
    );


    setupSend();


}









// =====================================
// STATUS
// =====================================


function updateStatus(text){


    const status =
        document.getElementById(
            "roomStatus"
        );


    if(status){

        status.innerHTML =
            text;

    }

}









// =====================================
// SEND MESSAGE
// =====================================


function setupSend(){



    if(!sendBtn)
        return;



    sendBtn.onclick =
    sendMessage;



    messageInput.addEventListener(
        "keypress",
        (e)=>{

            if(e.key==="Enter"){

                sendMessage();

            }

        }
    );


}







function sendMessage(){



    const text =
        messageInput.value.trim();



    if(
        !text ||
        !socket ||
        socket.readyState !== 1
    ){

        return;

    }



    socket.send(

        JSON.stringify({

            type:"text",

            content:text

        })

    );



    messageInput.value="";



}









// =====================================
// OLD MESSAGES
// =====================================


async function loadOldMessages(roomId){



    try{


        const res =
            await fetch(
                `/chat/${roomId}/messages`
            );


        const messages =
            await res.json();



        messages.forEach(
        (msg)=>{


            displayMessage({

                type:
                    msg.is_image
                    ? "image"
                    : "text",


                user_id:
                    msg.user_id,


                content:
                    msg.content,


                url:
                    msg.file_path

            });



        });



    }
    catch(e){

        console.log(
            "History error",
            e
        );

    }



}









// =====================================
// DISPLAY MESSAGE
// =====================================


function displayMessage(data){



    if(!messageBox)
        return;



    const div =
        document.createElement(
            "div"
        );



    const currentUser =
        getCurrentUser();





    const mine =
        currentUser &&
        Number(currentUser.id)
        ===
        Number(data.user_id);




    if(mine){

        div.className =
            "message my-message";

    }
    else{

        div.className =
            "message other-message";

    }





    if(data.type==="image"){


        div.innerHTML = `

        <img src="${data.url}">

        <span class="tick">
            ✓✓
        </span>

        `;


    }

    else{


        div.innerHTML = `

        <p>
        ${escapeHTML(
            data.content || ""
        )}
        </p>

        <span class="tick">
            ✓✓
        </span>

        `;


    }






    messageBox.appendChild(
        div
    );



    messageBox.scrollTop =
        messageBox.scrollHeight;



}









// =====================================
// SECURITY
// =====================================


function escapeHTML(text){


    const div =
        document.createElement(
            "div"
        );


    div.textContent =
        text;


    return div.innerHTML;


}