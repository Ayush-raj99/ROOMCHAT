/*
RoomChat V2

Chat JavaScript

Handles:
- Secure WebSocket connection
- Sending messages
- Receiving messages
- Loading history
- Image messages
*/


let socket = null;

let messageBox;
let messageInput;
let sendBtn;



// =====================================
// GET USER
// =====================================

function getCurrentUser(){

    const user = localStorage.getItem("user");

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



        const user = getCurrentUser();



        if(!user){

            alert(
                "User not found"
            );

            window.location.href="/";

            return;

        }



        connectSocket(user);



    }
);





// =====================================
// CONNECT WEBSOCKET
// =====================================

function connectSocket(user){



    const roomId = user.room_id;



    const protocol =
        window.location.protocol === "https:"
        ? "wss"
        : "ws";



    const websocketURL =
        `${protocol}://${window.location.host}/ws/${roomId}/${user.id}`;



    console.log(
        "Connecting:",
        websocketURL
    );



    socket = new WebSocket(
        websocketURL
    );




    socket.onopen = function(){


        console.log(
            "WebSocket Connected"
        );


        updateStatus(
            "Connected 🟢"
        );


    };





    socket.onmessage = function(event){


        const data =
            JSON.parse(
                event.data
            );


        displayMessage(
            data
        );


    };






    socket.onerror = function(error){


        console.log(
            "WebSocket Error",
            error
        );


        updateStatus(
            "Error 🔴"
        );


    };







    socket.onclose = function(){


        console.log(
            "WebSocket Closed"
        );


        updateStatus(
            "Disconnected 🔴"
        );


    };




    loadOldMessages(
        roomId
    );


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


            if(event.key === "Enter"){

                sendMessage();

            }

        }

    );



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

        console.log(
            "Socket not connected"
        );

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



                if(message.is_image){


                    displayMessage({

                        type:"image",

                        user_id:
                            message.user_id,

                        url:
                            message.file_path

                    });


                }
                else{


                    displayMessage({

                        type:"text",

                        user_id:
                            message.user_id,

                        content:
                            message.content

                    });


                }



            }

        );



    }

    catch(error){


        console.log(
            "History error:",
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



    div.className =
        "message";




    const user =
        getCurrentUser();




    if(
        user &&
        user.id === data.user_id
    ){

        div.classList.add(
            "my-message"
        );

    }







    if(data.type === "image"){


        div.innerHTML = `

            <img 
            src="${data.url}"
            width="250"
            style="
            border-radius:10px;
            "
            >

        `;


    }

    else{


        div.innerHTML = `

            <p>
            ${escapeHTML(
                data.content || ""
            )}
            </p>

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