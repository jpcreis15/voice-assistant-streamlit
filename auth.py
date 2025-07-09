import app
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from PIL import Image

# im = Image.open("img/medicompliance.jpeg")

st.set_page_config(page_title='Dummy Voice Assistant')

def get_user_management(db):
    try:
        with db.connect() as conn:
            query = 'SELECT * FROM user_management;'
            rows = conn.execute(text(query)).fetchall()

            res_temp = dict()
            for r in rows:
                res_temp[r[1]] = {'email': r[2], 'name': r[3], 'password': r[4]}
            res = { 'usernames': res_temp }
            return res
    except Exception as e:
        raise Exception(e , ": in get_user_management")

def get_cookies(db):
    try:
        with db.connect() as conn:
            query = 'SELECT * FROM cookies;'
            rows = conn.execute(text(query)).fetchall()
            return {'cookie_expiry_days': rows[0][1], 'cookie_key': rows[0][2], 'cookie_name': rows[0][3]}
    except Exception as e:
        raise Exception(e , ": in get_cookies")

def get_preauthorized(db):
    try:
        with db.connect() as conn:
            query = 'SELECT * FROM preauthorized;'
            rows = conn.execute(text(query)).fetchall()
            email_list = [r[1] for r in rows]
            return {'emails': email_list}
    except Exception as e:
        raise Exception(e , ": in get_preauthorized")

# Configure logo and name of the page to be shown in the browser.
# st.set_page_config(page_title='MediCompliance',
#                     page_icon=im)

# Init the DB
if "db" not in st.session_state:
    load_dotenv()

    APP_DATABASE_NAME = os.getenv('APP_DATABASE_NAME')
    APP_DATABASE_USER = os.getenv('APP_DATABASE_USER')
    APP_DATABASE_PASS = os.getenv('APP_DATABASE_PASS')
    APP_DATABASE_HOST = os.getenv('APP_DATABASE_HOST')
    APP_DATABASE_PORT = os.getenv('APP_DATABASE_PORT')
    
    try:
        db_string = 'postgresql://{}:{}@{}:{}/{}'.format(APP_DATABASE_USER, 
                                                         APP_DATABASE_PASS, 
                                                         APP_DATABASE_HOST,
                                                         APP_DATABASE_PORT,
                                                         APP_DATABASE_NAME)
        st.session_state["db"] = create_engine(db_string)
    except Exception as e:
        raise Exception("Something went wrong with CB DB connection: " , e)

#######################################################################
# Remove footers and headers
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
#######################################################################

## Credentials from DB
config = dict()
cookies = dict()
try:
    config['credentials'] = get_user_management(st.session_state["db"])
    config['preauthorized'] = get_preauthorized(st.session_state["db"])
    cookies = get_cookies(st.session_state["db"])
except Exception as e: 
    raise Exception("Something went wrong with the DB connection: " , e)

# Create the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    cookies['cookie_name'],
    cookies['cookie_key'],
    cookies['cookie_expiry_days']
)

_, main_col, _ =  st.columns([0.2, 0.6, 0.2])
with main_col:
    # get credentials from login
    # name, authentication_status, username = authenticator.login("Login", "main")
    authenticator.login("main", fields = {'Form name': 'Login'})

if st.session_state["authentication_status"] is False:
    _, main_col, _ =  st.columns([0.2, 0.6, 0.2])
    with main_col:
        st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    _, main_col, _ =  st.columns([0.2, 0.6, 0.2])
    with main_col:
        st.warning('Please enter your username and password')
elif st.session_state['authentication_status']:
    # authenticator.logout("Logout", "sidebar")
    authenticator.logout("Logout")
    app.main()