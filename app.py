from flask import Flask
import sys
import users
import login
import follows
import followers
import tweets
import tweet_likes
import comments
import comment_likes

app = Flask(__name__)


class Data:
    def __init__(self):

        # GET
        self.get_users = users.Users.get_users()
        self.get_user_follows = follows.Follows.get_user_follows()
        self.get_user_followers = followers.Followers.get_user_followers()
        self.get_tweets = tweets.Tweets.get_tweets()
        self.get_tweet_likes = tweet_likes.Tweet_likes.get_tweet_likes()
        self.get_comments = comments.Comments.get_comments()
        self.get_comment_likes = comment_likes.Comment_likes.get_comment_likes()

        # POST
        self.post_user = users.Users.post_user()
        self.user_login = login.Login.user_login()
        self.follow_user = follows.Follows.follow_user()
        self.post_tweet = tweets.Tweets.post_tweet()
        self.like_tweet = tweet_likes.Tweet_likes.like_tweet()
        self.post_comment = comments.Comments.post_comment()
        self.like_comment = comment_likes.Comment_likes.like_comment()

        # PATCH
        self.update_user = users.Users.update_user()
        self.update_tweet = tweets.Tweets.update_tweet()
        self.update_comment = comments.Comments.update_comment()

        # DELETE
        self.delete_user = users.Users.delete_user()
        self.user_logout = login.Login.user_logout()
        self.unfollow_user = follows.Follows.unfollow_user()
        self.delete_tweet = tweets.Tweets.delete_tweet()
        self.unlike_tweet = tweet_likes.Tweet_likes.unlike_tweet()
        self.delete_comment = comments.Comments.delete_comment()
        self.unlike_comment = comment_likes.Comment_likes.unlike_comment()


# GET endpoints


@app.get("/api/users")
def get_users():
    return Data.get_users


@app.get("/api/follows")
def get_user_follows():
    return Data.get_user_follows


@app.get("/api/followers")
def get_user_followers():
    return Data.get_user_followers


@app.get("/api/tweets")
def get_tweets():
    return Data.get_tweets


@app.get("/api/tweet-likes")
def get_tweet_likes():
    return Data.get_tweet_likes


@app.get("/api/comments")
def get_comments():
    return Data.get_comments


@app.get("/api/comment-likes")
def get_comment_likes():
    return Data.get_comment_likes


# POST endpoints


@app.post("/api/users")
def post_user():
    return Data.post_user


@app.post("/api/login")
def user_login():
    return Data.user_login


@app.post("/api/follows")
def follow_user():
    return Data.follow_user


@app.post("/api/tweets")
def post_tweets():
    return Data.post_tweets


@app.post("/api/tweet-likes")
def like_tweet():
    return Data.like_tweet


@app.post("/api/comments")
def post_comment():
    return Data.post_comment


@app.post("/api/comment-likes")
def like_comment():
    return Data.like_comment


# PATCH endpoints


@app.patch("/api/users")
def update_user():
    return Data.update_user


@app.patch("/api/tweets")
def update_tweet():
    return Data.update_tweet


@app.patch("/api/comments")
def update_comment():
    return Data.update_comment


# DELETE endpoints


@app.delete("/api/users")
def delete_user():
    return Data.delete_user


@app.delete("/api/login")
def user_logout():
    return Data.user_logout


@app.delete("/api/follows")
def unfollow_user():
    return Data.unfollow_user


@app.delete("/api/tweets")
def delete_tweet():
    return Data.delete_tweet


@app.delete("/api/tweet-likes")
def unlike_tweet():
    return Data.unlike_tweet


@app.delete("/api/comments")
def delete_comment():
    return Data.delete_comment


@app.delete("/api/comment-likes")
def unlike_comment():
    return Data.unlike_comment


# Production Code
if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

if(mode == "production"):
    import bjoern
    print("Bjoern is running.")
    bjoern.run(app, "0.0.0.0", 5017)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    print("Running in testing mode!")
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()
