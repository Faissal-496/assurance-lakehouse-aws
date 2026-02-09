import streamlit as st
import streamlit_authenticator as stauth
import os
import streamlit as st

PUBLIC_USERNAME = "sst"
ADMIN_USERNAME = "admin"

ACCESS_DENIED_MSG = "You don't have permission to access this page."

config = {
    "credentials" : {
        "usernames": {
            os.environ.get("BASIC_AUTH_USERNAME") : {
                "name" : PUBLIC_USERNAME,
                "password" : os.environ.get("BASIC_AUTH_PASSWORD_HASH")
            },
            
            os.environ.get("ADMIN_AUTH_USERNAME") : {
                "name" : ADMIN_USERNAME,
                "password" : os.environ.get("ADMIN_AUTH_PASSWORD_HASH")
            }
        }
    },

    "cookie": {
        "expiry_days" : 1,
        "key": "crashwise_atd",
        "name" : "crashwise_webapp"
    }
}

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

def init_authenticator_session_state():
    keys = ["authentication_status", "name", "logout", "username"]
    for key in keys:
        if not key in st.session_state:
            st.session_state[key] = None

def setup_authenticator(admin_required = False):
    if not "authentication_status" in st.session_state:
        st.session_state["authentication_status"] = None
        st.session_state["logout"] = None

    if st.session_state["authentication_status"]:
        authenticator.logout('Logout', 'main')
            
        if admin_required and st.session_state["name"] != ADMIN_USERNAME:
            st.warning(ACCESS_DENIED_MSG)
            st.stop()

    elif st.session_state["authentication_status"] == None:
        st.warning('Please login')
        name, authentication_status, username = authenticator.login('Login', 'main')
        st.stop()

    elif st.session_state["authentication_status"] == False:
        name, authentication_status, username = authenticator.login('Login', 'main')
        st.warning('Please login')
        st.stop()











def set_page_style():
    return st.markdown("""
                <html>
                    <head>
                    <style>
                        ::-webkit-scrollbar {
                            width: 20px;
                            }

                            /* Track */
                            ::-webkit-scrollbar-track {
                            background: #f1f1f1;
                            }

                            /* Handle */
                            ::-webkit-scrollbar-thumb {
                            background: #888;
                            }

                            /* Handle on hover */
                            ::-webkit-scrollbar-thumb:hover {
                            background: #555;
                            }

                            [data-testid="stSidebar"][aria-expanded="true"]{
                                max-width: 15%;
                            }
                    </style>
                    </head>
                    <body>
                    </body>
                </html>
            """, unsafe_allow_html=True)


def setup_sidebar():
    sideb = st.sidebar
    if sideb.button("Clear application cache"):
        st.cache_data.clear()

    if 'login' not in st.session_state:
        st.session_state.login = ""

    login = sideb.text_input("Username", st.session_state.login)

    if sideb.button("Enter"):
        st.session_state.login = login

    if st.session_state.login == "":
        st.warning("Please enter a username to access this page.")
        st.stop()


def get_remote_ip() -> str:
    """Get remote ip."""

    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip

class ContextFilter(logging.Filter):
    def filter(self, record):
        record.user_ip = get_remote_ip()
        record.user_name = st.session_state.login
        return super().filter(record)
    
def setup_logger(caller_page : str):
    logger = logging.getLogger(caller_page)
    logger.propagate = False
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(name)s %(asctime)s [username=%(user_name)s] [userip=%(user_ip)s] - %(message)s")

    #if no streamhandler present, add one
    if sum([isinstance(handler, logging.StreamHandler) for handler in logger.handlers]) == 0:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.addFilter(ContextFilter())
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    #if a file handler is requested, check for existence then add
    if sum([isinstance(handler, logging.FileHandler) for handler in logger.handlers]) == 0:
        Path(os.environ["APP_LOGS_PATH"]).mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(Path(os.environ["APP_LOGS_PATH"])/"streamlit_logger.log", mode='a', maxBytes=5*1024*1024, 
                                        backupCount=2, encoding=None, delay=0)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("# Welcome to AssuranceWise ! 👋")
st.markdown(
    """
"""
)

set_page_style()

init_authenticator_session_state()
setup_authenticator()
setup_sidebar()

logger = setup_logger(caller_page = Path(__file__).stem)
logger.info("Ping")

st.title("Contact")
st.write("""
         For all enquiries/questions, please email us :

         - faissal : faissal_496@outlook.com
         - Omar : omar_546@outlook.com
         """)


