from flask import Flask, request, Response
import dbhelpers
import json
import traceback
import sys
import secrets

app = Flask(__name__)

# Add try and except block statements for each decoration
# Do better error catching (In what ways can the code error)
# Add dictionaries to app decorators
# Remove int(), add .get() for optional


@app.get("/api/users")
def get_users():
    userId = request.args.get('userId')

    if userId:
        user_info = dbhelpers.run_select_statement(
            "SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE id = ?", [userId])

        email = user_info[0][1]
        username = user_info[0][2]
        bio = user_info[0][3]
        birthdate = user_info[0][4]
        imageUrl = user_info[0][5]
        bannerUrl = user_info[0][6]

        user = [{"userId": userId, "email": email, "username": username, "bio": bio, "birthdate": birthdate, "imageUrl": imageUrl, "bannerUrl": bannerUrl
                 }]
        if(user == None):
            return Response("Failed to GET user", mimetype="text/plain", status=500)
        else:
            user_json = json.dumps(user, default=str)
            return Response(user_json, mimetype="application/json", status=200)
    else:
        all_users = dbhelpers.run_select_statement(
            "SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user")

        empty_user = []

        for user in all_users:
            userId = user[0]
            email = user[1]
            username = user[2]
            bio = user[3]
            birthdate = user[4]
            imageUrl = user[5]
            bannerUrl = user[6]

            user_dictionary = {"userId": userId, "email": email, "username": username, "bio": bio, "birthdate": birthdate, "imageUrl": imageUrl, "bannerUrl": bannerUrl
                               }

            empty_user.append(user_dictionary)

        if(all_users == None):
            return Response("Failed to GET all users", mimetype="text/plain", status=500)
        else:
            all_users_json = json.dumps(empty_user, default=str)
            return Response(all_users_json, mimetype="application/json", status=200)


@app.get("/api/tweets")
def get_tweets():
    userId = request.args.get('userId')

    if userId:
        tweet = dbhelpers.run_select_statement(
            "SELECT t.id, t.user_id, u.username, t.content, t.createdAt, u.imageUrl, t.tweetimage_url FROM `user` u INNER JOIN tweet t ON u.id = t.user_id WHERE t.user_id = ?", [userId])

        if(tweet == None):
            return Response("Failed to GET tweet", mimetype="text/plain", status=500)
        else:
            tweet_json = json.dumps(tweet, default=str)
            return Response(tweet_json, mimetype="application/json", status=200)
    else:
        all_tweets = dbhelpers.run_select_statement(
            "SELECT t.id, t.user_id, u.username, t.content, t.createdAt, u.imageUrl, t.tweetimage_url FROM `user` u INNER JOIN tweet t ON u.id = t.user_id")

        if(all_tweets == None):
            return Response("Failed to GET all tweets", mimetype="text/plain", status=500)
        else:
            all_tweets_json = json.dumps(all_tweets, default=str)
            return Response(all_tweets_json, mimetype="application/json", status=200)


@app.get("/api/tweet-likes")
def get_tweet_likes():
    tweetId = int(request.args['tweetId'])

    if tweetId:
        tweet_likes = dbhelpers.run_select_statement(
            "SELECT tl.tweet_id, tl.user_id, u.username FROM `user` u INNER JOIN tweet_like tl ON u.id = tl.user_id WHERE tweet_id = ?", [tweetId])

        if(tweet_likes == None):
            return Response("Failed to GET tweet likes", mimetype="text/plain", status=500)
        else:
            tweet_likes_json = json.dumps(tweet_likes, default=str)
            return Response(tweet_likes_json, mimetype="application/json", status=200)
    else:
        all_tweet_likes = dbhelpers.run_select_statement(
            "SELECT tl.tweet_id, tl.user_id, u.username FROM `user` u INNER JOIN tweet_like tl ON u.id = tl.user_id")

        if(all_tweet_likes == None):
            return Response("Failed to GET all tweet likes", mimetype="text/plain", status=500)
        else:
            all_tweet_likes_json = json.dumps(all_tweet_likes, default=str)
            return Response(all_tweet_likes_json, mimetype="application/json", status=200)


