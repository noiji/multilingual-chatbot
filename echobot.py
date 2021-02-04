from sys import exit
from google_trans_new import google_translator  
import http.client, urllib.parse, json, time, sys
import os

def get_serial():
        answer = "The serial number of your product " + os.popen("wmic diskdrive get caption").read()[8:] + "is " + os.popen("wmic diskdrive get serialnumber").read()[14:]
        return answer.replace('\n', ' ')

def get_translated(text):
        translator = google_translator()  
        lang = translator.detect(text) 
        org_lang = lang[0] #later will be used for answer translation
        if org_lang != 'en':
            text = translator.translate(text, lang_tgt = 'en')

        host = "0204swfc.azurewebsites.net";
        endpoint_key = "ba521fca-288c-40e2-9b48-b9e4f16c3020";
        route = "/qnamaker/knowledgebases/c28a1807-99cd-4f47-920d-cb60755926a6/generateAnswer";

        questions = {'question': text,'top': 3}
        questions = str(questions)

        headers = {
            'Authorization': 'EndpointKey ' + endpoint_key,
            'Content-Type': 'application/json'
        }

        try:
            conn = http.client.HTTPSConnection(host,port=443)
            conn.request ("POST", route,  questions, headers)
            response = conn.getresponse ()
            answer = response.read ()
            ret = json.loads(answer)
            answer = ret['answers'][0]['answer']

        except :
            answer = "Sorry. Can't find an answer. (HTTPS Connection Error)"
    
        if org_lang != 'en':
            answer = translator.translate(answer, lang_tgt = org_lang) 

        return answer

class EchoBot:
    async def on_turn(self, context):
        answer = "Hello and welcome to Samsung SSD Support Chatbot. Type 'serial' if you want to get the serial number of your product. "
        if context.activity.type == "message" and context.activity.text:
            if 'serial' in context.activity.text:
                answer = get_serial()
            else: 
                answer = get_translated(context.activity.text)
        sendInfo = answer
        await context.send_activity(sendInfo)