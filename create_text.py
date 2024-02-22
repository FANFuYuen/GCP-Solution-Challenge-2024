from playsound import playsound
from textspeech import TextToSpeech
from sns import sns 

def convert_to_text(data):
    new_list = []
    no_equipment_dict = {} # initialize the dictionary
    
    for item in data:
        for body_part in item['BodyParts']:
            new_item = {}
            new_item['BodyPartsName'] = body_part['Name']
            if not body_part['EquipmentDetections'] and body_part['Confidence'] > 60:
                new_item['EquipmentDetections'] = False
                new_list.append(new_item)
                # add the name and message of the body part to the dictionary
                if body_part['Name'] == 'FACE':
                    no_equipment_dict['FACE'] = "You forgot to wear a mask"
                elif body_part['Name'] == 'LEFT_HAND':
                    no_equipment_dict['LEFT_HAND'] = "You forgot to wear left gloves"
                elif body_part['Name'] == 'RIGHT_HAND':
                    no_equipment_dict['RIGHT_HAND'] = "You forgot to wear right gloves"
                elif body_part['Name'] == 'HEAD':
                    no_equipment_dict['HEAD'] = "You forgot to wear a helmet"
                # you can add more cases here for other body parts
            else:
                for equipment in body_part['EquipmentDetections']:
                    new_item['EquipmentDetections'] = True
                    new_list.append(new_item)
    
    print("New list:",new_list)
    print()
    print()
    
    # use a dictionary to store the mapping between the English and Chinese names of the body parts
    name_dict_eng = {'FACE': 'masks', 'LEFT_HAND': 'left gloves','RIGHT_HAND': 'right gloves', 'HEAD': 'helmet'}
    name_dict_can = {'FACE': '口罩', 'LEFT_HAND': '左手手套','RIGHT_HAND': '右手手套', 'HEAD': '頭盔'}
    # use the join method to concatenate the English names of the body parts with "and"
    no_equipment_names_eng = " and ".join(no_equipment_dict.keys())
    # use the join method to concatenate the Chinese names of the body parts with "同"
    no_equipment_names_can = " 同 ".join(name_dict_can[name] for name in no_equipment_dict.keys())
    
    # print the English sentence
    print("You forgot to bring " + no_equipment_names_eng)
    # print the Chinese sentence
    print("你好似唔記得帶 " + no_equipment_names_can)
    text_to_speech = "你好似唔記得帶" + no_equipment_names_can + "喎!"
    TextToSpeech(text_to_speech)
    playsound('C:\\A05\\FYP-test\\sound\\output.mp3')

    #send sms to Supervisor
    print(no_equipment_dict)
    Without_Equipment_Types = [name_dict_eng[name] for name in no_equipment_dict.keys()]
    print("".join(name_dict_eng[name] for name in no_equipment_dict.keys()))
    print(Without_Equipment_Types)
    #sns(Without_Equipment_Types)
    return Without_Equipment_Types


def main():
    # Your JSON data
    #data = [{'BodyParts': [{'Name': 'FACE', 'Confidence': 99.33522033691406, 'EquipmentDetections': []}, {'Name': 'HEAD', 'Confidence': 99.9900894165039, 'EquipmentDetections': [{'BoundingBox': {'Width': 0.34320372343063354, 'Height': 0.21172700822353363, 'Left': 0.3430291414260864, 'Top': 0.1534411460161209}, 'Confidence': 99.68537902832031, 'Type': 'HEAD_COVER', 'CoversBodyPart': {'Confidence': 99.96173095703125, 'Value': True}}]}], 'BoundingBox': {'Width': 0.5586622953414917, 'Height': 0.8255558013916016, 'Left': 0.33662280440330505, 'Top': 0.16051796078681946}, 'Confidence': 99.97274780273438, 'Id': 0}]
    #data = [{'BodyParts': [{'Name': 'FACE', 'Confidence': 99.9471664428711, 'EquipmentDetections': []}, {'Name': 'HEAD', 'Confidence': 99.9997329711914, 'EquipmentDetections': []}], 'BoundingBox': {'Width': 0.8396624326705933, 'Height': 0.958730161190033, 'Left': 0.12025316804647446, 'Top': 0.03492063656449318}, 'Confidence': 99.97567749023438, 'Id': 0}]
    data = [{'BodyParts': [{'Name': 'FACE', 'Confidence': 99.96942138671875, 'EquipmentDetections': []}, {'Name': 'LEFT_HAND', 'Confidence': 99.81414031982422, 'EquipmentDetections': []}, {'Name': 'RIGHT_HAND', 'Confidence': 87.91783142089844, 'EquipmentDetections': []}, {'Name': 'HEAD', 'Confidence': 99.99913787841797, 'EquipmentDetections': []}], 'BoundingBox': {'Width': 0.5666217803955078, 'Height': 0.7951564192771912, 'Left': 0.23082099854946136, 'Top': 0.18466195464134216}, 'Confidence': 99.99397277832031, 'Id': 0}]
    convert_to_text(data)

if __name__ == "__main__":
    main()