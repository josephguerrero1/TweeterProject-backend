from flask import request, Response
import dbhelpers
import json
import traceback
import secrets


class Login:

    # User Login

    def user_login():
        email = request.json['email']
        password = request.json['password']

        checkUser = dbhelpers.run_select_statement(
            "SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE email = ?, password = ?", [
                email, password]
        )

        if(len(checkUser) == 1):
            loginToken = secrets.token_urlsafe(50)
            user_id = checkUser[0][0]
            userId = dbhelpers.run_insert_statement("INSERT INTO user_session (user_id, loginToken) VALUES (?, ?)",
                                                    [user_id, loginToken])
        else:
            return "Login did not work"

        if(userId == None):
            return Response("DB Error, Sorry!", mimetype="text/plain", status=500)
        else:
            username = checkUser[0][2]
            bio = checkUser[0][3]
            birthdate = checkUser[0][4]
            imageUrl = checkUser[0][5]
            bannerUrl = checkUser[0][6]

            logged_in_user = {"userId": userId, "email": email, "username": username, "bio": bio,
                              "birthdate": birthdate, "loginToken": loginToken, "imageUrl": imageUrl, "bannerUrl": bannerUrl}
            logged_in_user_json = json.dumps(logged_in_user, default=str)
            return Response(logged_in_user_json, mimetype="application/json", status=201)

    # User Logout

    def user_logout():
        loginToken = request.json['loginToken']

        rowcount = dbhelpers.run_delete_statement(
            "DELETE FROM user_session WHERE loginToken = ?", [loginToken]
        )

        if(rowcount == 1):
            return Response(status=204)
        elif(rowcount == 0):
            return Response("Error, loginToken does not exist!", mimetype="text/plain", status=400)
        elif(rowcount == None):
            return Response("Database Error", mimetype="text/plain", status=500)
