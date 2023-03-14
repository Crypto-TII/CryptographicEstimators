from enum import  Enum


LE_CODE_LENGTH = "code length"
LE_CODE_DIMENSION = "code dimension"
LE_FIELD_SIZE = "field size"


class VerboseInformation(Enum):
    """
    """
    NW = "Nw_prime"
    LISTS = "L_prime"
    LISTS_SIZE = "list_size"
    NORMAL_FORM = "normal_form"
    ISD = "C_ISD"
