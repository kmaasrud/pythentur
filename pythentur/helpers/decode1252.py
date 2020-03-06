def decode1252(string):
    replace = [
        ('Ã†', 'Æ'), ('Ã˜', 'Ø'), ('Ã…', 'Å'), ('Ã¦', 'æ'), ('Ã¸', 'ø'), ('Ã¥', 'å')
    ]
    for rep, repwith in replace:
        string = string.replace(rep, repwith)
    return string