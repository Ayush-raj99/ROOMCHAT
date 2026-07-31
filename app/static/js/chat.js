/*
RoomChat V2
Chat JavaScript

Handles:
- WebSocket connection
- Real time messages
- Sending messages
- Receiving messages
*/





let chatSocket = null;



let messageBox =

document.getElementById(

    "messageBox"

);



let messageInput =

document.getElementById(

    "messageInput"

);



let sendBtn =

document.getElementById(

    "sendBtn"

);







// =====================================================
// START CHAT CONNECTION
// =====================================================


if(messageBox){



    let roomId =

    window.location.pathname

    .split("/")

    .pop();




    let user =

    getCurrentUser();





    if(user){



        chatSocket =

        new WebSocket(

            `ws://${window.location.host}/ws/${roomId}/${user.id}`

        );






        chatSocket.onopen = function(){


            let status =

            document.getElementById(

                "roomStatus"

            );



            if(status)

            status.innerHTML =

            "Connected 🟢";


        };






        chatSocket.onmessage = function(event){



            let data =

            JSON.parse(

                event.data

            );



            displayMessage(data);



        };







        chatSocket.onclose = function(){



            let status =

            document.getElementById(

                "roomStatus"

            );



            if(status)

            status.innerHTML =

            "Disconnected 🔴";



        };



    }



}








// =====================================================
// SEND MESSAGE
// =====================================================


if(sendBtn){



sendBtn.addEventListener(

"click",

function(){



    let message =

    messageInput.value.trim();





    if(

        message === "" ||

        chatSocket === null

    )

    return;







    chatSocket.send(

        JSON.stringify({


            content:message


        })

    );





    messageInput.value = "";





}

);



}








// =====================================================
// ENTER BUTTON SEND
// =====================================================


if(messageInput){



messageInput.addEventListener(

"keypress",

function(event){



    if(event.key === "Enter"){


        sendBtn.click();


    }



}

);



}








// =====================================================
// DISPLAY MESSAGE
// =====================================================


function displayMessage(data){



    let div =

    document.createElement(

        "div"

    );




    div.className =

    "message";





    let currentUser =

    getCurrentUser();






    if(

        currentUser &&

        currentUser.id === data.user_id

    ){


        div.classList.add(

            "my-message"

        );


    }






    div.innerHTML =

    `

    <p>

        ${escapeHTML(data.content)}

    </p>


    <span class="message-time">

        just now

    </span>

    `;







    messageBox.appendChild(

        div

    );




    messageBox.scrollTop =

    messageBox.scrollHeight;



}








// =====================================================
// SECURITY
// =====================================================


function escapeHTML(text){



    let div =

    document.createElement(

        "div"

    );



    div.textContent = text;



    return div.innerHTML;



}