





import requests
import json
import openai
import sys,os
import logging
# import backoff


openai.api_key = "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"


# @backoff.on_exception(backoff.expo, openai.OpenAIError, max_tries=3)
def make_request_openai(aiInput:str, model='text-davinci-003', temperature=0, top_p=1, frequency_penalty=0, presence_penalty=0):
    response = openai.Completion.create(
            model=model,
            prompt=aiInput,
            temperature=temperature,
            max_tokens=1024,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
        )
    return response


def extract_entity_resume(text):
    aiInput="""
    Extract the all the relevant entities and information from resume in json , do not include jsonoutput or anything , simply return dict
  """+text
    response=make_request_openai(aiInput)

    logging.debug(
        "ResumeAIHandler: extract entities: REQUEST => "
        + aiInput
        + ", \n RESPONSE =>"
        + str(response)
        + ", \n API RESPONSE =>"
        + "return response...>"
        + response["choices"][0]["text"]
    )

    if response["choices"][0] and response["choices"][0]["text"]:
        resp_data=response["choices"][0]["text"]
        logging.debug(resp_data)
        return resp_data
        
       
    else:
        logging.debug("Returning None")
        return "None"