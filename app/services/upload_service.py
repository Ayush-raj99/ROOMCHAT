"""
RoomChat V2
Upload Service

Handles:
- Saving uploaded files
- Generating file URLs
"""


import os

import uuid

from fastapi import UploadFile





# =====================================================
# UPLOAD DIRECTORY
# =====================================================


UPLOAD_FOLDER = "app/uploads"



os.makedirs(

    UPLOAD_FOLDER,

    exist_ok=True

)







# =====================================================
# SAVE FILE
# =====================================================


async def save_upload_file(

    file: UploadFile

):


    # Create unique filename

    extension = ""



    if "." in file.filename:

        extension = (

            file.filename

            .split(".")

            [-1]

        )



    filename = (

        str(uuid.uuid4())

        + "."

        + extension

    )





    file_path = os.path.join(

        UPLOAD_FOLDER,

        filename

    )





    # Save file

    with open(

        file_path,

        "wb"

    ) as buffer:


        content = await file.read()



        buffer.write(

            content

        )







    # URL returned to frontend

    file_url = (

        "/uploads/"

        + filename

    )



    return file_url