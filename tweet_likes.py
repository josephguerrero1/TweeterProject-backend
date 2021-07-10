from flask import request, Response
import dbhelpers
import json
import traceback


class Tweet_likes:

    # Get Tweet Likes

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

    # Like Tweet

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

        tweet_like_id = dbhelpers.run_insert_statement(
            "INSERT INTO tweet_like (tweet_id, user_id) VALUES (?, ?)", [
                tweetId, userId]
        )

        if(tweet_like_id == None):
            return Response("Tweet ID is invalid", mimetype="text/plain", status=500)
        else:
            return Response(status=204)
    # Note: Catch error for when if the user has already liked the tweet

    # Unlike Tweet

    def unlike_tweet():
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

        tweet_like_id = dbhelpers.run_insert_statement(
            "INSERT INTO tweet_like (tweet_id, user_id) VALUES (?, ?)", [
                tweetId, userId]
        )

        if(tweet_like_id == None):
            return Response("Tweet ID is invalid", mimetype="text/plain", status=500)
        else:
            return Response(status=204)
