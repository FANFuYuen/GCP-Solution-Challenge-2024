#Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

import io
from PIL import Image, ImageDraw, ExifTags, ImageColor

def export_ppe(photo,bucket,folder_name ,confidence):

    fill_green='#00d400'
    fill_red='#ff0000'
    fill_yellow='#ffff00'
    line_width=3

    #open image and get image data from stream.
    s3 = boto3.resource('s3')
    session = boto3.Session(profile_name='default')
    image = s3.Object(bucket,folder_name + '/' +photo)
    image = Image.open(image.get()['Body'])
    stream = io.BytesIO()
    image.save(stream, format=image.format)    
    image_binary = stream.getvalue()
    imgWidth, imgHeight = image.size  
    draw = ImageDraw.Draw(image)  

    client=session.client('rekognition')

    response = client.detect_protective_equipment(Image={'Bytes': image_binary})

    for person in response['Persons']:
        
        found_mask=False

        for body_part in person['BodyParts']:
            ppe_items = body_part['EquipmentDetections']
                 
            for ppe_item in ppe_items:
                #found a mask 
                if ppe_item['Type'] == 'FACE_COVER':
                    fill_color=fill_green
                    found_mask=True
                    # check if mask covers face
                    if ppe_item['CoversBodyPart']['Value'] == False:
                        fill_color=fill='#ff0000'
                    # draw bounding box around mask
                    box = ppe_item['BoundingBox']
                    left = imgWidth * box['Left']
                    top = imgHeight * box['Top']
                    width = imgWidth * box['Width']
                    height = imgHeight * box['Height']
                    points = (
                            (left,top),
                            (left + width, top),
                            (left + width, top + height),
                            (left , top + height),
                            (left, top)
                        )
                    draw.line(points, fill=fill_color, width=line_width)

                     # Check if confidence is lower than supplied value       
                    if ppe_item['CoversBodyPart']['Confidence'] < confidence:
                        #draw warning yellow bounding box within face mask bounding box
                        offset=line_width+ line_width 
                        points = (
                                    (left+offset,top + offset),
                                    (left + width-offset, top+offset),
                                    ((left) + (width-offset), (top-offset) + (height)),
                                    (left+ offset , (top) + (height -offset)),
                                    (left + offset, top + offset)
                                )
                        draw.line(points, fill=fill_yellow, width=line_width)
                
        if found_mask==False:
            # no face mask found so draw red bounding box around body
            box = person['BoundingBox']
            left = imgWidth * box['Left']
            top = imgHeight * box['Top']
            width = imgWidth * box['Width']
            height = imgHeight * box['Height']
            points = (
                (left,top),
                (left + width, top),
                (left + width, top + height),
                (left , top + height),
                (left, top)
                )
            draw.line(points, fill=fill_red, width=line_width)

    image.show()
    # Create a new BytesIO object
    stream = io.BytesIO()
    # Save the modified image to the stream in JPEG format
    image.save(stream, format='JPEG')
    # Seek to the start of the stream
    stream.seek(0)
    # Create a new S3 client
    s3_client = session.client('s3')

    photo = folder_name + '/' +photo
    # Upload the stream to S3
    s3_client.upload_fileobj(stream, bucket,photo,ExtraArgs={'ACL':'public-read', 'ContentType': 'image/jpeg', 'ContentDisposition': 'inline'})
    

def main():
    photo='cam_12023-10-12-14-53-23.jpg'
    bucket = '220073549'
    folder_name = 'boss-email'
    confidence=80
    export_ppe(photo,bucket ,folder_name,confidence)

if __name__ == "__main__":
    main()