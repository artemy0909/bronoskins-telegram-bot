from utils.database import RightLevel

RIGHTS_FIRED = RightLevel.get(RightLevel.code == -1)
RIGHTS_ADMIN = RightLevel.get(RightLevel.code == 0)
RIGHTS_BOSS = RightLevel.get(RightLevel.code == 1)
RIGHTS_WORKER = RightLevel.get(RightLevel.code == 2)
RIGHTS_TRAINEE = RightLevel.get(RightLevel.code == 3)

ACCESS_FOR_ALL = (RIGHTS_ADMIN, RIGHTS_BOSS, RIGHTS_WORKER, RIGHTS_TRAINEE)
ACCESS_FOR_ADMINS = (RIGHTS_ADMIN, RIGHTS_BOSS)


def admins_ids():
    users_to_send = [i for i in RIGHTS_BOSS.stuff_set] + [i for i in RIGHTS_ADMIN.stuff_set]
    send_to_id = []
    for user in users_to_send:
        logins = [i.telegram_id for i in user.login_set]
        if logins:
            send_to_id.extend(logins)
    return send_to_id
