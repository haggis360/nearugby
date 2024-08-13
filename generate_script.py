# open file to read
import random

myfile = open("init_users_predictions.txt", "w")

# drop table time_properties;
# create table time_properties(id integer not null, season integer, game_week integer, primary key(id));
# insert into time_properties(id, season, game_week) VALUES (1, 2022, 7);

# clear test predictions
myfile.write(
    "delete from player_prediction where user_id in(200,201,202,203,204,205,206,207,208,209,210);\n"
)
# clear test users
for i in range(200, 210):
    myfile.write("delete from User where id=" + str(i) + ";\n")
# create test users
myfile.write(
    'insert into user(id, email, password, name) values(200, "homewin@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","homewin");\n'
)
myfile.write(
    'insert into user(id, email, password, name) values(201, "awaywin@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","awaywin");\n'
)
myfile.write(
    'insert into user(id, email, password, name) values(202, "draw@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","draw");\n'
)
myfile.write(
    'insert into user(id, email, password, name) values(203, "200-0@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","200-0");\n'
)
myfile.write(
    'insert into user(id, email, password, name) values(204, "dan@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","dan");\n'
)
myfile.write(
    'insert into user(id, email, password, name) values(205, "pete@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","pete");\n'
)
myfile.write(
    'insert into user(id, email, password, name) values(206, "sue@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","sue");\n'
)
myfile.write(
    'insert into user(id, email, password, name) values(207, "mary@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","mary");\n'
)
myfile.write(
    'insert into user(id, email, password, name) values(208, "george@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","george");\n'
)
myfile.write(
    'insert into user(id, email, password, name) values(209, "david@test.com", "scrypt:32768:8:1$IjkY5tzGzriHKFIS$edb675a0570ef5f8d747b3439d42fdd3d6a63c6ff11fc86033fc51aaf7d8c24e7b74b67feb09a55062582147b01b54b8e80512166afd6fd0f334681183daac00","dave");\n'
)
# always home win predictions
for fixture_id in range(1, 2618):
    myfile.write(
        "insert into player_prediction(user_id, fixture_id, home_score, away_score, prediction_outcome, prediction_point_diff) values(200,"
        + str(fixture_id)
        + ",50,10,0,0);\n"
    )
# always away win predicting user
for fixture_id in range(1, 2618):
    myfile.write(
        "insert into player_prediction(user_id, fixture_id, home_score, away_score, prediction_outcome, prediction_point_diff) values(201,"
        + str(fixture_id)
        + ",10,50,0,0);\n"
    )
# always draw predicting user
for fixture_id in range(1, 2618):
    myfile.write(
        "insert into player_prediction(user_id, fixture_id, home_score, away_score, prediction_outcome, prediction_point_diff) values(202,"
        + str(fixture_id)
        + ",20,20,0,0);\n"
    )
# random predictions
for fixture_id in range(1, 2618):
    for user_id in range(203, 209):
        myfile.write(
            "insert into player_prediction(user_id, fixture_id, home_score, away_score, prediction_outcome, prediction_point_diff) values("
            + str(user_id)
            + ","
            + str(fixture_id)
            + ","
            + str(random.randint(0, 50))
            + ","
            + str(random.randint(0, 50))
            + ",0,0);\n"
        )
