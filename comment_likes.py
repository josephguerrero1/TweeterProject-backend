from flask import request, Response
import dbhelpers
import json
import traceback


class Comment_likes:

    # Get Comment Likes

    def get_comment_likes():
        commentId = request.args.get('commentId')

        if commentId:
            comment_likes_info = dbhelpers.run_select_statement(
                "SELECT cl.comment_id, cl.user_id, u.username FROM `user` u INNER JOIN comment_like cl ON u.id=cl.user_id WHERE cl.comment_id = ?", [commentId])

            userId = comment_likes_info[0][1]
            username = comment_likes_info[0][2]

            comment_like = [{
                "commentId": commentId,
                "userId": userId,
                "username": username
            }]
            if(comment_like == None):
                return Response("Failed to GET comment like", mimetype="text/plain", status=500)
            else:
                comment_like_json = json.dumps(comment_like, default=str)
                return Response(comment_like_json, mimetype="application/json", status=200)
        else:
            all_comment_likes = dbhelpers.run_select_statement(
                "SELECT cl.comment_id, cl.user_id, u.username FROM `user` u INNER JOIN comment_like cl ON u.id = cl.user_id")

            empty_comment_like = []

            for comment_like in all_comment_likes:
                commentId = all_comment_likes[0][0]
                userId = all_comment_likes[0][1]
                username = all_comment_likes[0][2]

                comment_like = {
                    "commentId": commentId,
                    "userId": userId,
                    "username": username
                }

                empty_comment_like.append(comment_like)

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
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

        comment_like_id = dbhelpers.run_insert_statement(
            "INSERT INTO comment_like (comment_id, user_id) VALUES (?, ?)", [
                commentId, userId]
        )

        if(comment_like_id == None):
            return Response("Failed to like comment", mimetype="text/plain", status=500)
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
        loginToken = request.json['login_Token']
        commentId = request.json['commentId']

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

        rowcount = dbhelpers.run_delete_statement(
            "DELETE FROM comment_like cl WHERE cl.comment_id = ? AND cl.user_id = ?", [
                commentId, userId]
        )

        if(rowcount == None):
            return Response("Database Error", mimetype="text/plain", status=500)
        elif(rowcount == 1):
            return Response(status=204)
