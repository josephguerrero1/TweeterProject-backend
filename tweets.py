from flask import request, Response
import dbhelpers
import json
import traceback


class Tweets:

    # Get Tweets

    def get_tweets():
        userId = request.args.get('userId')

        if userId:
            tweet = dbhelpers.run_select_statement(
                "SELECT t.id, t.user_id, u.username, t.content, t.createdAt, u.imageUrl, t.tweetimage_url FROM `user` u INNER JOIN tweet t ON u.id = t.user_id WHERE t.user_id = ?", [userId])

            tweetId = tweet[0]
            email = tweet[0][1]
            username = tweet[0][2]
            bio = tweet[0][3]
            birthdate = tweet[0][4]
            imageUrl = tweet[0][5]
            bannerUrl = tweet[0][6]

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

    # Post Tweet

    def post_tweet():
        # Data sent by the user

        loginToken = request.json['loginToken']
        content = request.json['content']
        imageUrl = request.json.get('imageUrl')

        # Using the loginToken to get the userId of the user via SELECT STATEMENT

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        # If the user_id is None, it will return an invalid Logintoken error

        # Else, a variable of userId is created which is taken from the user_id table

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

        # Inserting into tweet table

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

    # Update Tweet

    def update_tweet():
        loginToken = request.json['loginToken']
        tweetId = request.json['tweetId']
        content = request.json['content']

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=500)
        else:
            userId = user_id[0][0]

        rowcount = dbhelpers.run_update_statement(
            "UPDATE tweet t SET t.content = ? WHERE t.id = ? AND t.user_id = ?", [
                content, tweetId, userId]
        )

        if(rowcount == 1):
            updated_tweet = {
                "tweetId": tweetId,
                "content": content
            }
            updated_tweet_json = json.dumps(updated_tweet, default=str)
            return Response(updated_tweet_json, mimetype="application/json", status=200)
        elif(rowcount == None):
            return Response("Database Error", mimetype="text/plain", status=500)

    # Delete Tweet

    def delete_tweet():
        loginToken = request.json['loginToken']
        tweetId = request.json['tweetId']
