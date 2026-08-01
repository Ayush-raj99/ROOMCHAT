/*
RoomChat V2

Upload JavaScript

Handles:
- File upload
- Sending file message through WebSocket
*/



document.addEventListener(

    "DOMContentLoaded",

    function(){



        const uploadBtn = document.getElementById(

            "uploadBtn"

        );



        const fileInput = document.getElementById(

            "fileInput"

        );





        if(

            !uploadBtn ||

            !fileInput

        ){

            return;

        }







        uploadBtn.onclick = async function(){





            const file = fileInput.files[0];





            if(!file){



                alert(

                    "Select a file"

                );


                return;


            }







            const formData = new FormData();





            formData.append(

                "file",

                file

            );







            try{





                const response = await fetch(

                    "/upload/file",

                    {


                        method:"POST",


                        body:formData


                    }

                );







                const data = await response.json();







                if(!response.ok){



                    alert(

                        data.detail ||

                        "Upload failed"

                    );



                    return;


                }







                // Send file message to websocket



                if(window.socket){



                    window.socket.send(

                        JSON.stringify({


                            type:"image",


                            url:data.url


                        })


                    );



                }







                fileInput.value="";






            }



            catch(error){



                console.error(error);



                alert(

                    "Upload error"

                );



            }





        };




    }

);