import boto3


def sns(Without_Equipment_Types,photo_name):
    # Create a SNS client
    client = boto3.client("sns")
    print("ready for send sms.")

    # Create a dictionary mapping equipment types to emojis
    emoji_dict = {'helmet': '⛑️', 'left gloves': '🫱', 'right gloves': '🫲','masks':'😷'}
    Without_Equipment_Types = [f'{item} {emoji_dict[item]}' for item in Without_Equipment_Types]

    # Convert list to string with newline character as separator
    equipment_string = '\n'.join(Without_Equipment_Types)
    message =  f'''cam1 discover someone is unsafe:
Without Equipment Types:
{equipment_string}
Venue: Level 2 Entry
The detail below:
https://220073549.s3.amazonaws.com/boss-email/{photo_name}
'''
    print(message)

    # Send a SMS message
    client.publish(PhoneNumber="+85246384562", Message=message)






def main():
    Without_Equipment_Types =['masks', 'left gloves', 'right gloves', 'helmet']
    photo_name = 'example.jpg'
    sns(Without_Equipment_Types, photo_name)

if __name__ == "__main__":
    main()