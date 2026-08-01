"""
RoomChat V2
Upload Routes

Handles:
- Image upload
- File upload
- Saving files
"""


import os
import shutil
import uuid


from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException



# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(

    prefix="/upload",

    tags=["Upload"]

)





# ==========================================================
# UPLOAD DIRECTORY
# ==========================================================

UPLOAD_FOLDER = "app/uploads"



# Create folder if missing

os.makedirs(

    UPLOAD_FOLDER,

    exist_ok=True

)





# ==========================================================
# UPLOAD FILE
# ==========================================================

@router.post("/file")

async def upload_file(

    file: UploadFile = File(...)

):


    try:



        extension = ""



        if "." in file.filename:


            extension = file.filename.split(".")[-1]



        filename = (

            str(uuid.uuid4())

            +

            "."

            +

            extension

        )



        filepath = os.path.join(

            UPLOAD_FOLDER,

            filename

        )





        with open(

            filepath,

            "wb"

        ) as buffer:



            shutil.copyfileobj(

                file.file,

                buffer

            )






        return {


            "message":"Upload successful",


            "filename":filename,


            "url":"/uploads/" + filename


        }






    except Exception as e:



        raise HTTPException(

            status_code=500,

            detail=str(e)

        )