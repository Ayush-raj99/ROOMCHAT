/*
RoomChat V2

Main JavaScript

Handles:
- Home page
- Basic frontend setup
*/


document.addEventListener(

    "DOMContentLoaded",

    function(){



        console.log(

            "RoomChat V2 loaded"

        );



        const rooms = document.querySelectorAll(

            ".room-card"

        );



        console.log(

            "Available rooms:",

            rooms.length

        );



    }

);