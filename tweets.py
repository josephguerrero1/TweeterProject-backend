from flask import request, Response
import dbhelpers
import json
import traceback


class Tweets:

    # Get Tweets

    def get_tweets():
        userId = request.args.get('userId')

        if userId:
            tweet_info = dbhelpers.run_select_statement(
                "SELECT t.id, u.username, t.content, t.createdAt, u.imageUrl, t.tweetimage_url FROM `user` u INNER JOIN tweet t ON u.id = t.user_id WHERE t.user_id = ?", [userId])

            tweetId = tweet_info[0][0]
            username = tweet_info[0][1]
            content = tweet_info[0][2]
            createdAt = tweet_info[0][3]
            userImageUrl = tweet_info[0][4]
            tweetImageUrl = tweet_info[0][5]

            tweet = [{
                "tweetId": tweetId,
                "userId": userId,
                "username": username,
                "content": content,
                "createdAt": createdAt,
                "userImageUrl": userImageUrl,
                "tweetImageUrl": tweetImageUrl
            }]

            if(tweet_info == None):
                return Response("Failed to GET tweet information", mimetype="text/plain", status=500)
            else:
                tweet_info_json = json.dumps(tweet_info, default=str)
                return Response(tweet_info_json, mimetype="application/json", status=200)
        else:
            all_tweets_info = dbhelpers.run_select_statement(
                "SELECT t.id, t.user_id, u.username, t.content, t.createdAt, u.imageUrl, t.tweetimage_url FROM `user` u INNER JOIN tweet t ON u.id = t.user_id"
            )

            empty_tweet = []

            for tweet in all_tweets_info:
                tweetId = all_tweets_info[0][0]
                userId = all_tweets_info[0][1]
                username = all_tweets_info[0][2]
                content = all_tweets_info[0][3]
                createdAt = all_tweets_info[0][4]
                userImageUrl = all_tweets_info[0][5]
                tweetImageUrl = all_tweets_info[0][6]

                tweet = {
                    "tweetId": tweetId,
                    "userId": userId,
                    "username": username,
                    "content": content,
                    "createdAt": createdAt,
                    "userImageUrl": userImageUrl,
                    "tweetImageUrl": tweetImageUrl
                }

                empty_tweet.append(tweet)

            if(all_tweets_info == None):
                return Response("Failed to GET all of the tweets' information", mimetype="text/plain", status=500)
            else:
                all_tweets_info_json = json.dumps(all_tweets_info, default=str)
                return Response(all_tweets_info_json, mimetype="application/json", status=200)

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
            return Response("Failed to post tweet", mimetype="text/plain", status=500)
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
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

        rowcount = dbhelpers.run_update_statement(
            "UPDATE tweet t SET t.content = ? WHERE t.id = ? AND t.user_id = ?", [
                content, tweetId, userId]
        )

        if(rowcount == 1):
            updated_Tweet = dbhelpers.run_select_statement(
                "SELECT t.id, t.content FROM tweet t WHERE t.id = ? AND t.user_id = ?", [
                    tweetId, userId]
            )

            tweetId = updated_Tweet[0][0]
            content = updated_Tweet[0][1]

            updated_tweet = {
                "tweetId": tweetId,
                "content": content
            }
            updated_tweet_json = json.dumps(updated_tweet, default=str)
            return Response(updated_tweet_json, mimetype="application/json", status=200)
        elif(rowcount == None):
            return Response("Failed to update tweet", mimetype="text/plain", status=500)

    # Delete Tweet

    def delete_tweet():
        loginToken = request.json['loginToken']
        tweetId = request.json['tweetId']

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=500)
        else:
            userId = user_id[0][0]

        rowcount = dbhelpers.run_delete_statement(
            "DELETE FROM tweet t WHERE t.id = ? AND t.user_id = ?", [
                tweetId, userId]
        )

        if(rowcount == 1):
            return Response(status=204)
        elif(rowcount == None):
            return Response("Failed to delete tweet", mimetype="text/plain", status=500)
