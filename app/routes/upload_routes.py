"""
RoomChat V2
Upload Routes
"""

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from fastapi.responses import JSONResponse


from app.services.upload_service import save_upload_file





router = APIRouter(

    prefix="/upload",

    tags=["Upload"]

)







# ==========================================================
# UPLOAD FILE
# ==========================================================


@router.post("/")

async def upload_file(

    file: UploadFile = File(...)

):


    try:


        file_url = await save_upload_file(

            file

        )



        return JSONResponse(

            {

                "message":

                "File uploaded successfully",


                "url":

                file_url

            }

        )




    except Exception as e:



        raise HTTPException(

            status_code=500,

            detail=str(e)

        )