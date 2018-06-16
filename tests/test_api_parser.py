from worldcup.api_parser import WorldCupData


def test_get_team_info():
    wcdata = WorldCupData()
    assert wcdata.get_team_info(1) == {
        "emoji": "flag-ru",
        "emojiString": "🇷🇺",
        "fifaCode": "RUS",
        "flag": "https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/Flag_of_Russia.svg/900px-Flag_of_Russia.png",
        "id": 1,
        "iso2": "ru",
        "name": "Russia"
    }
    assert wcdata.get_team_info(1, "name") == "Russia"


def test_get_stadium_info():
    wcdata = WorldCupData()
    assert wcdata.get_stadium_info(1) == {
        "city": "Moscow",
        "id": 1,
        "image": "https://upload.wikimedia.org/wikipedia/commons/e/e6/Luzhniki_Stadium%2C_Moscow.jpg",
        "lat": 55.715765,
        "lng": 37.5515217,
        "name": "Luzhniki Stadium"
    }
    assert wcdata.get_stadium_info(1, "name") == "Luzhniki Stadium"


def test_all_matches():
    wcdata = WorldCupData()
    all_matches = wcdata.all_matches()
    assert len(all_matches) == 64


def test_group_members():
    wcdata = WorldCupData()
    members = []
    for group in "abcdefgh":
        members.extend(wcdata.get_group_members(group))
    assert len(members) == 32
