from flask import request, Response
import dbhelpers
import json
import traceback


class Comments:

    # Get Comments

    def get_comments():
        tweetId = request.json['tweetId']
        all_comments = dbhelpers.run_select_statement(
            "SELECT c.id, c.user_id, u.username, c.content, c.createdAt FROM `user` u INNER JOIN comment c ON u.id = c.user_id WHERE c.tweet_id = ?", [tweetId])

        empty_comment = []

        for comment in all_comments:
            commentId = all_comments[1]
            userId = all_comments[2]
            username = all_comments[3]
            content = all_comments[4]
            createdAt = all_comments[5]

            comment = {
                "commentId": commentId,
                "tweetId": tweetId,
                "userId": userId,
                "username": username,
                "content": content,
                "createdAt": createdAt
            }

            empty_comment.append(comment)

        if(all_comments == None):
            return Response("Failed to GET all comments", mimetype="text/plain", status=500)
        else:
            all_comments_json = json.dumps(empty_comment, default=str)
            return Response(all_comments_json, mimetype="application/json", status=200)

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
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

        comment_id = dbhelpers.run_insert_statement(
            "INSERT INTO comment (tweet_id, user_id, content) VALUES (?, ?, ?)", [
                tweetId, userId, content]
        )

        if(comment_id == None):
            return Response("Failed to post comment", mimetype="text/plain", status=500)
        else:
            comment_info = dbhelpers.run_select_statement(
                "SELECT u.username, c.createdAt FROM `user` u INNER JOIN comment c ON u.id = c.user_id WHERE c.id = ?", [
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

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

        rowcount = dbhelpers.run_update_statement(
            "UPDATE comment c SET c.content = ? WHERE c.id = ? AND c.user_id = ?", [
                content, commentId, userId]
        )

        if(rowcount == None):
            return Response("Failed to update comment", mimetype="text/plain", status=500)
        elif(rowcount == 1):
            updated_comment = dbhelpers.run_select_statement(
                "SELECT c.tweet_id, u.username, c.createdAt FROM `user` u INNER JOIN comment c ON u.id = c.user_id WHERE c.id = ?", [
                    commentId]
            )

            tweetId = updated_comment[0][0]
            username = updated_comment[0][1]
            createdAt = updated_comment[0][2]

            updated_Comment = {
                "commentId": commentId,
                "tweetId": tweetId,
                "userId": user_id,
                "username": username,
                "content": content,
                "createdAt": createdAt
            }

            updated_Comment_json = json.dumps(updated_Comment, default=str)
            return Response(updated_Comment_json, mimetype="application/json", status=200)

    # Delete Comments

    def delete_comment():
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

        rowcount = dbhelpers.run_delete_statement(
            "DELETE FROM comment c WHERE c.id = ? AND c.user_id = ?", [
                commentId, userId]
        )

        if(rowcount == 1):
            return Response(status=204)
        elif(rowcount == None):
            return Response("Failed to delete comment", mimetype="text/plain", status=500)
