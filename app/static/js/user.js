/*
RoomChat V2
User JavaScript

Handles:
- User creation
- Login form
- Saving user data
*/





// =====================================================
// LOGIN / CREATE USER
// =====================================================


const loginForm =

document.getElementById(

    "loginForm"

);





if(loginForm){


    loginForm.addEventListener(

        "submit",

        async function(event){



            event.preventDefault();





            let username =

            document.getElementById(

                "username"

            ).value;





            let displayName =

            document.getElementById(

                "displayName"

            ).value;





            let profilePicture =

            document.getElementById(

                "profilePicture"

            ).value;







            try{


                let response =

                await fetch(

                    "/users/",

                    {


                        method:"POST",


                        headers:{


                            "Content-Type":

                            "application/json"


                        },


                        body:JSON.stringify({


                            username:


                            username,


                            display_name:


                            displayName || username,


                            profile_picture:


                            profilePicture || null


                        })

                    }

                );





                let user =

                await response.json();







                if(user.id){



                    saveUser(user);





                    showAlert(

                        "Login successful"

                    );





                    setTimeout(

                        ()=>{


                            window.location.href =

                            "/join-room";


                        },

                        1000

                    );



                }



            }

            catch(error){


                console.log(error);


                showAlert(

                    "Something went wrong",

                    "error"

                );


            }



        }

    );

}