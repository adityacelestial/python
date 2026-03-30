from utility import search_user

initial_user=input("Enter the username:").strip()

short_menu="1.Regidtration\n2.Exit"
menu="1.Registration\n2.Login\n3.Search\n4.Delete\n5.Exit"

showmenu=""
def select_menu(initial_user): 
    if(search_user(initial_user)):
        return True

    else:
        return False

