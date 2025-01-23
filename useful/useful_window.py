def center_window(window, width_aplication, height_aplication):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width/2) - (width_aplication/2))
    y = int((screen_height/2) - (height_aplication/2))
    return window.geometry(f"{width_aplication}x{height_aplication}+{x}+{y}")
