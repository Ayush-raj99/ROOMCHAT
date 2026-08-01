/*
RoomChat V2

Room JavaScript

Handles:
- Joining rooms
- Saving current user
- Redirecting to chat
*/


document.addEventListener(

    "DOMContentLoaded",

    function(){



        const form = document.getElementById(

            "joinRoomForm"

        );



        if(!form){

            return;

        }





        form.addEventListener(

            "submit",

            async function(event){



                event.preventDefault();





                const roomId = document.getElementById(

                    "roomId"

                ).value;





                const username = document.getElementById(

                    "username"

                ).value.trim();





                const password = document.getElementById(

                    "roomPassword"

                ).value;





                if(

                    username === "" ||

                    password === ""

                ){

                    alert(

                        "Enter all details"

                    );

                    return;

                }





                try{



                    const response = await fetch(

                        "/rooms/join",

                        {


                            method:"POST",


                            headers:{


                                "Content-Type":

                                "application/json"


                            },


                            body:JSON.stringify({


                                room_id:Number(roomId),


                                username:username,


                                password:password


                            })

                        }

                    );







                    const data = await response.json();







                    if(!response.ok){



                        alert(

                            data.detail || "Join failed"

                        );


                        return;

                    }







                    const user = {


                        id:data.user_id,


                        username:data.username,


                        room_id:data.room_id


                    };







                    localStorage.setItem(

                        "user",

                        JSON.stringify(user)

                    );







                    window.location.href =

                    `/chat/${data.room_id}`;





                }

                catch(error){



                    console.error(error);



                    alert(

                        "Server error"

                    );



                }





            }

        );



    }

);