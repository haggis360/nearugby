from .user import User


def get_player(user_id: int) -> User:
    return User.query.get(user_id)


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


def latest_team_form(team):
    pass


def latest_match_form():
    pass
