from oauth2client.client import OAuth2WebServerFlow

flow = OAuth2WebServerFlow(client_id='1074063071205-kjcvjjdrbotu2v00k4198543ntr2d7fg.apps.googleusercontent.com',
                           client_secret='Bn08ejvafGKWvoKdBNqCcOPH',
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='http://locahost:8080/auth_return')

auth_uri = flow.step1_get_authorize_url()
print(auth_uri)