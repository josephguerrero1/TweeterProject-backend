from flask import request, Response
import dbhelpers
import json
import traceback


class Tweet_likes:

    # Get Tweet Likes

    def get_tweet_likes():
        tweetId = request.args.get('tweetId')

        if tweetId:
            tweet_likes_info = dbhelpers.run_select_statement(
                "SELECT tl.user_id, u.username FROM `user` u INNER JOIN tweet_like tl ON u.id = tl.user_id WHERE tl.tweet_id = ?", [tweetId])

            userId = tweet_likes_info[0][1]
            username = tweet_likes_info[0][2]

            tweet_like = [{
                "tweetId": tweetId,
                "userId": userId,
                "username": username
            }]
            if(tweet_like == None):
                return Response("Failed to GET tweet like information", mimetype="text/plain", status=500)
            else:
                tweet_like_json = json.dumps(tweet_like, default=str)
                return Response(tweet_like_json, mimetype="application/json", status=200)
        else:
            all_tweet_likes = dbhelpers.run_select_statement(
                "SELECT tl.tweet_id, tl.user_id, u.username FROM `user` u INNER JOIN tweet_like tl ON u.id = tl.user_id")

            empty_tweet_like = []

            for tweet_like in all_tweet_likes:
                tweetId = all_tweet_likes[0]
                userId = all_tweet_likes[1]
                username = all_tweet_likes[2]

                tweet_like = {
                    "tweetId": tweetId,
                    "userId": userId,
                    "username": username
                }

                empty_tweet_like.append(tweet_like)

            if(all_tweet_likes == None):
                return Response("Failed to GET all tweet likes information", mimetype="text/plain", status=500)
            else:
                all_tweet_likes_json = json.dumps(
                    all_tweet_likes, default=str)
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
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

            tweet_like_id = dbhelpers.run_insert_statement(
                "INSERT INTO tweet_like (tweet_id, user_id) VALUES (?, ?)", [
                    tweetId, userId]
            )

            if(tweet_like_id == None):
                return Response("Failed to like tweet", mimetype="text/plain", status=500)
            else:
                return Response(status=201)

    # Unlike Tweet

    def unlike_tweet():
        loginToken = request.json['login_Token']
        tweetId = request.json['tweetId']

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

            rowcount = dbhelpers.run_delete_statement(
                "DELETE FROM tweet_like tl WHERE tl.tweet_id = ? AND tl.user_id = ?", [
                    tweetId, userId]
            )

            if(rowcount == None):
                return Response("Failed to unlike tweet", mimetype="text/plain", status=500)
            elif(rowcount == 1):
                return Response(status=204)
