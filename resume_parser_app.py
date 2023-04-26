from fastapi import FastAPI,Request
import logging
from parse_data import *
from fastapi import File, UploadFile,Response
import os
from call_gpt import *
from fastapi.responses import JSONResponse


logging.basicConfig(filename="./logs/resume_parser_app.log",level=logging.DEBUG)

app = FastAPI()




@app.get("/")
def read():
    return {"Hello":"Welcome to Resume Parser, AI service"}

async def upload_file(file):
    filepath=os.path.join("fileupload",file.filename)
    with open(filepath, 'wb') as f:
        content = await file.read()
        f.write(content)
        f.close()
    return filepath




@app.post("/parse_file")
async def make_call(file: UploadFile = File(...)):
    """
    Main function: takes an Input file 
   1. Extract the text from the file
   2. create prompt for gpt call
   2. pass the text to gpt to extract the information from the resume
   return Json 
    """

    try:
    
        filepath=await upload_file(file)
        logging.debug(f'Processing Filepath:  {filepath}')
        text=await get_text_resume(filepath)
        # call gpt
        response=extract_entity_resume(text)
        # response=response.replace("\"", "\'")
        return JSONResponse(content={
            "response": response,
            "staus": "Ok"
        }, status_code=200)
    

    except Exception as err:
        logging.error(f'could not print REQUEST: {err}')
        return JSONResponse(content={
           "response": {},
            "error_message": "could not process request"
        }, status_code=404)
  


