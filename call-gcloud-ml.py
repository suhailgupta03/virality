
from oauth2client.client import GoogleCredentials
import googleapiclient.discovery
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import sys
import json
import pickle
import argparse

X_SCALER_PKL = "xscaler.pkl"
Y_SCALER_PKL = "yscaler.pkl"


parser = argparse.ArgumentParser(description='Calculate virality score')

parser.add_argument(
    '--sentiment',
    type=float,
    help="Sentiment score",
    required=True
)

parser.add_argument(
    '--post_length',
    type=int,
    help="Post Length",
    required=True
)

parser.add_argument(
    '--hash_tag_count',
    type=int,
    help="Number of hash tags",
    required=True
)

parser.add_argument(
    '--content_url_count',
    type=int,
    help="Number of content url(s)",
    required=True
)

parser.add_argument(
    '--like_count',
    type=int,
    help="Number of likes",
    required=True
)

parser.add_argument(
    '--share_count',
    type=int,
    help="Number of shares",
    required=True
)

parser.add_argument(
    '--comment_count',
    type=int,
    help="Number of comments",
    required=True
)

parser.add_argument(
    '--followers_count',
    type=int,
    help="Number of followers",
    required=True
)

parser.add_argument(
    '--following_count',
    type=int,
    help="Number of following",
    required=True
)

parser.add_argument(
    '--tweet_count',
    type=int,
    help="Number of user tweets",
    required=True
)

parser.add_argument(
    '--gender',
    type=int,
    help="Gender (-1,0,1)",
    required=True
)


parser.add_argument(
    '--seconds_elapsed',
    type=int,
    help="Number of seconds elapsed since the post was published",
    required=True
)

args = parser.parse_args()

test_record = [{
    "sentiment": args.sentiment,
    "postLength": args.post_length,
    "hashTagCount": args.hash_tag_count,
    "contentURLCount": args.content_url_count,
    "likeCount": args.like_count,
    "shareCount": args.share_count,
    "commentCount": args.comment_count,
    "followersCount": args.followers_count,
    "followingCount": args.following_count,
    "tweetCount": args.tweet_count,
    "gender": args.gender,
    "secondsElapsed": args.seconds_elapsed
}]

with open(X_SCALER_PKL, 'rb') as input:
    X_scaler = pickle.load(input)

with open(Y_SCALER_PKL, 'rb') as input:
    Y_scaler = pickle.load(input)

test_frame = pd.DataFrame(columns=test_record[0].keys())

for index in range(len(test_record)):
    test_frame.loc[index] = list(test_record[index].values())


scaled_input = X_scaler.transform(test_frame.values)


# Change this values to match your project
PROJECT_ID = "tensorflow-class-214013"
MODEL_NAME = "virality"
CREDENTIALS_FILE = "credentials.json"

inputs_for_prediction = []

for index, _ in enumerate(scaled_input):
    inputs_for_prediction.append({
        "input": list(scaled_input[index])
    })


# Connect to the Google Cloud-ML Service
credentials = GoogleCredentials.from_stream(CREDENTIALS_FILE)
service = googleapiclient.discovery.build('ml', 'v1', credentials=credentials)

# # Connect to our Prediction Model
name = 'projects/{}/models/{}'.format(PROJECT_ID, MODEL_NAME)
response = service.projects().predict(
    name=name,
    body={'instances': inputs_for_prediction}
).execute()

# # Report any errors
if 'error' in response:
    raise RuntimeError(response['error'])

# # Grab the results from the response object
results = response['predictions']

predicted = []
for index in range(len(results)):
    predicted.append(Y_scaler.inverse_transform(results[index]['virality'][0]))

print(json.dumps({
    "score": predicted[0][0][0]
}))

# python call-gcloud-ml.py --sentiment 0 --post_length 130 --hash_tag_count 0 --content_url_count 1 --like_count 1528 --share_count 31 --comment_count 0 --followers_count 25229 --following_count 243 --tweet_count 45542 --gender -1 --seconds_elapsed 5812868
