import traceback


def render_exception(e, html=False):
    strOut = "Error : \n"
    for arg in e.args:
        strOut += str(arg) + "\n"
    strOut += traceback.format_exc()
    if html:
        strOut = strOut.replace("\n", "<br>").replace('"', "")
    return strOut


def is_content_html(obj: [str, object]) -> bool:
    """
    Function to test the response for content-type html
    """
    if type(obj) == str:
        return obj.startswith("<!DOCTYPE html>")
    else:
        try:
            return "html" in obj.headers.get("content-type", "")
        except Exception:
            raise TypeError(f"Invalid type {type(obj)}")
