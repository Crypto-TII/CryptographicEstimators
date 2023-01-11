from enum import Enum

SD_CODE_LENGTH = "code length"
SD_CODE_DIMENSION = "code dimension"
SD_ERROR_WEIGHT = "error weight"

class VerboseInformation(Enum):
    CONSTRAINTS = "constraints"
    PERMUTATIONS = "permutations"
    TREE = "tree"
    GAUSS = "gauss"
    REPRESENTATIONS = "representation"
    LISTS = "lists"