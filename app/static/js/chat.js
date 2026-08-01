/*
RoomChat V2
WhatsApp Style Chat JS
*/


let socket = null;

let messageBox;
let messageInput;
let sendBtn;



function getCurrentUser(){

    const user = localStorage.getItem("user");

    if(!user){
        return null;
    }

    return JSON.parse(user);

}





document.addEventListener(
"DOMContentLoaded",
()=>{


    messageBox =
    document.getElementById("messageBox");


    messageInput =
    document.getElementById("messageInput");


    sendBtn =
    document.getElementById("sendBtn");



    const user = getCurrentUser();


    if(!user){

        alert("Login first");
        return;

    }


    connectSocket(user);



});







function connectSocket(user){


    const protocol =
    window.location.protocol==="https:"
    ?"wss"
    :"ws";


    const url =
    `${protocol}://${window.location.host}/ws/${user.room_id}/${user.id}`;



    socket = new WebSocket(url);



    socket.onopen=()=>{

        updateStatus(
        "Connected 🟢"
        );

    };



    socket.onmessage=(event)=>{


        const data =
        JSON.parse(event.data);



        displayMessage(data);


    };



    socket.onclose=()=>{


        updateStatus(
        "Disconnected 🔴"
        );


    };



    loadOldMessages(
    user.room_id
    );


    setupSendButton();



}







function updateStatus(text){

    const status =
    document.getElementById(
    "roomStatus"
    );


    if(status){

        status.innerHTML=text;

    }

}







function setupSendButton(){


    sendBtn.onclick=()=>{

        sendMessage();

    };



    messageInput.addEventListener(
    "keypress",
    e=>{

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
    socket.readyState!==WebSocket.OPEN
    ){

        return;

    }




    socket.send(
    JSON.stringify({

        type:"text",

        content:text


    }));



    messageInput.value="";


}









async function loadOldMessages(roomId){


    const response =
    await fetch(
    `/chat/${roomId}/messages`
    );


    const messages =
    await response.json();



    messages.forEach(msg=>{


        displayMessage({

            type:
            msg.is_image
            ?
            "image"
            :
            "text",


            user_id:
            msg.user_id,


            content:
            msg.content,


            url:
            msg.file_path,


            message_id:
            msg.id,


            status:
            "seen"

        });


    });



}

function displayMessage(data){


    if(!messageBox){
        return;
    }



    const user =
    getCurrentUser();



    const div =
    document.createElement("div");



    div.classList.add(
        "message"
    );



    // My message = right side

    if(
        user &&
        user.id === data.user_id
    ){

        div.classList.add(
            "my-message"
        );


    }

    // Other person's message = left side

    else{

        div.classList.add(
            "other-message"
        );

    }





    let content = "";



    if(data.type === "image"){


        content = `

        <img 
        src="${data.url}"
        class="chat-image"
        >

        `;


    }

    else{


        content = `

        <span>
        ${escapeHTML(
            data.content || ""
        )}
        </span>

        `;


    }





    div.innerHTML = `

        <div class="message-content">

            ${content}

            ${
            user &&
            user.id === data.user_id
            ?
            `
            <span class="ticks">
            ✓✓
            </span>
            `
            :
            ""
            }

        </div>

    `;



    messageBox.appendChild(
        div
    );



    messageBox.scrollTop =
    messageBox.scrollHeight;



}


function escapeHTML(text){


    const div =
    document.createElement("div");


    div.textContent=text;


    return div.innerHTML;


}