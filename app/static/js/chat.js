/*
RoomChat V2
Chat JavaScript

Handles:
- WebSocket connection
- Text messages
- Image upload
- Image messages
- Message history
*/


let socket = null;

let messageBox;
let messageInput;
let sendBtn;

let fileInput;
let uploadBtn;



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
        document.getElementById("messageBox");


    messageInput =
        document.getElementById("messageInput");


    sendBtn =
        document.getElementById("sendBtn");


    fileInput =
        document.getElementById("fileInput");


    uploadBtn =
        document.getElementById("uploadBtn");



    const user = getCurrentUser();



    if(!user){

        alert("User not found");

        window.location.href="/";

        return;

    }



    connectSocket(user);


    setupSendButton();


    setupUploadButton();



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
        "Connecting:",
        url
    );



    socket = new WebSocket(url);



    socket.onopen=function(){

        updateStatus(
            "Connected 🟢"
        );

    };



    socket.onmessage=function(event){


        const data =
            JSON.parse(
                event.data
            );


        displayMessage(data);


    };



    socket.onerror=function(){

        updateStatus(
            "Error 🔴"
        );

    };



    socket.onclose=function(){

        updateStatus(
            "Disconnected 🔴"
        );

    };



    loadOldMessages(
        user.room_id
    );

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

        status.innerHTML=text;

    }

}







// =====================================
// TEXT MESSAGE
// =====================================

function setupSendButton(){


    if(!sendBtn){
        return;
    }



    sendBtn.onclick=function(){

        sendMessage();

    };



    messageInput.addEventListener(
    "keypress",
    function(e){

        if(e.key==="Enter"){

            sendMessage();

        }

    });


}




function sendMessage(){



    const text =
        messageInput.value.trim();



    if(
        !text ||
        !socket ||
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
// IMAGE UPLOAD
// =====================================

function setupUploadButton(){



    if(!uploadBtn){
        return;
    }




    uploadBtn.onclick = async function(){



        const file =
            fileInput.files[0];



        if(!file){

            alert(
                "Select file first"
            );

            return;

        }



        const formData =
            new FormData();



        formData.append(
            "file",
            file
        );



        try{


            const response =
            await fetch(
                "/upload/file",
                {

                    method:"POST",

                    body:formData

                }
            );



            const data =
                await response.json();




            if(
                socket &&
                socket.readyState === WebSocket.OPEN
            ){


                socket.send(

                    JSON.stringify({

                        type:"image",

                        url:data.url

                    })

                );


            }



            fileInput.value="";



        }

        catch(error){


            console.log(
                "Upload error:",
                error
            );


        }



    };


}








// =====================================
// OLD MESSAGES
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


        });



    }

    catch(error){

        console.log(error);

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

    else{

        div.classList.add(
            "other-message"
        );

    }






    if(data.type==="image"){


        div.innerHTML=`

        <img
        src="${data.url}"
        width="250"
        style="
        border-radius:12px;
        "
        >

        `;


    }

    else{


        div.innerHTML=`

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


    div.textContent=text;


    return div.innerHTML;


}