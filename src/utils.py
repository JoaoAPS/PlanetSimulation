def assertType(varName, var, correct_type):
    """Raises a TypeError if 'var' is not of type 'correct_type'"""
    correct = False

    if type(correct_type) is list or type(correct_type) is tuple:
        for t in correct_type:
            if type(var) is t:
                correct = True
    else:
        correct = type(var) is correct_type

    if not correct:
        raise TypeError(
            varName + ' must be of type ' + str(correct_type) +
            ', type' + str(type(var)) + ' was passed!'
        )
