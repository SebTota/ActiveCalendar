import shortuuid


def get_random_alphanumeric_string(length: int = 12):
    return shortuuid.ShortUUID().random(length=length)
