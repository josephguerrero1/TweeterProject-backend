from flask import request, Response
import dbhelpers
import json
import traceback


class Comment_likes:

    # Get Comment Likes

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
                all_comment_likes_json = json.dumps(
                    all_comment_likes, default=str)
                return Response(all_comment_likes_json, mimetype="application/json", status=200)

    # Like Comment

    def like_comment():
        loginToken = request.json['loginToken']
        commentId = request.json['commentId']

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=500)
        else:
            userId = user_id[0][0]

        comment_like_id = dbhelpers.run_insert_statement(
            "INSERT INTO comment_like (comment_id, user_id) VALUES (?, ?)", [
                commentId, userId]
        )

        if(comment_like_id == None):
            return Response("Comment ID is invalid", mimetype="text/plain", status=500)
        else:
            comment_like_info = dbhelpers.run_select_statement(
                "SELECT cl.comment_id, cl.user_id, u.username FROM `user` u INNER JOIN comment_like cl ON u.id = cl.user_id WHERE cl.id = ?", [
                    comment_like_id]
            )

            username = comment_like_info[0][2]

            comment_like = {
                "commentId": commentId,
                "userId": userId,
                "username": username
            }

            comment_like_json = json.dumps(comment_like, default=str)
            return Response(comment_like_json, mimetype="application/json", status=201)

    # Unlike Comment

    def unlike_comment():
        loginToken = request.json['loginToken']
        commentId = request.json['commentId']
