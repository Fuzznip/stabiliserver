# dropDictionary is a dictionary of pairs of items and drop sources to the list of channels they should post in
# eg. { ("abyssal whip", "abyssal demon"): [ "1233130963870154864", "1232048319996625029", ... ] }
dropDictionary: dict[tuple[str, str], list[str]] = {}

get_drop_dictionary = lambda: dropDictionary
set_drop_dictionary = lambda new_dict: dropDictionary.update(new_dict)