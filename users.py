from flask import request, Response
import dbhelpers
import json
import traceback
import secrets


class Users:

    # Get Users

    def get_users():
        userId = request.args.get('userId')

        if userId:
            user_info = dbhelpers.run_select_statement(
                "SELECT email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE id = ?", [userId])

            email = user_info[0][0]
            username = user_info[0][1]
            bio = user_info[0][2]
            birthdate = user_info[0][3]
            imageUrl = user_info[0][4]
            bannerUrl = user_info[0][5]

            user = [{"userId": userId, "email": email, "username": username, "bio": bio, "birthdate": birthdate, "imageUrl": imageUrl, "bannerUrl": bannerUrl
                     }]
            if(user == None):
                return Response("Failed to GET user", mimetype="text/plain", status=500)
            else:
                user_json = json.dumps(user, default=str)
                return Response(user_json, mimetype="application/json", status=200)
        else:
            all_users = dbhelpers.run_select_statement(
                "SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user")

            empty_user = []

            for user in all_users:
                userId = user[0]
                email = user[1]
                username = user[2]
                bio = user[3]
                birthdate = user[4]
                imageUrl = user[5]
                bannerUrl = user[6]

                user = {"userId": userId, "email": email, "username": username, "bio": bio, "birthdate": birthdate, "imageUrl": imageUrl, "bannerUrl": bannerUrl
                        }

                empty_user.append(user)

            if(all_users == None):
                return Response("Failed to GET all users", mimetype="text/plain", status=500)
            else:
                all_users_json = json.dumps(empty_user, default=str)
                return Response(all_users_json, mimetype="application/json", status=200)

    # Post User

    def post_user():
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        birthdate = request.json['birthdate']
        imageUrl = request.json.get('imageUrl')
        bannerUrl = request.json.get('bannerUrl')
        loginToken = secrets.token_urlsafe(50)

        userId = dbhelpers.run_insert_statement("INSERT INTO user(email, username, password, bio, birthdate, imageUrl, bannerUrl) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                                [email, username, password, bio, birthdate, imageUrl, bannerUrl])
        if(userId == None):
            return Response("Failed to post a new user", mimetype="text/plain", status=500)
        else:

            user_session_id = dbhelpers.run_insert_statement("INSERT INTO user_session us (user_id, loginToken) VALUES (?, ?)",
                                                             [userId, loginToken])

            newUser = {"userId": userId, "email": email, "username": username, "bio": bio,
                       "birthdate": birthdate, "imageUrl": imageUrl, "bannerUrl": bannerUrl, "loginToken": loginToken}
            newUser_json = json.dumps(newUser, default=str)
            return Response(newUser_json, mimetype="application/json", status=201)

    # Update User

    def update_user():

        # Data sent by the user
        loginToken = request.json['loginToken']
        bio = request.json.get('bio')
        birthdate = request.json.get('birthdate')
        email = request.json.get('email')
        username = request.json.get('username')
        bannerUrl = request.json.get('bannerUrl')
        imageUrl = request.json.get('imageUrl')

        # Using the loginToken to get the userId of the user via SELECT STATEMENT
        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        # If the user_id is None, it will return an invalid Logintoken error

        # Else, a variable of userId is created which is taken from the user_id table
        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

        # If the user put data in any of the keys, it will run an update statement to update the specific key of the user.

        if(bio != None or bio != ''):
            rowcount = dbhelpers.run_update_statement(
                "UPDATE `user` u SET u.bio = ? WHERE u.id = ?", [bio, userId]
            )

        if(birthdate != None or birthdate != ''):
            rowcount = dbhelpers.run_update_statement(
                "UPDATE `user` u SET u.birthdate = ? WHERE u.id = ?", [
                    birthdate, userId]
            )

        if(email != None or email != ''):
            rowcount = dbhelpers.run_update_statement(
                "UPDATE `user` u SET u.email = ? WHERE u.id = ?", [
                    email, userId]
            )

        if(username != None or username != ''):
            rowcount = dbhelpers.run_update_statement(
                "UPDATE `user` u SET u.username = ? WHERE u.id = ?", [
                    username, userId]
            )

        if(bannerUrl != None or bannerUrl != ''):
            rowcount = dbhelpers.run_update_statement(
                "UPDATE `user` u SET u.bannerUrl = ? WHERE u.id = ?", [
                    bannerUrl, userId]
            )

        if(imageUrl != None or imageUrl != ''):
            rowcount = dbhelpers.run_update_statement(
                "UPDATE `user` u SET u.imageUrl = ? WHERE u.id = ?", [
                    imageUrl, userId]
            )

        # If the rowcount is None, a database error is sent back

        # If the rowcount is 1, I convert the updatedUser object to JSON and send it back to the user with a success status of 200

        if(rowcount == None):
            return Response("Database Error", mimetype="text/plain", status=500)
        elif(rowcount == 1):
            # I run a select statement to fetch all the updated or not updated values of the keys.

            updated_user = dbhelpers.run_select_statement(
                "SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.imageUrl, u.bannerUrl FROM `user` u  WHERE u.id = ?", [
                    userId]
            )

            # I store them into variables

            userId = updated_user[0][0]
            email = updated_user[0][1]
            username = updated_user[0][2]
            bio = updated_user[0][3]
            birthdate = updated_user[0][4]
            imageUrl = updated_user[0][5]
            bannerUrl = updated_user[0][6]

            # Making an object to return as JSON Data to the user

            updatedUser = {
                "userId": userId,
                "email": email,
                "username": username,
                "bio": bio,
                "birthdate": birthdate,
                "imageUrl": imageUrl,
                "bannerUrl": bannerUrl
            }
            updatedUser_json = json.dumps(updatedUser, default=str)
            return Response(updatedUser_json, mimetype="application/json", status=200)

    # Delete User

    def delete_user():
        loginToken = request.json['loginToken']
        password = request.json['password']

        user_id = dbhelpers.run_select_statement(
            "SELECT us.user_id FROM user_session us WHERE us.loginToken = ?", [
                loginToken]
        )

        if(user_id == None):
            return Response("Invalid Login Token", mimetype="text/plain", status=400)
        else:
            userId = user_id[0][0]

        Login_combo = dbhelpers.run_select_statement(
            "SELECT u.password FROM `user` u WHERE u.id= ?", [userId]
        )

        if(password == Login_combo[0][0]):
            rowcount = dbhelpers.run_delete_statement(
                "DELETE FROM `user` u WHERE u.id = ?", [userId]
            )
        else:
            return Response("Wrong password", mimetype="text/plain", status=500)

        if(rowcount == 1):
            return Response(status=204)
        elif(rowcount == None):
            return Response("Failed to delete user", mimetype="text/plain", status=500)
