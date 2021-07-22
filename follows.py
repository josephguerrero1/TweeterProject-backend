from flask import request, Response
import dbhelpers
import json
import traceback


class Follows:

    # Get User Follows

    def get_user_follows():
        userId = request.args['userId']

        all_user_follows = dbhelpers.run_select_statement(
            "SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.imageUrl, u.bannerUrl FROM `user` u INNER JOIN follow f ON u.id=f.followed_id WHERE f.user_id= ?", [userId])

        empty_user_follow = []

        for user_follow in all_user_follows:
            userId = all_user_follows[0]
            email = all_user_follows[1]
            username = all_user_follows[2]
            bio = all_user_follows[3]
            birthdate = all_user_follows[4]
            imageUrl = all_user_follows[5]
            bannerUrl = all_user_follows[6]

            user_follow = {"userId": userId, "email": email, "username": username, "bio": bio, "birthdate": birthdate, "imageUrl": imageUrl, "bannerUrl": bannerUrl
                           }

            empty_user_follow.append(user_follow)

        if(all_user_follows == None):
            return Response("Failed to GET user follows", mimetype="text/plain", status=500)
        else:
            all_user_follows_json = json.dumps(empty_user_follow, default=str)
            return Response(all_user_follows_json, mimetype="application/json", status=200)

    # Follow User

    def follow_user():
        loginToken = request.json['loginToken']
        followId = request.json['followId']

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

            follow_id = dbhelpers.run_insert_statement(
                "INSERT INTO follow (user_id, followed_id) VALUES (?, ?)", [
                    userId, followId]
            )

            if(follow_id == None):
                return Response("Failed to follow user", mimetype="text/plain", status=500)
            else:
                return Response(status=204)

    # Unfollow User

    def unfollow_user():
        loginToken = request.json['loginToken']
        followId = request.json['followId']

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

        rowcount = dbhelpers.run_delete_statement(
            "DELETE from follow f WHERE f.user_id = ? AND f.followed_id = ?", [
                userId, followId]
        )

        if(rowcount == 1):
            return Response(status=204)
        elif(rowcount == None):
            return Response("Failed to unfollow user", mimetype="text/plain", status=500)
