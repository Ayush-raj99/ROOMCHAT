/*
RoomChat V2
WhatsApp Style Chat JS
*/


let socket = null;

let messageBox;
let messageInput;
let sendBtn;
let fileInput;



// =============================
// GET USER
// =============================

function getCurrentUser(){


    const user =
    localStorage.getItem("user");


    if(!user){

        return null;

    }


    return JSON.parse(user);

}





// =============================
// FORMAT TIME
// =============================

function formatTime(dateString){


    if(!dateString){

        return "";

    }


    const date =
    new Date(dateString);



    // Convert UTC to India time (UTC + 5:30)

    date.setMinutes(
        date.getMinutes() + 330
    );



    return date.toLocaleTimeString(

        [],

        {
            hour:"2-digit",

            minute:"2-digit",

            hour12:false

        }

    );

}





// =============================
// START
// =============================

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


    fileInput =
    document.getElementById(
        "fileInput"
    );



    const user =
    getCurrentUser();



    if(!user){

        window.location.href="/";

        return;

    }



    connectSocket(user);



    sendBtn.onclick =
    sendMessage;



    messageInput.addEventListener(
    "keypress",
    function(e){

        if(e.key==="Enter"){

            sendMessage();

        }

    });



    fileInput.addEventListener(
    "change",
    uploadImage
    );


});






// =============================
// WEBSOCKET
// =============================

function connectSocket(user){


    const protocol =
    location.protocol==="https:"
    ?
    "wss"
    :
    "ws";



    socket =
    new WebSocket(

    `${protocol}://${location.host}/ws/${user.room_id}/${user.id}`

    );



    socket.onopen=function(){

        updateStatus(
            "Online 🟢"
        );

    };



    socket.onmessage=function(event){


        const data =
        JSON.parse(
            event.data
        );


        displayMessage(data);


    };



    socket.onclose=function(){

        updateStatus(
            "Disconnected"
        );

    };



    loadOldMessages(
        user.room_id
    );


}







// =============================
// STATUS
// =============================

function updateStatus(text){


    const status =
    document.getElementById(
        "roomStatus"
    );


    if(status){

        status.innerHTML=text;

    }

}








// =============================
// SEND TEXT
// =============================

function sendMessage(){


    const text =
    messageInput.value.trim();



    if(
        !text ||
        !socket ||
        socket.readyState!==1
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








// =============================
// IMAGE UPLOAD
// =============================

async function uploadImage(){


    const file =
    fileInput.files[0];


    if(!file){

        return;

    }



    const formData =
    new FormData();



    formData.append(
        "file",
        file
    );



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



    socket.send(

        JSON.stringify({

            type:"image",

            url:data.url

        })

    );



    fileInput.value="";


}








// =============================
// OLD MESSAGES
// =============================

async function loadOldMessages(roomId){


    const response =
    await fetch(
        `/chat/${roomId}/messages`
    );



    const messages =
    await response.json();



    messages.forEach(
    msg=>{


        displayMessage({

            id:
            msg.id,


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


            created_at:
            msg.created_at


        });



    });


}









// =============================
// DISPLAY MESSAGE
// =============================

function displayMessage(data){


    const div =
    document.createElement(
        "div"
    );



    div.className =
    "message";



    const user =
    getCurrentUser();





    if(user.id === data.user_id){


        div.classList.add(
            "my-message"
        );


    }
    else{


        div.classList.add(
            "other-message"
        );


    }




    const time =
    formatTime(
        data.created_at
    );





    if(data.type==="image"){


        div.innerHTML = `


        <img

        class="chat-image"

        src="${data.url}"

        onclick="openImageViewer('${data.url}')"

        >



        <div class="message-footer">


        <span class="message-time">
        ${time}
        </span>



        ${
        user.id===data.user_id
        ?
        `
        <span class="message-tick">
        ✓✓
        </span>
        `
        :
        ""
        }



        </div>


        `;



    }
    else{


        div.innerHTML = `


        <span>

        ${escapeHTML(data.content)}

        </span>



        <div class="message-footer">


        <span class="message-time">
        ${time}
        </span>



        ${
        user.id===data.user_id
        ?
        `
        <span class="message-tick">
        ✓✓
        </span>
        `
        :
        ""
        }



        </div>



        `;


    }




    messageBox.appendChild(div);



    messageBox.scrollTop =
    messageBox.scrollHeight;



}








// =============================
// IMAGE VIEWER
// =============================

function openImageViewer(url){


    const viewer =
    document.createElement(
        "div"
    );


    viewer.className =
    "image-viewer";



    viewer.innerHTML = `

    <span class="close-viewer">
    ×
    </span>


    <img src="${url}">


    `;



    document.body.appendChild(
        viewer
    );



    viewer.onclick=function(){

        viewer.remove();

    };


}








// =============================
// SECURITY
// =============================

function escapeHTML(text){


    const div =
    document.createElement(
        "div"
    );


    div.textContent=text;


    return div.innerHTML;


}