@app.get("/api/comments")
def get_comments():
    tweetId = int(request.args['tweetId'])
    comments = dbhelpers.run_select_statement(
        "SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.createdAt FROM `user` u INNER JOIN comment c ON u.id = c.user_id WHERE c.tweet_id = ?", [tweetId])

    if(comments == None):
        return Response("Failed to GET comments", mimetype="text/plain", status=500)
    else:
        comments_json = json.dumps(comments, default=str)
        return Response(comments_json, mimetype="application/json", status=200)


@app.get("/api/comment-likes")
def get_comment_likes():
    commentId = int(request.args['commentId'])

    if commentId:
        comment_likes = dbhelpers.run_select_statement(
            "SELECT c.id, c.user_id, u.username FROM `user` u INNER JOIN comment c ON u.id = c.user_id WHERE c.id = ?", [commentId])

        if(comment_likes == None):
            return Response("Failed to GET comment likes", mimetype="text/plain", status=500)
        else:
            comment_likes_json = json.dumps(comment_likes, default=str)
            return Response(comment_likes_json, mimetype="application/json", status=200)
    else:
        all_comment_likes = dbhelpers.run_select_statement(
            "SELECT c.id, c.user_id, u.username FROM `user` u INNER JOIN comment c ON u.id = c.user_id")

        if(all_comment_likes == None):
            return Response("Failed to GET all comment likes", mimetype="text/plain", status=500)
        else:
            all_comment_likes_json = json.dumps(all_comment_likes, default=str)
            return Response(all_comment_likes_json, mimetype="application/json", status=200)


@app.get("/api/follows")
def get_user_follows():
    userId = int(request.args['userId'])

    user_follows = dbhelpers.run_select_statement(
        "SELECT f.followed_id, u.email, u.username, u.bio, u.birthdate, u.imageUrl, u.bannerUrl FROM `user` u INNER JOIN follow f ON u.id = f.followed_id WHERE f.user_id= ?", [userId])

    if(user_follows == None):
        return Response("Failed to GET user follows", mimetype="text/plain", status=500)
    else:
        user_follows_json = json.dumps(user_follows, default=str)
        return Response(user_follows_json, mimetype="application/json", status=200)


@app.get("/api/followers")
def get_user_followers():
    userId = int(request.args['userId'])

    user_followers = dbhelpers.run_select_statement(
        "SELECT f.user_id, u.email, u.username, u.bio, u.birthdate, u.imageUrl, u.bannerUrl FROM `user` u INNER JOIN follow f ON u.id = f.user_id WHERE f.followed_id= ?", [userId])

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

        newUser = {"userId": userId, "email": email, "username": username, "bio": bio,
                   "birthdate": birthdate, "imageUrl": imageUrl, "bannerUrl": bannerUrl, "loginToken": loginToken}
        newUser_json = json.dumps(newUser, default=str)
        return Response(newUser_json, mimetype="application/json", status=201)


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

    user_id = dbhelpers.run_select_statement(
        "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
            loginToken]
    )

    if(user_id == None):
        return Response("Invalid Login Token", mimetype="text/plain", status=500)
    else:
        userId = user_id[0][0]

    follow_id = dbhelpers.run_insert_statement(
        "INSERT INTO follow (user_id, followed_id) VALUES (?, ?)", [
            userId, followId]
    )

    if(follow_id == None):
        return Response("Follow ID is invalid", mimetype="text/plain", status=500)
    else:

        return Response(status=204)


@app.post("/api/tweets")
def post_tweet():
    loginToken = request.json['loginToken']
    content = request.json['content']
    imageUrl = request.json.get('imageUrl')

    user_id = dbhelpers.run_select_statement(
        "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
            loginToken]
    )

    if(user_id == None):
        return Response("Invalid Login Token", mimetype="text/plain", status=500)
    else:
        userId = user_id[0][0]

    tweetId = dbhelpers.run_insert_statement(
        "INSERT INTO tweet (content, imageUrl) VALUES (?, ?)"), [content, imageUrl]

    if(tweetId == None):
        return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
    else:

        tweet_info = dbhelpers.run_select_statement(
            "SELECT u.username, u.imageUrl, t.createdAt FROM `user` u INNER JOIN tweet t ON u.id = t.user_id WHERE tweet_id = ?", [
                tweetId]
        )

        username = tweet_info[0][0]
        userImageUrl = tweet_info[0][1]
        createdAt = tweet_info[0][2]

        tweet = {"tweetId": tweetId, "userId": userId, "username": username, "userImageUrl": userImageUrl, "content": content, "createdAt": createdAt, "imageUrl": imageUrl
                 }

        tweet_json = json.dumps(tweet, default=str)
        return Response(tweet_json, mimetype="application/json", status=201)


