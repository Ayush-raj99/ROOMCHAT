/*
RoomChat V2
Upload JavaScript

Handles:
- Image upload
- File upload
- Attachment sending
*/





let uploadButton =

document.getElementById(

    "uploadBtn"

);



let fileInput =

document.getElementById(

    "fileInput"

);







// =====================================================
// OPEN FILE SELECTOR
// =====================================================


if(uploadButton){


    uploadButton.addEventListener(

        "click",

        function(){


            fileInput.click();


        }

    );

}








// =====================================================
// UPLOAD FILE
// =====================================================


if(fileInput){



fileInput.addEventListener(

"change",

async function(){



    let file =

    fileInput.files[0];





    if(!file)

    return;







    let formData =

    new FormData();





    formData.append(

        "file",

        file

    );







    try{



        let response =

        await fetch(

            "/upload",

            {


                method:"POST",


                body:formData


            }

        );








        let result =

        await response.json();







        if(result.url){



            sendAttachment(

                result.url,

                file.type

            );



        }





    }

    catch(error){



        console.log(error);



        showAlert(

            "Upload failed",

            "error"

        );



    }




}

);



}









// =====================================================
// SEND ATTACHMENT MESSAGE
// =====================================================


function sendAttachment(

    url,

    type

){



    if(

        typeof chatSocket ===

        "undefined" ||

        chatSocket === null

    )

    return;







    chatSocket.send(

        JSON.stringify({



            content:

            url,



            attachment_type:

            type



        })

    );



}