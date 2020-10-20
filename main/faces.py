import boto3
# import cv2
import pprint
import random
import string



def aws_detect(img):
    client = boto3.client('rekognition', region_name='us-east-1')
    img_bytes = img
    response = client.detect_faces(
        Attributes= ["ALL"],
        Image={ 'Bytes': img_bytes }
    )
    if list(response['FaceDetails']):
        sorted_emos = sorted(response['FaceDetails'][0]['Emotions'], key=lambda k: k['Confidence'], reverse=True)
        return sorted_emos
    else:
        return None
#       return list(map(lambda emotion: {emotion['Type']: emotion['Confidence']}, sorted_emos))

def aws_create_collection():
    if __name__ == '__main__':
        client = boto3.client('rekognition', region_name='us-east-1')
    response = client.create_collection(
        CollectionId="sei727"
    )
    print(response)

def aws_delete_collection():
    if __name__ == '__main__':
        client = boto3.client('rekognition', region_name='us-east-1')
    response = client.delete_collection(
        CollectionId="sei727"
    )
    print(response)

def add_faces_to_collection(img):
    random_str = ''.join(random.choice(string.ascii_letters) for i in range(8))
    client = boto3.client('rekognition', region_name='us-east-1')
    img_bytes = img
    # with open('main/sei727/Gabriela.png', 'rb') as img_b:
    #     img_bytes = img_b.read()
    try:
        response = client.index_faces(
            CollectionId="sei727",
            DetectionAttributes=["ALL"],
            ExternalImageId=random_str,
            Image={ 'Bytes': img_bytes },
            MaxFaces=1,
            QualityFilter="LOW"
        )
    except Exception as e:
        print(str(e))
        return None
    else:
        if list(response['FaceRecords']):
            face = response['FaceRecords'][0]['Face']
            face_id = face['FaceId']
            external_image_id = face['ExternalImageId']
            print('in the faces', external_image_id, face_id)
            return [external_image_id, face_id]


def search_face_in_faces(img):
    client = boto3.client('rekognition', region_name='us-east-1')
    img_bytes = img
    # with open('main/sei727/Gabriela.png', 'rb') as img_b:
    #     img_bytes = img_b.read()
    try:
        response = client.search_faces_by_image(
            CollectionId="sei727",
            FaceMatchThreshold=75.0,
            Image={ 'Bytes': img_bytes },
            MaxFaces=1,
            QualityFilter="LOW"
        )
    except Exception as e:
        print(str(e))
        return None
    else:
        if list(response['FaceMatches']):
            return [response['FaceMatches'][0]['Face']['ExternalImageId'], response['FaceMatches'][0]['Face']['FaceId']]

def aws_delete_faces(faceIds):
    if __name__ == '__main__':
        client = boto3.client('rekognition', region_name='us-east-1')
    response = client.delete_faces(
        CollectionId="sei727",
        FaceIds=faceIds
    )
    print(response)

def aws_list_faces():
    if __name__ == '__main__':
        client = boto3.client('rekognition', region_name='us-east-1')
    response = client.list_faces(
        CollectionId="sei727",
        MaxResults=30
    )
    pprint.pprint(list(map(lambda face: face['FaceId'], list(response['Faces']))))
