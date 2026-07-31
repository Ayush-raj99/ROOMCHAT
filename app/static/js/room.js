/*
RoomChat V2
Room JavaScript

Handles:
- Create room
- Join room
- Room password verification
*/





// =====================================================
// CREATE ROOM
// =====================================================


const createRoomForm =

document.getElementById(

    "createRoomForm"

);





if(createRoomForm){


    createRoomForm.addEventListener(

        "submit",

        async function(event){


            event.preventDefault();





            let roomName =

            document.getElementById(

                "roomName"

            ).value;





            let password =

            document.getElementById(

                "roomPassword"

            ).value;






            try{


                let response =

                await fetch(

                    "/rooms/",

                    {


                        method:"POST",


                        headers:{


                            "Content-Type":

                            "application/json"


                        },


                        body:JSON.stringify({


                            name:roomName,


                            password:password


                        })


                    }

                );





                let room =

                await response.json();







                if(room.id){



                    showAlert(

                        "Room created"

                    );





                    setTimeout(

                        ()=>{


                            window.location.href =

                            "/chat/" + room.id;



                        },

                        1000

                    );

                }



            }


            catch(error){


                console.log(error);


                showAlert(

                    "Room creation failed",

                    "error"

                );


            }



        }

    );

}


// =====================================================
// JOIN ROOM
// =====================================================


const joinRoomForm =

document.getElementById(

    "joinRoomForm"

);





if(joinRoomForm){


    joinRoomForm.addEventListener(

        "submit",

        async function(event){


            event.preventDefault();





            let roomId =

            document.getElementById(

                "roomId"

            ).value;





            let password =

            document.getElementById(

                "roomPassword"

            ).value;





            let username =

            document.getElementById(

                "joinUsername"

            ).value;







            try{


                let response =

                await fetch(

                    "/rooms/join",

                    {


                        method:"POST",


                        headers:{


                            "Content-Type":

                            "application/json"


                        },


                        body:JSON.stringify({


                            room_id:

                            Number(roomId),


                            password:


                            password,


                            username:


                            username


                        })

                    }

                );






                let result =

                await response.json();







                if(response.ok){



                    showAlert(

                        "Entering room..."

                    );





                    setTimeout(

                        ()=>{


                            window.location.href =

                            "/chat/" + roomId;



                        },

                        800

                    );



                }



                else{


                    showAlert(

                        result.detail ||

                        "Wrong password",

                        "error"

                    );


                }



            }


            catch(error){


                console.log(error);


                showAlert(

                    "Connection error",

                    "error"

                );


            }




        }

    );

}