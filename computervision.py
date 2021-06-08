from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import os

# Create a Microsoft Computer Vision instance, which can be done for free on a student account.
# https://azure.microsoft.com/nl-nl/services/cognitive-services/computer-vision/

subscription_key = "PASTE_YOUR_COMPUTER_VISION_SUBSCRIPTION_KEY_HERE"
endpoint = "PASTE_YOUR_COMPUTER_VISION_ENDPOINT_HERE"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "static")

# Call API
def get_image_analysis(image):

    description = get_image_description(image)
    tags = get_image_tags(image)

    return description, tags


def get_image_description(image):
    local_image_path = os.path.join (images_folder, image)
    local_image = open(local_image_path, "rb")
    description_result = computervision_client.describe_image_in_stream(local_image)
    local_image.close
    
    # Get the captions (descriptions) from the response, with confidence level
    print("Description of local image: ")
    # Open local image file
    
    res = "No description detected."
    if (len(description_result.captions) == 0):
        print(res)
        return res
    else:
        
        for caption in description_result.captions:
            confidence = caption.confidence * 100
            res = caption.text
            print("'{}' with confidence {:.2f}%".format(res, confidence))
            # We only need the first (often the only) description
            return res


def get_image_tags(image):
    print("===== Tag an Image - local =====")
    # Open local image file
    local_image_path = os.path.join (images_folder, image)
    local_image = open(local_image_path, "rb")
    # Call API local image
    tags_result_local = computervision_client.tag_image_in_stream(local_image)
    local_image.close

    # Print results with confidence score
    print("Tags in the local image: ")
    res = "No tags detected."
    if (len(tags_result_local.tags) == 0):
        print(res)
        return res
    else:
        res = ""
        for tag in tags_result_local.tags:
            confidence = tag.confidence * 100
            if confidence > 80:
                print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
                res += tag.name + ","

        res = res[:-1]
        return res


if __name__ == "__main__":
    get_image_analysis("18.jpg")
