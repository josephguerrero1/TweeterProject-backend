from flask import Flask, request, Response
import dbhelpers
import json
import traceback
import sys
import secrets

app = Flask(__name__)

# To do for all app.get decorations
# Add try and except block
# Write if check to see if the userId is there because userId is optional


@app.get("/api/users")
def get_users():
    params = int(request.args['userId'])
    users = dbhelpers.run_select_statement(
        "SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE id = ?", [params])

    if(users == None):
        return Response("Failed to GET users", mimetype="text/plain", status=500)
    else:
        users_json = json.dumps(users, default=str)
        return Response(users_json, mimetype="application/json", status=200)


@app.get("/api/tweets")
def get_tweets():
    params = int(request.args['userId'])
    tweets = dbhelpers.run_select_statement(
        "SELECT t.id, t.user_id, u.username, t.content, t.createdAt,u.imageUrl, t.tweetimage_url FROM `user` u INNER JOIN tweet t ON u.id=t.user_id WHERE u.id = ?", [params])

    if(tweets == None):
        return Response("Failed to GET tweets", mimetype="text/plain", status=500)
    else:
        tweets_json = json.dumps(tweets, default=str)
        return Response(tweets_json, mimetype="application/json", status=200)


@app.get("/api/tweet-likes")
def get_tweet_likes():
    params = int(request.args['tweetId'])
    tweet_likes = dbhelpers.run_select_statement(
        "SELECT tl.tweet_id, tl.user_id, u.username FROM `user` u INNER JOIN tweet_like tl ON u.id = tl.user_id WHERE tl.tweet_id = ?", [params])

    if(tweet_likes == None):
        return Response("Failed to GET tweet likes", mimetype="text/plain", status=500)
    else:
        tweet_likes_json = json.dumps(tweet_likes, default=str)
        return Response(tweet_likes_json, mimetype="application/json", status=200)


@app.get("/api/comments")
def get_comments():
    params = int(request.args['tweetId'])
    comments = dbhelpers.run_select_statement(
        "SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.createdAt FROM `user` u INNER JOIN comment c ON u.id = c.user_id WHERE c.tweet_id = ?", [params])

    if(comments == None):
        return Response("Failed to GET comments", mimetype="text/plain", status=500)
    else:
        comments_json = json.dumps(comments, default=str)
        return Response(comments_json, mimetype="application/json", status=200)


@app.get("/api/comment-likes")
def get_comment_likes():
    params = int(request.args['commentId'])
    comment_likes = dbhelpers.run_select_statement(
        "SELECT cl.comment_id, cl.user_id, u.username FROM `user` u INNER JOIN comment_like cl ON u.id=cl.user_id WHERE cl.comment_id = ?", [params])

    if(comment_likes == None):
        return Response("Failed to GET comment likes", mimetype="text/plain", status=500)
    else:
        comment_likes_json = json.dumps(comment_likes, default=str)
        return Response(comment_likes_json, mimetype="application/json", status=200)


@app.get("/api/follows")
def get_user_follows():
    params = int(request.args['userId'])
    user_follows = dbhelpers.run_select_statement("", [params])

    if(user_follows == None):
        return Response("Failed to GET user follows", mimetype="text/plain", status=500)
    else:
        user_follows_json = json.dumps(user_follows, default=str)
        return Response(user_follows_json, mimetype="application/json", status=200)


@app.get("/api/followers")
def get_user_followers():
    params = int(request.args['userId'])
    user_followers = dbhelpers.run_select_statement("", [params])

    if(user_followers == None):
        return Response("Failed to GET user followers", mimetype="text/plain", status=500)
    else:
        user_followers_json = json.dumps(user_followers, default=str)
        return Response(user_followers_json, mimetype="application/json", status=200)


