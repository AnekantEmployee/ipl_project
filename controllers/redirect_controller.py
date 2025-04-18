from constants import MAIN_MENU_OPTIONS

from templates import team_analysis
from templates import head_to_head_screen


def redirect_controller(menu, cnx):
    """Redirecting to the specific page based on the option

    Args:
        menu (sttring): menu option selected
        cnx (_type_): connection obect
    """
    if menu == MAIN_MENU_OPTIONS[0]:
        head_to_head_screen(cnx)

    elif menu == MAIN_MENU_OPTIONS[1]:
        team_analysis(cnx)
