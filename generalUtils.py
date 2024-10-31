import traceback


def render_exception(e):
    strOut = "Error : \n"
    for arg in e.args:
        strOut += str(arg) + "\n"
    strOut += traceback.format_exc()
    # strOut = strOut.replace("\n", "<br>").replace('"', "")
    return strOut