@app.post("/api/tweet-likes")
def like_tweet():
    loginToken = request.json['login_Token']
    tweetId = request.json['tweetId']

    user_id = dbhelpers.run_select_statement(
        "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
            loginToken]
    )

    if(user_id == None):
        return Response("Invalid Login Token", mimetype="text/plain", status=500)
    else:
        userId = user_id[0][0]

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


@app.delete("/api/users")
def delete_user():
    loginToken = request.json['loginToken']
    password = request.json['password']

    Login_combo = dbhelpers.run_select_statement(
        "SELECT u.password, us.loginToken FROM `user` u INNER JOIN user_session us ON u.id=us.user_id WHERE us.loginToken= ?", [
            loginToken]
    )

    if(password == Login_combo[0][0]):
        rowcount = dbhelpers.run_delete_statement(
            "DELETE FROM users WHERE loginToken = ?", [loginToken]
        )
    else:
        return "Wrong password!"

    if(rowcount == 1):
        return "User has been deleted!"
    elif(rowcount == 0):
        return "Error, loginToken does not exist!"
    elif(rowcount == None):
        return "Database Error"


@app.delete("/api/login")
def logout():
    loginToken = request.json['loginToken']

    rowcount = dbhelpers.run_delete_statement(
        "DELETE FROM user_session WHERE loginToken = ?", [loginToken]
    )

    if(rowcount == 1):
        return "User has been logged out!"
    elif(rowcount == 0):
        return "Error, loginToken does not exist!"
    elif(rowcount == None):
        return "Database Error"


@app.delete("/api/follows")
def unfollow_user():
    loginToken = request.json['loginToken']
    followId = request.json['followId']

    rowcount = dbhelpers.run_delete_statement(
        "DELETE FROM follow WHERE "
    )


@app.delete("/api/tweets")
def delete_tweet():
    loginToken = request.json['loginToken']
    tweetId = request.json['tweetId']


@app.delete("/api/tweet-likes")
def unlike_tweet():
    loginToken = request.json['loginToken']
    tweetId = request.json['tweetId']


@app.delete("/api/comments")
def delete_comments():
    loginToken = request.json['loginToken']
    commentId = request.json['commentId']


@app.delete("/api/comment-likes")
def unlike_comment():
    loginToken = request.json['loginToken']
    commentId = request.json['commentId']


@app.patch("/api/users")
def update_user():
    loginToken = request.json['loginToken']
    bio = request.json['bio']
    birthdate = request.json['birthdate']
    email = request.json['email']
    username = request.json['username']
    bannerUrl = request.json['bannerUrl']
    imageUrl = request.json['imageUrl']

    if(email != None):
        # run update
        # Run individually
        return True


@app.patch("/api/tweets")
def update_tweet():
    loginToken = request.json['loginToken']
    tweetId = request.json['tweetId']
    content = request.json['content']

    # Write if statement
    tweet = dbhelpers.run_select_statement(
        "SELECT us.loginToken, t.id, t.content FROM user_session us INNER JOIN tweet t ON us.user_id=t.user_id WHERE us.loginToken = ? AND t.id = ?", [
            loginToken, tweetId]
    )

    rowcount = dbhelpers.run_update_statement(
        "UPDATE tweet SET content = ? WHERE id = ?", [content, tweetId]
    )


@app.patch("/api/comments")
def update_comment():
    loginToken = request.json['loginToken']
    commentId = request.json['commentId']
    content = request.json['content']

    # Write if statement
    comment = dbhelpers.run_select_statement(
        "SELECT us.loginToken, c.id, c.content FROM user_session us INNER JOIN comment c ON us.user_id = c.user_id WHERE us.loginToken = ? AND c.id = ?", [
            loginToken, commentId]
    )

    rowcount = dbhelpers.run_update_statement(
        "UPDATE comment SET content = ? WHERE id = ?", [content, commentId]
    )


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
