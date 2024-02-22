import boto3
import json
from textspeech import TextToSpeech
from playsound import playsound

def detect_faces(photo, bucket):
    
    session = boto3.Session(profile_name='default')
    client = session.client('rekognition')

    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                   Attributes=['ALL'])
    print("heres is the response"+str(response))
    print('Detected faces for ' + photo)
    #print(response)
    if not response['FaceDetails']:
        print("FaceDetails is empty")
        gender_value = "null"
        gender_confidence="gender_confidence"
    else:
        for faceDetail in response['FaceDetails']:
            print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
                  + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
            print("here is the face detail"+faceDetail)
            #print('Here are the other attributes:')
            #print(json.dumps(faceDetail, indent=4, sort_keys=True))
            # Access predictions for individual face details and print them
            #print("Gender: " + str(faceDetail['Gender']))
            gender_value = faceDetail['Gender']['Value']
            gender_confidence = faceDetail['Gender']['Confidence']
            #----------------------------
            #print("Smile: " + str(faceDetail['Smile']))
            #print("Eyeglasses: " + str(faceDetail['Eyeglasses']))
            #print("Face Occluded: " + str(faceDetail['FaceOccluded']))
            #print("Emotions: " + str(faceDetail['Emotions'][0]))
            print()
            #return len(response['FaceDetails'])
    return gender_value,gender_confidence
    
def main():
    photo='cam_12023-10-03-12-39-04.jpg'
    bucket='220073549'
    folder_name = 'boss-email'
    face_gender,face_confidence = detect_faces(photo, bucket)
    #detect_faces(photo, bucket)
    
    print(face_confidence)
    if (face_gender=="Female"):
        TextToSpeech("小姐你好")
    elif (face_gender=="Male"):
        TextToSpeech("先生你好")
    else:
        TextToSpeech("大家你好")
    
    playsound('C:\\A05\\FYP-test\\sound\\output.mp3')


if __name__ == "__main__":
    main()
