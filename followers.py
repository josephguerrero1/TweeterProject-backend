from flask import request, Response
import dbhelpers
import json
import traceback


class Followers:

    # Get User Followers

    def get_user_followers():
        userId = request.args['userId']

        user_followers = dbhelpers.run_select_statement(
            "SELECT f.user_id, u.email, u.username, u.bio, u.birthdate, u.imageUrl, u.bannerUrl FROM `user` u INNER JOIN follow f ON u.id = f.user_id WHERE f.followed_id = ?", [userId])

        if(user_followers == None):
            return Response("Failed to GET user followers", mimetype="text/plain", status=500)
        else:
            user_followers_json = json.dumps(user_followers, default=str)
            return Response(user_followers_json, mimetype="application/json", status=200)
