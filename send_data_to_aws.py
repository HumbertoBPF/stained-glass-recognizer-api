import csv

import boto3


def send_image_data_to_dynamo_db():
    client = boto3.client('dynamodb')

    with open('db_data/info_images.csv', mode='r') as f:
        csv_file = csv.DictReader(f)

        for row in csv_file:
            print(row)
            response = client.put_item(
                Item={
                    'name': {
                        'S': row['filename'],
                    },
                    'artist': {
                        'S': row['artist'],
                    },
                    'year_birth': {
                        'S': row['year of birth'],
                    },
                    'year_passing': {
                        'S': row['year of passing']
                    },
                    'artist_reference': {
                        'S': row['artist reference']
                    },
                    'glass_date': {
                        'S': row['glass date']
                    },
                    'date_reference': {
                        'S': row['date reference']
                    },
                    'iconography': {
                        'S': row['iconography']
                    },
                    'church_name': {
                        'S': row['church name']
                    },
                    'url': {
                        'S': row['url']
                    }
                },
                ReturnConsumedCapacity='TOTAL',
                TableName='stained-glass-images',
            )

            print(response)


send_image_data_to_dynamo_db()
