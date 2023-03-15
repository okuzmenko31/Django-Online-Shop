def get_clean_email(email):
    """This function returns email
    without all symbols after @"""
    email = email
    username = email.split('@')[0]
    return username
