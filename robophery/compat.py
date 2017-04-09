

def const(value):

    """Constant optimisation

    http://docs.micropython.org/en/latest/wipy/reference/speed_python.html?highlight=const#the-const-declaration
    """

    try:
        return const(value)
    except:
        return value
