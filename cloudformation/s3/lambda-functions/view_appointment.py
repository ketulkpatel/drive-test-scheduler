import boto3
from boto3.dynamodb.conditions import Attr

sqs = boto3.client('sqs')
dynamo_db = boto3.resource('dynamodb')
appointment_table_name='Appointment'
appointment_table = dynamo_db.Table(appointment_table_name)

def make_response(status, message , data):
    return {
        "status": status,
        "message": message,
        "data": data
    }


def lambda_handler(event, context):
    
    try:

        license_number = event['license_number']
        date_of_birth = event['date_of_birth']
        appointment_id = event['appointment_id']
        result_appointment = appointment_table.scan(FilterExpression= Attr('license_number').eq(license_number) and Attr('date_of_birth').eq(date_of_birth) and Attr('appointment_id').eq(appointment_id) )
        
        if result_appointment['Count'] == 0:
            response = make_response(False, "Please provide correct details.", None)
        else:
            view_appointment = appointment_table.get_item(Key={'appointment_id': appointment_id})
            view_appointment_item = view_appointment['Item']
            response = make_response(True, "Appointment has been fetched.", view_appointment_item)
                    
    except Exception as e:
        response = make_response(False, str(e), None)

    return response

