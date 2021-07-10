from flask import request, Response
import dbhelpers
import json
import traceback


class Followers:

    # Get User Followers

    def get_user_followers():
        userId = request.args['userId']

        all_user_followers = dbhelpers.run_select_statement(
            "SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.imageUrl, u.bannerUrl FROM `user` u INNER JOIN follow f ON u.id = f.followed_id WHERE f.followed_id = ?", [
                userId]
        )

        empty_user_follower = []

        for user_follower in all_user_followers:
            userId = all_user_followers[0]
            email = all_user_followers[1]
            username = all_user_followers[2]
            bio = all_user_followers[3]
            birthdate = all_user_followers[4]
            imageUrl = all_user_followers[5]
            bannerUrl = all_user_followers[6]

            user_follower = {"userId": userId, "email": email, "username": username, "bio": bio, "birthdate": birthdate, "imageUrl": imageUrl, "bannerUrl": bannerUrl
                             }

            empty_user_follower.append(user_follower)

        if(all_user_followers == None):
            return Response("Failed to GET all user followers", mimetype="text/plain", status=500)
        else:
            all_user_followers_json = json.dumps(
                empty_user_follower, default=str)
            return Response(all_user_followers_json, mimetype="application/json", status=200)
