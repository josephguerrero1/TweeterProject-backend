from flask import request, Response
import dbhelpers
import json
import traceback
import secrets


class Login:

    # User Login

    def user_login():
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json['password']

        user_info = dbhelpers.run_select_statement(
            "SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE email = ?, password = ?", [
                email, password]
        )

        if(len(user_info) != 1):
            return Response("Failed to get user information", mimetype="text/plain", status=500)
        elif(len(user_info) == 1):
            loginToken = secrets.token_urlsafe(50)
            userId = user_info[0][0]
            user_session_id = dbhelpers.run_insert_statement("INSERT INTO user_session us (user_id, loginToken) VALUES (?, ?)",
                                                             [userId, loginToken])

            if(user_session_id == None):
                return Response("Failed to login", mimetype="text/plain", status=500)
            else:
                email = user_info[0][1]
                username = user_info[0][2]
                bio = user_info[0][3]
                birthdate = user_info[0][4]
                imageUrl = user_info[0][5]
                bannerUrl = user_info[0][6]

                logged_in_user = {"userId": userId, "email": email, "username": username, "bio": bio,
                                "birthdate": birthdate, "loginToken": loginToken, "imageUrl": imageUrl, "bannerUrl": bannerUrl}
                logged_in_user_json = json.dumps(logged_in_user, default=str)
                return Response(logged_in_user_json, mimetype="application/json", status=201)

    # User Logout

    def user_logout():
        loginToken = request.json['loginToken']

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

            rowcount = dbhelpers.run_delete_statement(
                "DELETE FROM user_session WHERE loginToken = ? AND user_id = ?", [
                    loginToken, userId]
            )

            if(rowcount == 1):
                return Response(status=204)
            elif(rowcount == None):
                return Response("Failed to logout", mimetype="text/plain", status=500)
