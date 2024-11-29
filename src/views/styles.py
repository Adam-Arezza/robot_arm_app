from ttkbootstrap.style import Style


def create_style_set():
    style_set = Style()
    style_set.configure('Custom.TFrame', background='grey')
    style_set.configure('Custom.TLabel', background='grey')
    style_set.configure('Custom.TCheckbutton', background='grey')
    #style_set.configure('Custom.TNotebook', background='grey')