@app.post("/api/users")
def post_user():
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']
    bio = request.json['bio']
    birthdate = request.json['birthdate']
    imageUrl = request.json.get('imageUrl')
    bannerUrl = request.json.get('bannerUrl')
    loginToken = secrets.token_urlsafe(50)

    userId = dbhelpers.run_insert_statement("INSERT INTO user(email, username, password, bio, birthdate, imageUrl, bannerUrl) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                            [email, username, password, bio, birthdate, imageUrl, bannerUrl])
    if(userId == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        user = [userId, email, username, bio,
                birthdate, imageUrl, bannerUrl, loginToken]
        user_json = json.dumps(user, default=str)
        return Response(user_json, mimetype="application/json", status=201)


@app.post("/api/login")
def user_login():
    email = request.json['email']
    password = request.json['password']

    checkUser = dbhelpers.run_select_statement(
        "SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE email = ?, password = ?", [
            email, password]
    )

    if(len(checkUser) == 1):
        loginToken = secrets.token_urlsafe(50)
        user_id = checkUser[0][0]
        userId = dbhelpers.run_insert_statement("INSERT INTO user_session (user_id, loginToken) VALUES (?, ?)",
                                                [user_id, loginToken])
    else:
        return "Login did not work"

    if(userId == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        username = checkUser[0][2]
        bio = checkUser[0][3]
        birthdate = checkUser[0][4]
        imageUrl = checkUser[0][5]
        bannerUrl = checkUser[0][6]

        logged_in_user = {"userId": userId, "email": email, "username": username, "bio": bio,
                          "birthdate": birthdate, "loginToken": loginToken, "imageUrl": imageUrl, "bannerUrl": bannerUrl}
        logged_in_user_json = json.dumps(logged_in_user, default=str)
        return Response(logged_in_user_json, mimetype="application/json", status=201)


@app.post("/api/follows")
def follow_user():
    loginToken = request.json['loginToken']
    followId = request.json['followId']
    # userId =

    userId = dbhelpers.run_insert_statement(
        "INSERT INTO follow (user_id, followed_id) VALUES (?, ?)"), [userId, followId]

    if(userId == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        user = "User has been followed!"
        user_json = json.dumps(user, default=str)
        return Response(user_json, mimetype="application/json", status=204)


@app.post("/api/tweets")
def post_tweet():
    loginToken = request.json['loginToken']
    content = request.json['content']
    imageUrl = request.json['imageUrl']

    userId = dbhelpers.run_insert_statement(
        "INSERT INTO tweet (content, imageUrl) VALUES (?, ?)"), [content, imageUrl]

    if(userId == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:

        params = request.args['loginToken']

        tweet_info = dbhelpers.run_select_statement(
            "SELECT t.id, t.user_id, u.username, u.imageUrl, t.content, t.createdAt, t.tweetimage_url FROM user_session us INNER JOIN `user` u ON us.user_id=u.id INNER JOIN tweet t ON u.id=t.user_id WHERE us.loginToken = ?", [
                params]
        )
        tweet_info_json = json.dumps(tweet_info, default=str)
        return Response(tweet_info_json, mimetype="application/json", status=201)


@app.post("/api/tweet-likes")
def like_tweet():
    loginToken = request.json['login_Token']
    tweetId = request.json['tweetId']
    # userId =

    userId = dbhelpers.run_insert_statement(
        "INSERT INTO tweet_like (user_id, tweet_id) VALUES (?, ?)", [
            userId, tweetId]
    )

    if(userId == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        tweet_like = "Tweet has been liked!"
        tweet_like_json = json.dumps(tweet_like, default=str)
        return Response(tweet_like_json, mimetype="application/json", status=201)


@app.post("/api/comments")
def post_comment():
    loginToken = request.json['loginToken']
    tweetId = request.json['tweetId']
    content = request.json['content']

    userId = dbhelpers.run_insert_statement(
        "INSERT INTO comment (tweet_id, content) VALUES (?, ?)", [
            tweetId, content]
    )

    if(userId == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:
        comment = "Comment has been posted!"
        comment_json = json.dumps(comment, default=str)
        return Response(comment_json, mimetype="application/json", status=201)


@app.post("/api/comment-likes")
def like_comment():
    loginToken = request.json['loginToken']
    commentId = request.json['commentId']


# @app.delete("/api/users")
@app.delete("/api/login")
def logout():
    loginToken = request.json['loginToken']

    rowcount = dbhelpers.run_delete_statement(
        "DELETE FROM user_session WHERE loginToken = ?", [loginToken]
    )

    # if(rowcount == 1):
    #     # success
    # elif(rowcount == 0):
    #     # loginToken did not exist
    # elif(rowcount == None):
    #     # database error


# @app.delete("/api/follows")
# @app.delete("/api/tweets")
# @app.delete("/api/tweet-likes")
# @app.delete("/api/comments")
# @app.delete("/api/comment-likes")
# @app.patch("/api/users")
# @app.patch("/api/tweets")
# @app.patch("/api/comments")
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
