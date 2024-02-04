import json
import boto3
from boto3.dynamodb.conditions import Attr
import uuid

sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/646219003399/BookAppointmentMessageQueue'
dynamo_db = boto3.resource('dynamodb')
appointment_table_name='Appointment'
appointment_table = dynamo_db.Table(appointment_table_name)

payment_table_name='PaymentInformation'
payment_table = dynamo_db.Table(payment_table_name)

def make_response(status, message , data):
    return {
        "status": status,
        "message": message,
        "data": data
    }

def lambda_handler(event, context):
    
    try:
        receipt_id = event['receipt_id']
        license_number = event['license_number']
        date_of_birth = event['date_of_birth']
        email_address = event['email_address']
        appointment_date = event['appointment_date']
        appointment_slot = event['appointment_slot']
        type = event['type']

        result_payment = payment_table.scan(FilterExpression= Attr('receipt_id').eq(receipt_id) and Attr('license_number').eq(license_number) and Attr('date_of_birth').eq(date_of_birth) )
    
        if result_payment['Count'] == 0:
            response =  make_response(False, "Please provide correct details.", None)
        else:
            
            result_appointment = appointment_table.scan(FilterExpression= Attr('license_number').eq(license_number) and Attr('date_of_birth').eq(date_of_birth) )
            
            if result_appointment['Count'] == 0:
                appointment_id = uuid.uuid4().hex
                appointment_table.put_item(Item={"appointment_id": appointment_id,"license_number": license_number, "date_of_birth": date_of_birth, "email_address": email_address, "appointment_date": appointment_date, "appointment_slot": appointment_slot})
                message = json.dumps({
                    "type": type,
                    "appointment_id": appointment_id,
                    "license_number": license_number,
                    "date_of_birth": date_of_birth,
                    "email_address": email_address,
                    "appointment_date": appointment_date,
                    "appointment_slot": appointment_slot
                })
                sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=message
                )
                response = make_response(True, "Appointment has been booked. You will recieve email for the same soon.", appointment_id)

            else:
                response = make_response(False, "Appointment has been already booked.", None)
       
    except Exception as e:
        response = make_response(False, str(e), None)

    return response

