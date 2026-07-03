password = "admin123"

def get_user(user_input):
    query = "SELECT * FROM users WHERE id = " + user_input
    return query