from os.path import splitext, join


def assetIdToCharStringPath(charstring_directory_path, assetId):
    # type: (str,str) -> str

    return join(charstring_directory_path, f"{splitext(assetId)[0]}.charstring")
