from flask import request, Response
import dbhelpers
import json
import traceback


class Follows:

    # Get User Follows

    def get_user_follows():
        userId = request.args['userId']

        all_user_follows = dbhelpers.run_select_statement(
            "SELECT f.followed_id, u.email, u.username, u.bio, u.birthdate, u.imageUrl, u.bannerUrl FROM `user` u INNER JOIN follow f ON u.id = f.followed_id WHERE f.user_id= ?", [userId])

        if(user_follows == None):
            return Response("Failed to GET user follows", mimetype="text/plain", status=500)
        else:
            user_follows_json = json.dumps(user_follows, default=str)
            return Response(user_follows_json, mimetype="application/json", status=200)

    # Follow User

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

    # Unfollow User

    def unfollow_user():
        loginToken = request.json['loginToken']
        followId = request.json['followId']

        rowcount = dbhelpers.run_delete_statement(
            "DELETE FROM follow WHERE "
        )
