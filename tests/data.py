VALID_USER_DATA: list[tuple[str, str, str]] = [
    (
        "John Doe",
        "JOHN@EMAIL.TLD",
        "/"*256,
    ),
    (
        "Valérie Dodier",
        "JussiSeikola@MyMaIl.co",
        "!#$%&'()*,./:;<=>?@[]^_`{|}~",
    ),
    (
        "Лайма Назарова",
        "C.hyouMao@Extraville.fi",
        "388983c6-f14f-4d19-b661-cb192fdc47da",
    ),
    (
        "立 杨 立 杨 立 杨 立",
        f"{"a.a"*18}@a.a",
        "eLoritho1",
    ),
    (
        "W"*32,
        "a@B.c",
        "立"*8,
    ),
]

INVALID_USER_DATA: list[tuple[str, str, str]] = [
    (
        "",
        "",
        "",
    ),
    (
        "X"*128,
        "@GracieWallismail.ru",
        "1234567",
    ),
    (
        "-.",
        "."*64,
        "!"*512,
    ),
    (
        "1@",
        "@.com",
        "**123*",
    ),
    (
        "$$",
        "YetererCOOLDomain.com",
        "!"*512,
    ),
]

USER_INFO: list[tuple[int, str, str]] = [
    (
        7207503858480705536,
        "形県青田市南区形県青田市南区渚町木村105村105号",
        ".$r.ZFJT@h2([L;@hbKKkvvHK+_djM.com",
    ),
    (
        -0,
        "Søndre",
        "55.381736, 11.945865",
    ),
    (
        -7207503858480705536,
        "立 杨",
        f"Metal@{"Video" * 100}.com",
    ),
    (
        4485111300570398124312,
        "aaa.bbb.ccc",
        "",
    ),
    (
        0,
        "",
        "",
    ),
]

JWT_CREDENTIALS: list[tuple[str, dict[str, str | int]]] = [
    (
        "access",
        {
            "sub": 7207503858480705536,
            "name": "Fuleat",
            "email": "HarryByrne@teleworm.us",
            "key": "Newmark & Lewis",
        },
    ),
    (
        "access",
        {
            "sub": 7207503858480705536,
            "name": "123123",
            "email": "55.628354, 12.636962",
            "key": "198.4 pounds (90.2 kilograms)",
        },
    ),
    (
        "refresh",
        {
            "sub": -1000000000,
            "name": "True",
            "email": "Mozilla/5.0@...........",
            "key": "21f323d3-6df2-4d27-994a-6ec0af48ad50",
        },
    ),
    (
        "refresh",
        {
            "sub": -0,
            "name": 123123,
            "email": "28 years old",
            "key": "July 12, 1995",
        },
    ),
    (
        "refresh",
        {
            "sub": 0,
            "name": "",
            "email": "",
            "key": "",
        },
    ),
]

JWT_TOKENS: list[tuple[str, str]] = [
    ("refresh", ""),
    ("refresh", "形県青田市南区形県青田市南区渚町木村105村105号"),
    ("access", "JLKSLKjsadhj91ysijcx1kgppakls9as;zxpSodS"*100),
    ("access", "aaa.bbb.ccc"),
    ("access", "Santiago Méndez"),
]
