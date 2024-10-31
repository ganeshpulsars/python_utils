import pyinputplus as pyip


def inputDefaultWrapper(inputFunc):
    def wrapperFunc(*args, **kwargs):
        try:
            args = list(args)
            if len(args) >= 1:
                prompt = args[0]
            else:
                prompt = kwargs.get("prompt", "Input please :")
            default = kwargs.get("default", None)
            newPrompt = prompt.replace(":", f" <{default}> :")
            # inStr = inputFunc(*args, **kwargs, prompt=newPrompt, blank=True)
            inStr = inputFunc(newPrompt, **kwargs, blank=True)
            if inStr == "":
                return default
            else:
                return inStr
        except Exception as e:
            raise e

    return wrapperFunc


inputDefaultStr = inputDefaultWrapper(pyip.inputStr)
inputDefaultInt = inputDefaultWrapper(pyip.inputInt)
inputDefaultDate = inputDefaultWrapper(pyip.inputDate)
inputDefaultYesNo = inputDefaultWrapper(pyip.inputYesNo)
inputDefaultBool = inputDefaultWrapper(pyip.inputBool)


def inputDefaultMenu(choices, prompt="Please select :", **kwargs):
    try:
        default = kwargs.get("default", None)
        default = "1" if default is None else default
        newPrompt = prompt.replace(":", f" <{default}> :\n")
        choice = pyip.inputMenu(choices, prompt=newPrompt, numbered=True, blank=True)
        return choice
    except Exception as e:
        raise e
