from sys import exit
from google_trans_new import google_translator  
import http.client, urllib.parse, json, time, sys

class EchoBot:
    async def on_turn(self, context):
        if context.activity.type == "message" and context.activity.text:
            translator = google_translator()  
            lang = translator.detect(context.activity.text) 
            org_lang = lang[0] #later will be used for answer translation
            if org_lang != 'en':
                text = translator.translate(context.activity.text, lang_tgt = 'en')
            else:
                text = context.activity.text

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
    

            sendInfo = answer
            await context.send_activity(sendInfo)