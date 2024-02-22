# import the opencv library
import cv2
from datetime import datetime


def current_time():
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return current_time


save_local_path = "C:\\A05\\FYP-test\\photo\\"
#print("Current Time =", current_time)

# define video capture objects for two webcams
vid1 = cv2.VideoCapture(0)
vid2 = cv2.VideoCapture(1)

while (True):
    # Capture the video frame by frame from first webcam
    ret1, frame1 = vid1.read()
    # Display the resulting frame
    cv2.imshow('frame1', frame1)

    # Capture the video frame by frame from second webcam
    ret2, frame2 = vid2.read()
    # Display the resulting frame
    cv2.imshow('frame2', frame2)

    # the 'q' button is set as the quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

    # Save photo when 's' key is pressed
    if cv2.waitKey(2) & 0xFF == ord('s'):
        #cv2.imwrite(save_local_path+'photo_'+current_time+'.jpg', frame1)
        now = str(current_time())
        cv2.imwrite(save_local_path+"cam_1-"+now+".jpg", frame1)
        cv2.imwrite(save_local_path+"cam_2-"+now+".jpg", frame2)
        print(save_local_path+"hello1"+str(current_time())+".jpg")
        print("Photo saved successfully!")

# After the loop release the cap objects
vid1.release()
vid2.release()
# Destroy all the windows
cv2.destroyAllWindows()
