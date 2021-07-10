from flask import request, Response
import dbhelpers
import json
import traceback


class Comments:

    # Get Comments

    def get_comments():
        tweetId = int(request.args['tweetId'])
        comments = dbhelpers.run_select_statement(
            "SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.createdAt FROM `user` u INNER JOIN comment c ON u.id = c.user_id WHERE c.tweet_id = ?", [tweetId])

        if(comments == None):
            return Response("Failed to GET comments", mimetype="text/plain", status=500)
        else:
            comments_json = json.dumps(comments, default=str)
            return Response(comments_json, mimetype="application/json", status=200)

    # Post Comment

    def post_comment():
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

        comment_id = dbhelpers.run_insert_statement(
            "INSERT INTO comment (tweet_id, user_id, content) VALUES (?, ?, ?)", [
                tweetId, userId, content]
        )

        if(comment_id == None):
            return Response("Tweet ID is invalid", mimetype="text/plain", status=500)
        else:
            comment_info = dbhelpers.run_select_statement(
                "SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.createdAt FROM `user` u INNER JOIN comment c ON u.id = c.user_id WHERE c.id = ?", [
                    comment_id]
            )

            username = comment_info[0][3]
            createdAt = comment_info[0][5]

            comment = {
                "commentId": comment_id,
                "tweetId": tweetId,
                "userId": userId,
                "username": username,
                "content": content,
                "createdAt": createdAt
            }

            comment_json = json.dumps(comment, default=str)
            return Response(comment_json, mimetype="application/json", status=201)

    # Update Comment

    def update_comment():
        loginToken = request.json['loginToken']
        commentId = request.json['commentId']
        content = request.json['content']

        # Write if statement
        comment = dbhelpers.run_select_statement(
            "SELECT us.loginToken, c.id, c.content FROM user_session us INNER JOIN comment c ON us.user_id = c.user_id WHERE us.loginToken = ? AND c.id = ?", [
                loginToken, commentId]
        )

        rowcount = dbhelpers.run_update_statement(
            "UPDATE comment SET content = ? WHERE id = ?", [content, commentId]
        )

    # Delete Comments

    def delete_comment():
        loginToken = request.json['loginToken']
        commentId = request.json['commentId']
