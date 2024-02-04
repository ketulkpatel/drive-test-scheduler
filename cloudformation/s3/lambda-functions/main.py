import json
import boto3
from boto3.dynamodb.conditions import Attr
import uuid


sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/646219003399/StoreAppointmentMessageQueue.fifo'
dynamo_db = boto3.resource('dynamodb')
appointment_table_name='Appointment'
appointment_table = dynamo_db.Table(appointment_table_name)

payment_table_name='PaymentInformation'
payment_table = dynamo_db.Table(payment_table_name)

def make_response(status, message , data):
    return json.dumps({
        "status": status,
        "message": message,
        "data": data
    })


def lambda_handler(event, context):
    
    try:
        body = event['body']
        body_json = json.loads(body)
        
        type = body_json['type']
    
        if type == "book":
            receipt_id = body_json['receipt_id']
            license_number = body_json['license_number']
            date_of_birth = body_json['date_of_birth']
            email_address = body_json['email_address']
            appointment_date = body_json['appointment_date']
            appointment_slot = body_json['appointment_slot']

            result_payment = payment_table.scan(FilterExpression= Attr('receipt_id').eq(receipt_id) and Attr('license_number').eq(license_number) and Attr('date_of_birth').eq(date_of_birth) )
            
            if result_payment['Count'] == 0:
                response =  make_response(False, "Please provide correct details.", None)
            else:
                
                result_appointment = appointment_table.scan(FilterExpression= Attr('license_number').eq(license_number) and Attr('date_of_birth').eq(date_of_birth) )
                
                if result_appointment['Count'] == 0:
                    appointment_id = uuid.uuid4().hex
                    appointment_table.put_item(Item={"appointment_id": appointment_id,"license_number": license_number, "date_of_birth": date_of_birth, "email_address": email_address, "appointment_date": appointment_date, "appointment_slot": appointment_slot})
                    response = make_response(True, "Appointment has been booked. You will recieve email for the same soon.", appointment_id)
                    
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
                        MessageBody=message,
                        MessageGroupId='lambda-group',
                        MessageDeduplicationId=str(context.aws_request_id)
                    )
                else:
                    response = make_response(False, "Appointment has been already booked.", None)

        elif type == "cancel":
            license_number = body_json['license_number']
            date_of_birth = body_json['date_of_birth']
            email_address = body_json['email_address']
            appointment_id = body_json['appointment_id']
            result_appointment = appointment_table.scan(FilterExpression= Attr('license_number').eq(license_number) and Attr('date_of_birth').eq(date_of_birth) and Attr('appointment_id').eq(appointment_id) )
            
            if result_appointment['Count'] == 0:
                response = make_response(False, "Please provide correct details.", None)
            else:
                cancel_appoitnment = appointment_table.delete_item(
                    Key={
                        'appointment_id': appointment_id
                    }
                )
                message = json.dumps({
                        "type": type,
                        "appointment_id": appointment_id,
                        "license_number": license_number,
                        "date_of_birth": date_of_birth,
                        "email_address": email_address
                    })
                sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=message,
                    MessageGroupId='lambda-group',
                    MessageDeduplicationId=str(context.aws_request_id)
                )
                response = make_response(True, "Appointment has been cancelled. You will recieve email for the same soon.", None)
                
        elif type == "reschedule":
            license_number = body_json['license_number']
            date_of_birth = body_json['date_of_birth']
            email_address = body_json['email_address']
            appointment_id = body_json['appointment_id']
            appointment_date = body_json['appointment_date']
            appointment_slot = body_json['appointment_slot']
            result_appointment = appointment_table.scan(FilterExpression= Attr('license_number').eq(license_number) and Attr('date_of_birth').eq(date_of_birth) and Attr('appointment_id').eq(appointment_id) )
            
            if result_appointment['Count'] == 0:
                response = make_response(False, "Please provide correct details.", None)
            else:
                reschedule_appointment = appointment_table.get_item(Key={'appointment_id': appointment_id})
                reschedule_appointment_item = reschedule_appointment['Item']
                reschedule_appointment_item['appointment_date'] = appointment_date
                reschedule_appointment_item['appointment_slot'] = appointment_slot
                reschedule_appointment_item['email_address'] = email_address

                appointment_table.put_item(Item=reschedule_appointment_item)
                
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
                    MessageBody=message,
                    MessageGroupId='lambda-group',
                    MessageDeduplicationId=str(context.aws_request_id)
                )
                response = make_response(True, "Appointment has been rescheduled. You will recieve email for the same soon.", None)
                
        elif type == "view":
            license_number = body_json['license_number']
            date_of_birth = body_json['date_of_birth']
            appointment_id = body_json['appointment_id']
            result_appointment = appointment_table.scan(FilterExpression= Attr('license_number').eq(license_number) and Attr('date_of_birth').eq(date_of_birth) and Attr('appointment_id').eq(appointment_id) )
            
            if result_appointment['Count'] == 0:
                response = make_response(False, "Please provide correct details.", None)
            else:
                view_appointment = appointment_table.get_item(Key={'appointment_id': appointment_id})
                view_appointment_item = view_appointment['Item']
                response = make_response(True, "Appointment has been fetched.", view_appointment_item)
                
        else:
            response = make_response(False, "Please check your type.", None)
    except Exception as e:
        response = make_response(False, str(e), None)

    return response