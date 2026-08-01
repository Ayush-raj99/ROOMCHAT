/*
RoomChat V2

Admin JavaScript

Handles:
- Create users
- Create rooms
- Assign users
- Change passwords
- Delete rooms
- Load dashboard data
*/


document.addEventListener(
    "DOMContentLoaded",
    function(){


        loadUsers();

        loadRooms();



        // ===============================
        // CREATE USER
        // ===============================

        const createUserBtn =
            document.getElementById("createUserBtn");


        if(createUserBtn){

            createUserBtn.onclick = async function(){


                const username =
                    document.getElementById(
                        "newUsername"
                    ).value;


                const password =
                    document.getElementById(
                        "newUserPassword"
                    ).value;



                const response = await fetch(
                    "/admin/users",
                    {

                        method:"POST",

                        headers:{
                            "Content-Type":
                            "application/json"
                        },


                        body:JSON.stringify({

                            username:username,

                            password:password

                        })

                    }
                );



                const data = await response.json();


                alert(
                    data.message ||
                    data.detail
                );


                loadUsers();

            }

        }





        // ===============================
        // CREATE ROOM
        // ===============================


        const createRoomBtn =
            document.getElementById("createRoomBtn");


        if(createRoomBtn){


            createRoomBtn.onclick = async function(){


                const name =
                    document.getElementById(
                        "newRoomName"
                    ).value;



                const password =
                    document.getElementById(
                        "newRoomPassword"
                    ).value;



                const response = await fetch(
                    "/admin/rooms",
                    {


                        method:"POST",


                        headers:{
                            "Content-Type":
                            "application/json"
                        },


                        body:JSON.stringify({

                            name:name,

                            password:password

                        })


                    }
                );



                const data =
                    await response.json();



                alert(
                    data.message ||
                    data.detail
                );



                loadRooms();


            }

        }





        // ===============================
        // ASSIGN USER TO ROOM
        // ===============================


        const assignBtn =
            document.getElementById(
                "assignBtn"
            );



        if(assignBtn){


            assignBtn.onclick = async function(){



                const user_id =
                    Number(
                        document.getElementById(
                            "assignUserId"
                        ).value
                    );



                const room_id =
                    Number(
                        document.getElementById(
                            "assignRoomId"
                        ).value
                    );




                const response =
                    await fetch(
                        "/admin/assign-room",
                        {


                            method:"POST",


                            headers:{
                                "Content-Type":
                                "application/json"
                            },


                            body:JSON.stringify({

                                user_id:user_id,

                                room_id:room_id

                            })


                        }
                    );



                const data =
                    await response.json();



                alert(
                    data.message ||
                    data.detail
                );


            }


        }





        // ===============================
        // CHANGE PASSWORD
        // ===============================


        const changePasswordBtn =
            document.getElementById(
                "changePasswordBtn"
            );



        if(changePasswordBtn){


            changePasswordBtn.onclick =
            async function(){



                const room_id =
                    Number(
                        document.getElementById(
                            "changeRoomId"
                        ).value
                    );



                const password =
                    document.getElementById(
                        "changePassword"
                    ).value;



                const response =
                    await fetch(
                        "/admin/rooms/password",
                        {


                            method:"POST",


                            headers:{
                                "Content-Type":
                                "application/json"
                            },


                            body:JSON.stringify({

                                room_id:room_id,

                                password:password

                            })


                        }
                    );



                const data =
                    await response.json();



                alert(
                    data.message ||
                    data.detail
                );


            }


        }





        // ===============================
        // DELETE ROOM
        // ===============================


        const deleteRoomBtn =
            document.getElementById(
                "deleteRoomBtn"
            );



        if(deleteRoomBtn){


            deleteRoomBtn.onclick =
            async function(){



                const room_id =
                    Number(
                        document.getElementById(
                            "deleteRoomId"
                        ).value
                    );



                const response =
                    await fetch(
                        `/admin/rooms/${room_id}`,
                        {


                            method:"DELETE"


                        }
                    );



                const data =
                    await response.json();



                alert(
                    data.message ||
                    data.detail
                );



                loadRooms();


            }


        }



    }

);







// =====================================
// LOAD USERS
// =====================================


async function loadUsers(){


    const select =
        document.getElementById(
            "assignUserId"
        );


    if(!select){

        return;

    }



    const response =
        await fetch(
            "/admin/users"
        );



    const users =
        await response.json();



    select.innerHTML =
        `
        <option value="">
            Select User
        </option>
        `;



    users.forEach(
        function(user){


            select.innerHTML +=
            `
            <option value="${user.id}">
                ${user.username}
            </option>
            `;


        }

    );


}









// =====================================
// LOAD ROOMS
// =====================================


async function loadRooms(){



    const response =
        await fetch(
            "/admin/rooms"
        );



    const rooms =
        await response.json();




    const selects = [

        "assignRoomId",

        "changeRoomId",

        "deleteRoomId"

    ];



    selects.forEach(

        function(id){



            const select =
                document.getElementById(id);



            if(!select){

                return;

            }



            select.innerHTML =
            `
            <option value="">
                Select Room
            </option>
            `;



            rooms.forEach(

                function(room){


                    select.innerHTML +=
                    `
                    <option value="${room.id}">
                        ${room.name}
                    </option>
                    `;


                }

            );



        }

    );



}