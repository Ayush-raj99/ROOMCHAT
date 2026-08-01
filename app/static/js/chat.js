/*
RoomChat V2

Chat JavaScript

Features:
- WebSocket chat
- Left/right message bubbles
- WhatsApp style ticks
- Image messages
- Message history
*/


let socket = null;

let messageBox;
let messageInput;
let sendBtn;




// =====================================
// GET CURRENT USER
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
// START CHAT
// =====================================

document.addEventListener(
"DOMContentLoaded",
function(){



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


        window.location.href="/";


        return;

    }




    connectSocket(user);



});









// =====================================
// CONNECT WEBSOCKET
// =====================================


function connectSocket(user){



    const roomId =
        user.room_id;




    const protocol =
        window.location.protocol === "https:"
        ?
        "wss"
        :
        "ws";





    const url =
    `${protocol}://${window.location.host}/ws/${roomId}/${user.id}`;





    console.log(
        "Connecting:",
        url
    );





    socket =
        new WebSocket(url);






    socket.onopen =
    function(){


        updateStatus(
            "Connected 🟢"
        );


    };







    socket.onmessage =
    function(event){



        const data =
            JSON.parse(
                event.data
            );



        displayMessage(data);



    };







    socket.onerror =
    function(error){


        console.log(
            "Socket error",
            error
        );


        updateStatus(
            "Error 🔴"
        );


    };







    socket.onclose =
    function(){


        updateStatus(
            "Disconnected 🔴"
        );


    };





    loadOldMessages(roomId);


    setupSendButton();



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
// SEND BUTTON
// =====================================


function setupSendButton(){



    if(!sendBtn){

        return;

    }




    sendBtn.onclick =
    function(){

        sendMessage();

    };






    messageInput.addEventListener(
    "keypress",
    function(event){



        if(event.key==="Enter"){


            sendMessage();


        }



    });



}









// =====================================
// SEND MESSAGE
// =====================================


function sendMessage(){



    const text =
        messageInput.value.trim();





    if(
        text === "" ||
        socket === null ||
        socket.readyState !== WebSocket.OPEN
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
// LOAD OLD MESSAGES
// =====================================


async function loadOldMessages(roomId){



    try{


        const response =
            await fetch(
                `/chat/${roomId}/messages`
            );



        const messages =
            await response.json();





        messages.forEach(
        function(message){



            displayMessage({


                type:
                message.is_image
                ?
                "image"
                :
                "text",



                user_id:
                message.user_id,



                content:
                message.content,



                url:
                message.file_path



            });



        });



    }

    catch(error){


        console.log(
            "History error",
            error
        );


    }



}









// =====================================
// DISPLAY MESSAGE
// =====================================


function displayMessage(data){



    if(!messageBox){

        return;

    }




    const div =
        document.createElement(
            "div"
        );





    const user =
        getCurrentUser();




    const mine =
        user &&
        user.id === data.user_id;







    div.className =
        "message";






    if(mine){


        div.classList.add(
            "my-message"
        );


    }
    else{


        div.classList.add(
            "other-message"
        );


    }









    let body="";





    if(data.type==="image"){



        body = `


        <img

        src="${data.url}"

        class="chat-image"

        >



        `;


    }

    else{



        body = `


        <span class="message-text">

        ${escapeHTML(
            data.content || ""
        )}


        </span>



        `;



    }








    div.innerHTML =


    body +


    (

        mine

        ?

        `

        <span class="ticks">

        ✓✓

        </span>

        `

        :

        ""

    );








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