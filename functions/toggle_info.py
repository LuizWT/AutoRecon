show_info = False

def toggle_info():
    global show_info
    show_info = not show_info
    return show_info

def is_info_visible():
    return show_info
