from enum import Enum


PK_COLUMNS = "columns"
PK_ROWS = "rows"
PK_FIELD_SIZE = "field size"
PK_DIMENSION = "dimension"


class VerboseInformation(Enum):
    KMP_L1 = "L1"
    KMP_L2 = "L2"
    KMP_FINAL_LIST = "final list"
    SBC_ISD = "ISD cost"
    SBC_U = "u"
