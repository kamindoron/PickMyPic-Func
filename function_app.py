import azure.functions as func
import datetime
import json
import logging

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime as dt

import KeyVault #PickMyPic utils file.


VERSION = """ version 1.1.1
        ----------------------   
"""

app = func.FunctionApp()

STORAGE_ACCOUNT_NAME = KeyVault.get_secret("storage-account-name")

EMAIL_SERVER_HOST = KeyVault.get_secret("email-host")
EMAIL_SERVER_PORT = KeyVault.get_secret("email-port")
EMAIL_SERVER_MAIL = KeyVault.get_secret("email-support-mail") 
EMAIL_SERVER_PASSWORD = KeyVault.get_secret("email-password") 

#example local:  http://localhost:7071/api/PickMyPicFunc?query=version
#example deploy: https://pickmypic-func-dev.azurewebsites.net/api/PickMyPicFunc?query=version
@app.route(route="PickMyPicFunc", auth_level=func.AuthLevel.ANONYMOUS)
def pickmypic_func(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('---------- pickmypic_func info Python HTTP trigger function processed a request.------------')
    logging.debug('-----------pickmypic_func debug Python HTTP trigger function processed a request.---------')
    logging.warning('---------------pickmypic_func warning Python HTTP trigger function processed a request.------------')

    query = req.params.get('query')

    if not query:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            query = req_body.get('query')
       
    match (query):
        case 'version':
            print(f'version: {VERSION}')
            return func.HttpResponse(f"PickMyPicFunc version: {VERSION}")
        
        case 'test':
            print(f'******* FUNC **********')
            KeyVault.print_version()

            return func.HttpResponse(f"KeyVault.print() called")

        case 'name':
            #from demo code...   
            name = req.params.get('name')
            print(f"PickMyPicFunc Hello, {name}. This HTTP triggered function executed successfully.")
            return func.HttpResponse(f"PickMyPicFunc Hello, {name}. This HTTP triggered function executed successfully.")
        
        case 'secr':
            logging.info(f'STORAGE_ACCOUNT_NAME: {STORAGE_ACCOUNT_NAME} ')
            return func.HttpResponse(f'STORAGE_ACCOUNT_NAME: {STORAGE_ACCOUNT_NAME}')
        
        case _:
             print(f"PickMyPicFunc This HTTP triggered function executed successfully. query=name, query=version")
             return func.HttpResponse(f"PickMyPicFunc This HTTP triggered function executed successfully. query=name, query=version", status_code=200)


    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')
    #         return func.HttpResponse(
    #             "PickMyPicFunc This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.", 
    #             status_code=200)

    # if name:
    #     return func.HttpResponse(f"PickMyPicFunc Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "PickMyPicFunc This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )

#connection="AzureWebJobsStorage" - for local usage   connection="STORAGE_CONNECTION_STRING" for deployed function
@app.queue_trigger(arg_name="message", queue_name="emailqueue",
                  connection="STORAGE_CONNECTION_STRING", auth_level=func.AuthLevel.ANONYMOUS) 
def QueueTriggerFunc(message: func.QueueMessage):
    logging.info('QueueTriggerFunc %i, Python Queue trigger processed a message: %s',
                message.dequeue_count,
                message.get_body().decode('utf-8'))
    
    print(f'count: {message.dequeue_count}')
    message_json = message.get_body().decode('utf-8')
    print(f'***message_json: {message_json}')
    params = json.loads(message_json)

    params['src_email']="support@pickmypic.ai"

    print(f'***params: {params}'.encode('utf-8'))

    type = params.get('type')
    print(f" ***event_name: {params.get('type')}")

    if (str(type).lower() == 'webappuser'):
        send_email_to_webapp_user(params)



#def send_email(email_address, email_password, recipient, event_name, user_name, user_photos_link, exp_date, event_id, user_id):
def send_email_to_webapp_user(params: dict):
    logging.info(f"{dt.now()}  send_email start: destEmail: {params['dest_email']}, event: {params['event_id']}, eventName:{params['event_name']}, user:{params['user_id']}")

    # email message
    msg = MIMEMultipart()
    msg['From'] = params.get('src_email')
    msg['To'] = params.get('dest_email')
    msg['Subject'] = "FUNC!!! PickMyPic: התמונות שלך מהאירוע כבר כאן!"

    press_link_text = " לצפיה חוזרת בתמונות שלך מהאירוע או על הקישור הבא"
    exp_text = f"הקישור יהיה זמין עד לתאריך: {params['expiration_date']}"
    thanks_text = "תודה שבחרתם להשתמש בפלטפורמה שלנו"
    team_text = "PickMyPic"
    # create a beautiful email body
    body = """
    <html dir="rtl">
        <head>
            <style>
                h1 {{
                    color: black;
                    text-align: center;
                }}
                p {{
                    color: black;
                    text-align: center;
                    font-size: 18px;
                }}
                a {{
                    color: black;
                    text-align: center;
                    font-size: 18px;                    
                }}
                img {{
                    display: block;
                    margin: auto;
                }}
                .underlined {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <h1>{}</h1>
            <br>
            <p>{}, יש <a href="{}" target="_blank" class="underlined">ללחוץ כאן</a>{}</p>
            <p><a href="{}" target="_blank" class="underlined">{}</a></p>
            <p>{}</p>
            <br>
            <p>{}</p>
            <p>
                <a href="https://lp.pickmypic.ai/" target="_blank" class="underlined">
                  {}
                </a>
            </p>
        </body>
    </html>
    """.format(params['event_name'], params['user_name'], params['user_photos_link'], press_link_text, params['user_photos_link'], params['user_photos_link'], 
               exp_text, thanks_text, team_text)

    msg.attach(MIMEText(body, 'html'))

    # establish SMTP connection
    server = smtplib.SMTP_SSL(EMAIL_SERVER_HOST, EMAIL_SERVER_PORT)
    server.login(EMAIL_SERVER_MAIL, EMAIL_SERVER_PASSWORD)

    # send email
    text = msg.as_string()
    try:
        server.sendmail(params.get('src_email'), params['dest_email'], text)
    except Exception as e:
        logging.warning(f"{dt.now()} ERROR: send_email failed. destEmail: {params['dest_email']}, event: {params['event_id']}, eventName:{params['event_name']}, user:{params['user_id']}, error: {e}")

    # close the SMTP connection
    server.quit()
    logging.info(f"{dt.now()}  send_email OK. destEmail: {params['dest_email']}, event: {params['event_id']}, eventName:{params['event_name']}, user:{params['user_id']}")

