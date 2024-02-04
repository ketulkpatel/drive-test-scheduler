import boto3
from botocore.exceptions import ClientError
import json
import smtplib

queue_url = 'https://sqs.us-east-1.amazonaws.com/646219003399/StoreAppointmentMessageQueue.fifo'

sqs = boto3.client('sqs')


def send_email(sender_email, sender_password, receiver_email, subject, body):
    gmail_user = sender_email
    gmail_app_password = sender_password
    sent_from = gmail_user
    sent_to = [receiver_email]
    sent_subject = subject
    sent_body = body

    email_text = """\
From: %s
To: %s
Subject: %s
%s
""" % (sent_from, ", ".join(sent_to), sent_subject, sent_body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text.encode("utf-8"))
        server.close()
        print(email_text)
        print('Email sent!')
    except Exception as exception:
        print(str(exception))


def lambda_handler(event, context):
    
    try:
        for record in event['Records']:
            receipt_handle = record['receiptHandle']
            message_body = json.loads(record['body'])
            type = message_body['type']
            
            if type == "book":
                appointment_date = message_body['appointment_date']
                appointment_slot = message_body['appointment_slot']
                appointment_id = message_body['appointment_id']
                license_number = message_body['license_number']
                date_of_birth = message_body['date_of_birth']
                
                subject = "Related to road test appointment booking"
                body = f"""
                This is to confirm your appointment for a road test on {appointment_date} at {appointment_slot}. Your appointment ID is {appointment_id}.
    
                Please make sure to bring your driver's license with you, as we will need to verify your identity before the test.
                
                To confirm, your driver's license number is {license_number}, and your date of birth is {date_of_birth}.
                
                If you have any questions or need to reschedule or cancel your appointment, please visit the website again.
                
                Thank you for choosing us for your road test appointment.
                """
                
            elif type == "cancel":
                appointment_id = message_body['appointment_id']
                license_number = message_body['license_number']
                date_of_birth = message_body['date_of_birth']
                
                subject = "Related to road test appointment cancel"
                body = f"""
                This is to confirm your appointment for a road test for appointment ID: {appointment_id} has been canceled.
    
                Your driver's license number is {license_number}, and your date of birth is {date_of_birth}.
                
                If you have any questions or need to book your appointment, please visit the website again.
                
                Thank you for choosing us to cancel your road test appointment.
                """
            
            elif type == "reschedule":
                appointment_date = message_body['appointment_date']
                appointment_slot = message_body['appointment_slot']
                appointment_id = message_body['appointment_id']
                license_number = message_body['license_number']
                date_of_birth = message_body['date_of_birth']
                
                subject = "Related to road test appointment reschedule"
                body = f"""
                This is to confirm your appointment for a road test on {appointment_date} at {appointment_slot}. Your appointment ID is {appointment_id}.
    
                Please make sure to bring your driver's license with you, as we will need to verify your identity before the test.
                
                To confirm, your driver's license number is {license_number}, and your date of birth is {date_of_birth}.
                
                If you have any questions or need to reschedule or cancel your appointment, please visit the website again.
                
                Thank you for choosing us for your road test appointment.
                """
                
            else:
                return json.dumps("Please check type received from Main function.")
            
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            
            secret = get_secret()
            sender_email = secret['emailID']
            sender_password = secret['password']
            receiver_email = message_body['email_address']
            response = send_email(sender_email, sender_password, receiver_email, subject, body)
        
    except Exception as e:
        response = str(e)
    
    print(response) 
    
def get_secret():

    secret_name = "StoreEmailCredentials"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])
    return secret
    