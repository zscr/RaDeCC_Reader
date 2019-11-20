
#This function extracts all the numbers in a string and concatenates them

def get_digits(text):

    filtrate_list = list(filter(str.isdigit, text))
    filtrate = ''.join(filtrate_list)
    return (filtrate)
