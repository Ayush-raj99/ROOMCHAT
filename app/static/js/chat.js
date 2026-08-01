/*
RoomChat V2

Chat JavaScript

Features:
- WebSocket chat
- Left/right message alignment
- Message history
- Image messages
*/


let socket = null;

let messageBox;
let messageInput;
let sendBtn;



// ===============================
// GET USER
// ===============================

function getCurrentUser(){

    const user =
        localStorage.getItem("user");


    if(!user){

        return null;

    }


    return JSON.parse(user);

}





// ===============================
// START
// ===============================

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

        return;

    }



    connectSocket(user);


    loadOldMessages(
        user.room_id
    );


    setupSendButton();


});







// ===============================
// WEBSOCKET
// ===============================

function connectSocket(user){



    const protocol =
        window.location.protocol === "https:"
        ?
        "wss"
        :
        "ws";



    const url =
    `${protocol}://${window.location.host}/ws/${user.room_id}/${user.id}`;



    console.log(
        "Connecting:",
        url
    );



    socket =
        new WebSocket(url);





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

            console.log("RECEIVED MESSAGE:", data);

            


        displayMessage(data);


    };





    socket.onclose=function(){

        updateStatus(
            "Disconnected 🔴"
        );

    };





    socket.onerror=function(){

        updateStatus(
            "Error 🔴"
        );

    };



}







// ===============================
// STATUS
// ===============================


function updateStatus(text){


    const status =
        document.getElementById(
            "roomStatus"
        );


    if(status){

        status.innerText=text;

    }


}







// ===============================
// SEND BUTTON
// ===============================


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







// ===============================
// SEND MESSAGE
// ===============================


function sendMessage(){



    const text =
        messageInput.value.trim();



    if(
        text===""
        ||
        !socket
        ||
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









// ===============================
// LOAD HISTORY
// ===============================


async function loadOldMessages(roomId){


try{


const response =
await fetch(
`/chat/${roomId}/messages`
);



const messages =
await response.json();



messages.forEach(
message=>{


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

console.log(error);

}


}










// ===============================
// DISPLAY MESSAGE
// ===============================


function displayMessage(data){



const currentUser =
getCurrentUser();



if(!currentUser){

return;

}



const box =
document.createElement(
"div"
);



const myMessage =
Number(currentUser.id)
===
Number(data.user_id);





box.className =
"message " +
(
myMessage
?
"my-message"
:
"other-message"
);






if(data.type==="image"){



box.innerHTML=`

<img 
src="${data.url}"
class="chat-image"
>

${

myMessage

?

`<span class="ticks">
✓✓
</span>`

:

""

}

`;



}

else{



box.innerHTML=`

<span>
${escapeHTML(
data.content || ""
)}
</span>


${

myMessage

?

`<span class="ticks">
✓✓
</span>`

:

""

}


`;



}




messageBox.appendChild(box);



messageBox.scrollTop =
messageBox.scrollHeight;



}








// ===============================
// SECURITY
// ===============================


function escapeHTML(text){


const div =
document.createElement(
"div"
);


div.textContent=text;


return div.innerHTML;


}