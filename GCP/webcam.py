from google.cloud import storage
import os
from DetectFaces import detect_faces
from ppe import detect_ppe
from create_text import convert_to_text
from textspeech import TextToSpeech
from playsound import playsound
from export_ppe import export_ppe
from sns import sns
import cv2
from datetime import datetime
import base64
import time

#config
save_local_path = "C:\\A05\\FYP-test\\webcam_photo\\"
bucket_name = '220073549'
folder_name = 'boss-email'
file_name = 'test.jpg'
global photo_name
confidence=80
# Get the current time
start_time = time.time()

def current_time():
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return current_time


# Pass the image data to an encoding function.
def encode_image(image):
    with open(image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()  # added .decode() here
    return encoded_string

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

# define video capture objects for two webcams
vid1 = cv2.VideoCapture(0)
vid2 = cv2.VideoCapture(1)

while(True):
    # Capture the video frame by frame from first webcam
    ret1, frame1 = vid1.read()
    ret2, frame2 = vid2.read()

    # Create a copy of the frames for saving
    save_frame1 = frame1.copy()
    save_frame2 = frame2.copy()

    # Calculate the time remaining until the next photo
    time_remaining = int(20 - (time.time() - start_time))

    # Draw the countdown timer on the frames
    cv2.putText(frame1, 'Next photo in: {}s'.format(time_remaining), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(frame2, 'Next photo in: {}s'.format(time_remaining), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    # Display the resulting frame
    cv2.imshow('frame1', frame1)
    cv2.imshow('frame2', frame2)
    
    # the 'q' button is set as the quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
    
    # Save photo when 's' key is pressed
    if cv2.waitKey(2) & 0xFF == ord('s'):
        now = str(current_time())
        cv2.imwrite(save_local_path+"cam_1"+now+".jpg", frame1)
        cv2.imwrite(save_local_path+"cam_2"+now+".jpg", frame2)
        print(save_local_path+"hello1"+str(current_time())+".jpg")
        print("Photo saved successfully!")
        encoded_image = encode_image(save_local_path+"cam_1"+now+".jpg")
        photo_name="cam_1"+now+".jpg"
        upload_blob(bucket_name, save_local_path+photo_name, folder_name+'/'+photo_name)
        ppe_json = detect_ppe("cam_1"+now+".jpg", bucket_name,folder_name)
        Without_Equipment_Types= convert_to_text(ppe_json)
        export_ppe(photo_name,bucket_name,folder_name ,confidence)
        sns(Without_Equipment_Types,photo_name)
        
    # Save photo every 10 seconds
    if time.time() - start_time >= 20: # 20 seconds
        now = str(current_time())
        cv2.imwrite(save_local_path+"cam_1"+now+".jpg", save_frame1)
        cv2.imwrite(save_local_path+"cam_2"+now+".jpg", save_frame2)
        print(save_local_path+"hello1"+str(current_time())+".jpg")
        print("Photo saved successfully!")
        start_time = time.time() # reset the time
        

# After the loop release the cap objects
vid1.release()
vid2.release()
# Destroy all the windows
cv2.destroyAllWindows()
