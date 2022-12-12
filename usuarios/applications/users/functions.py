# Funciones extra de la app user

import random
import string

def code_generator(size=6, char=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(char) for _ in range(size))