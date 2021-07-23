import twitter
import wget
from PIL import Image

def download_images(twitterApi, mention):
    try:
        media1 = twitterApi.GetStatus(mention.AsDict()['in_reply_to_status_id'])._json['entities']['media'][0]['media_url']
        print(media1)
        wget.download(media1, out = 'images/downloaded/')
        media2 = twitterApi.GetStatus(twitterApi.GetStatus(mention.AsDict()['in_reply_to_status_id']).AsDict()['in_reply_to_status_id']).AsDict()['media'][0]['media_url']
        wget.download(media2, out = 'images/downloaded/')
        print(media2)
        return ('images/downloaded/' + media1.split('/')[-1], 'images/downloaded/' +  media2.split('/')[-1])
    except:
        print('No Media')
        return None


def resize_image(image_location):
    image = Image.open(image_location)
    if(image.size[0] > image.size[1]):
        image = image.resize((int(512 / image.size[1] * image.size[0]), 512))
        image = image.crop((0,0, 512, 512))
    else:
        image = image.resize((512, int(512 / image.size[0] * image.size[1])))
        image = image.crop((0,0, 512, 512))
    return image