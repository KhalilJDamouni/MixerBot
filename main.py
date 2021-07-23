import twitter
import wget
from model import *
from img_funcs import *
import csv
import time

if __name__ == '__main__':

    #Get Secret Twitter API Keys
    content = []
    with open('secrets.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            content.append(row)
    
    consumer_key        = content[1][0]
    consumer_secret     = content[1][1]
    access_token        = content[1][2]
    access_token_secret = content[1][3]

    twitterApi = twitter.Api(consumer_key=consumer_key,
                             consumer_secret=consumer_secret,
                             access_token_key=access_token,
                             access_token_secret=access_token_secret)

    #Infinite loop: Checks for new mentions, if none, sleeps for 30 seconds, then checks again (might change the number from 30 seconds)
    last_id = None
    while(True):
        mentions = twitterApi.GetMentions(count=100, since_id = last_id)
        if(len(mentions) > 0):
            print("Responding to ", len(mentions), " mentions.")
            last_id = mentions[-1].id
            for m in mentions:
                #Check if the mention is from the bot. If so, ignore
                if(m.user.screen_name == 'ImgMixerBot'):
                    continue

                #Dowwnload Images
                images = download_images(twitterApi, m)

                #Check if valid thread
                if(images == None):
                    print("Invalid Mention")
                    continue
                output_name = images[0].split('/')[-1].replace('.jpg', '') + images[1].split('/')[-1].replace('.jpg', '') + '.jpg'

                #Create Mix
                mix(images[0], images[1])

                #Respond to Tweet
                toAnnotate = twitterApi.GetStatus(mentions[0].id)
                respondToTweet = mentions[0]

                user = respondToTweet.user
                text = 'Neural Style Transfer Done!'
                exclude=[x.id for x in respondToTweet.user_mentions if x.id not in [user.id]]
                media = twitterApi.UploadMediaSimple('images/done/' + output_name)

                twitterApi.PostUpdate(
                    status='@{user.screen_name} {text}'.format(user=user, text=text),
                    in_reply_to_status_id=respondToTweet.id,
                    exclude_reply_user_ids=exclude,
                    media = media,
                    verify_status_length=False)

        else:
            time.sleep(30)