import streamlit as st

from models import connect_to_db
from constants import MAIN_MENU_OPTIONS
from controllers import redirect_controller


# Connect to db
cnx = connect_to_db()

redirect_controller(MAIN_MENU_OPTIONS[1], cnx)
