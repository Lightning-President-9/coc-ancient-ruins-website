from flask import Flask , render_template

app = Flask(__name__)

data_mem=[
    {
        "Unique ID": "COCAR#1",
        "Name": "KAI HIWATARI",
        "WAR": "IN",
        "War Attack": 123,
        "War Streak": "NO",
        "Clan Capital Attack": 25,
        "Clan Games": 6,
        "Clan Capital Maxed": 3,
        "Status": "Leader"
    },
    {
        "Unique ID": "COCAR#2",
        "Name": "Chief",
        "WAR": "IN",
        "War Attack": 3,
        "War Streak": "NO",
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#3",
        "Name": "MASTER SARVESH",
        "WAR": "IN",
        "War Attack": 32,
        "War Streak": "NO",
        "Clan Capital Attack": 13,
        "Clan Games": 6,
        "Clan Capital Maxed": 0,
        "Status": "Co-leader"
    },
    {
        "Unique ID": "COCAR#4",
        "Name": "NIKHIL",
        "WAR": "IN",
        "War Attack": 15,
        "War Streak": "YES",
        "Clan Capital Attack": 5,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#5",
        "Name": "taghonski",
        "WAR": "IN",
        "War Attack": 27,
        "War Streak": "NO",
        "Clan Capital Attack": 15,
        "Clan Games": 4,
        "Clan Capital Maxed": 3,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#6",
        "Name": "kyaw_ein",
        "WAR": "IN",
        "War Attack": 73,
        "War Streak": "NO",
        "Clan Capital Attack": 0,
        "Clan Games": 5,
        "Clan Capital Maxed": 0,
        "Status": "Co-leader"
    },
    {
        "Unique ID": "COCAR#7",
        "Name": "ApE_Re@L#22",
        "WAR": "IN",
        "War Attack": 13,
        "War Streak": "NO",
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#8",
        "Name": "karthi",
        "WAR": "IN",
        "War Attack": 54,
        "War Streak": "NO",
        "Clan Capital Attack": 10,
        "Clan Games": 4,
        "Clan Capital Maxed": 1,
        "Status": "Co-leader"
    },
    {
        "Unique ID": "COCAR#9",
        "Name": "+Little8uddy+",
        "WAR": "IN",
        "War Attack": 11,
        "War Streak": "YES",
        "Clan Capital Attack": 4,
        "Clan Games": 1,
        "Clan Capital Maxed": 1,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#10",
        "Name": "Ballistaaa",
        "WAR": "OUT",
        "War Attack": 5,
        "War Streak": "NO",
        "Clan Capital Attack": 17,
        "Clan Games": 2,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#11",
        "Name": "gautam",
        "WAR": "IN",
        "War Attack": 45,
        "War Streak": "YES",
        "Clan Capital Attack": 13,
        "Clan Games": 2,
        "Clan Capital Maxed": 2,
        "Status": "Co-leader"
    },
    {
        "Unique ID": "COCAR#12",
        "Name": "emnil007",
        "WAR": "IN",
        "War Attack": 51,
        "War Streak": "YES",
        "Clan Capital Attack": 23,
        "Clan Games": 6,
        "Clan Capital Maxed": 2,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#13",
        "Name": "RK79",
        "WAR": "IN",
        "War Attack": 59,
        "War Streak": "NO",
        "Clan Capital Attack": 5,
        "Clan Games": 3,
        "Clan Capital Maxed": 0,
        "Status": "Co-leader"
    },
    {
        "Unique ID": "COCAR#14",
        "Name": "thank God",
        "WAR": "IN",
        "War Attack": 3,
        "War Streak": "NO",
        "Clan Capital Attack": 17,
        "Clan Games": 1,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#15",
        "Name": "Kay M",
        "WAR": "IN",
        "War Attack": 34,
        "War Streak": "NO",
        "Clan Capital Attack": 19,
        "Clan Games": 2,
        "Clan Capital Maxed": 2,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#16",
        "Name": "PlumpToast",
        "WAR": "OUT",
        "War Attack": 0,
        "War Streak": "NO",
        "Clan Capital Attack": 14,
        "Clan Games": 1,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#17",
        "Name": "MALAY",
        "WAR": "IN",
        "War Attack": 13,
        "War Streak": "NO",
        "Clan Capital Attack": 12,
        "Clan Games": 2,
        "Clan Capital Maxed": 1,
        "Status": "Co-leader"
    },
    {
        "Unique ID": "COCAR#18",
        "Name": "Trapsus",
        "WAR": "IN",
        "War Attack": 14,
        "War Streak": "NO",
        "Clan Capital Attack": 6,
        "Clan Games": 4,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#19",
        "Name": "Eleiken",
        "WAR": "IN",
        "War Attack": 72,
        "War Streak": "YES",
        "Clan Capital Attack": 15,
        "Clan Games": 3,
        "Clan Capital Maxed": 1,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#20",
        "Name": "sreeram.k.y",
        "WAR": "IN",
        "War Attack": 0,
        "War Streak": "NO",
        "Clan Capital Attack": 7,
        "Clan Games": 1,
        "Clan Capital Maxed": 1,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#21",
        "Name": "LordHoodAs",
        "WAR": "IN",
        "War Attack": 1,
        "War Streak": "NO",
        "Clan Capital Attack": 5,
        "Clan Games": 1,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#22",
        "Name": "ligma",
        "WAR": "IN",
        "War Attack": 1,
        "War Streak": "YES",
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#23",
        "Name": "Taghonski",
        "WAR": "OUT",
        "War Attack": 0,
        "War Streak": "NO",
        "Clan Capital Attack": 15,
        "Clan Games": 6,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#24",
        "Name": "Abhi624",
        "WAR": "IN",
        "War Attack": 11,
        "War Streak": "NO",
        "Clan Capital Attack": 13,
        "Clan Games": 2,
        "Clan Capital Maxed": 1,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#25",
        "Name": "mr.lemo",
        "WAR": "IN",
        "War Attack": 0,
        "War Streak": "NO",
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#26",
        "Name": "itZDeniz1",
        "WAR": "OUT",
        "War Attack": 0,
        "War Streak": "NO",
        "Clan Capital Attack": 4,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#27",
        "Name": "Mimi7",
        "WAR": "IN",
        "War Attack": 12,
        "War Streak": "NO",
        "Clan Capital Attack": 8,
        "Clan Games": 1,
        "Clan Capital Maxed": 1,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#28",
        "Name": "arggggggah",
        "WAR": "IN",
        "War Attack": 2,
        "War Streak": "NO",
        "Clan Capital Attack": 25,
        "Clan Games": 4,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#29",
        "Name": "GOD OF UNDEAD",
        "WAR": "IN",
        "War Attack": 0,
        "War Streak": "NO",
        "Clan Capital Attack": 23,
        "Clan Games": 1,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#30",
        "Name": "Xbowskill",
        "WAR": "IN",
        "War Attack": 4,
        "War Streak": "NO",
        "Clan Capital Attack": 14,
        "Clan Games": 2,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#31",
        "Name": "devil recite",
        "WAR": "IN",
        "War Attack": 3,
        "War Streak": "NO",
        "Clan Capital Attack": 7,
        "Clan Games": 1,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#32",
        "Name": "jai hind",
        "WAR": "IN",
        "War Attack": 6,
        "War Streak": "YES",
        "Clan Capital Attack": 5,
        "Clan Games": 1,
        "Clan Capital Maxed": 1,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#33",
        "Name": "VRK",
        "WAR": "IN",
        "War Attack": 29,
        "War Streak": "NO",
        "Clan Capital Attack": 12,
        "Clan Games": 5,
        "Clan Capital Maxed": 3,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#34",
        "Name": "Rafael",
        "WAR": "IN",
        "War Attack": 15,
        "War Streak": "NO",
        "Clan Capital Attack": 6,
        "Clan Games": 2,
        "Clan Capital Maxed": 2,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#35",
        "Name": "arshul",
        "WAR": "IN",
        "War Attack": 1,
        "War Streak": "NO",
        "Clan Capital Attack": 22,
        "Clan Games": 2,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#36",
        "Name": "lil homie",
        "WAR": "IN",
        "War Attack": 8,
        "War Streak": "NO",
        "Clan Capital Attack": 0,
        "Clan Games": 1,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#37",
        "Name": "Mar€lyn",
        "WAR": "IN",
        "War Attack": 2,
        "War Streak": "NO",
        "Clan Capital Attack": 1,
        "Clan Games": 1,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#38",
        "Name": "Rider_22",
        "WAR": "IN",
        "War Attack": 1,
        "War Streak": "NO",
        "Clan Capital Attack": 3,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#39",
        "Name": "Noob3",
        "WAR": "IN",
        "War Attack": 0,
        "War Streak": "NO",
        "Clan Capital Attack": 0,
        "Clan Games": 1,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#40",
        "Name": "kindstonde17",
        "WAR": "IN",
        "War Attack": 4,
        "War Streak": "NO",
        "Clan Capital Attack": 17,
        "Clan Games": 4,
        "Clan Capital Maxed": 1,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#41",
        "Name": "evil_dancer",
        "WAR": "IN",
        "War Attack": 0,
        "War Streak": "NO",
        "Clan Capital Attack": 7,
        "Clan Games": 4,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#42",
        "Name": "Yash",
        "WAR": "IN",
        "War Attack": 3,
        "War Streak": "NO",
        "Clan Capital Attack": 19,
        "Clan Games": 4,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#43",
        "Name": "Pro@:",
        "WAR": "IN",
        "War Attack": 2,
        "War Streak": "NO",
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#44",
        "Name": "john cena",
        "WAR": "IN",
        "War Attack": 1,
        "War Streak": "YES",
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#45",
        "Name": "Kebab",
        "WAR": "IN",
        "War Attack": 0,
        "War Streak": "NO",
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    },
    {
        "Unique ID": "COCAR#46",
        "Name": "Admiral-V",
        "WAR": "IN",
        "War Attack": 1,
        "War Streak": "YES",
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0,
        "Status": "Elder"
    }
]

data_non_mem=[
    {
        "Unique ID": "COCAR#47",
        "Name": "KING SEENU",
        "War Attack": 40,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#48",
        "Name": "A'MIRAH",
        "War Attack": 6,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#49",
        "Name": "BONH",
        "War Attack": 18,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#50",
        "Name": "TVOY",
        "War Attack": 22,
        "Clan Capital Attack": 2,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#51",
        "Name": "SHARPZY",
        "War Attack": 9,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#52",
        "Name": "SAKLEN",
        "War Attack": 4,
        "Clan Capital Attack": 7,
        "Clan Games": 2,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#53",
        "Name": "KING SEENU2",
        "War Attack": 5,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#54",
        "Name": "BAJIRAV",
        "War Attack": 1,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#55",
        "Name": "DAMIAN",
        "War Attack": 0,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#56",
        "Name": "Mohammad Jeddi",
        "War Attack": 6,
        "Clan Capital Attack": 0,
        "Clan Games": 1,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#57",
        "Name": "spa ek",
        "War Attack": 20,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#58",
        "Name": "Deep",
        "War Attack": 8,
        "Clan Capital Attack": 3,
        "Clan Games": 2,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#59",
        "Name": "Hannah",
        "War Attack": 0,
        "Clan Capital Attack": 9,
        "Clan Games": 1,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#60",
        "Name": "Younes",
        "War Attack": 0,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#61",
        "Name": "paul",
        "War Attack": 0,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#62",
        "Name": "AR Rasel@",
        "War Attack": 0,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#63",
        "Name": "PRODIP",
        "War Attack": 1,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#64",
        "Name": "rilof",
        "War Attack": 0,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#65",
        "Name": "sb1010",
        "War Attack": 0,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#66",
        "Name": "Matt Ox",
        "War Attack": 1,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#67",
        "Name": "Janaka anuruddh",
        "War Attack": 0,
        "Clan Capital Attack": 3,
        "Clan Games": 2,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#68",
        "Name": "Tempete de feu",
        "War Attack": 0,
        "Clan Capital Attack": 2,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#69",
        "Name": "TIRTHA",
        "War Attack": 0,
        "Clan Capital Attack": 3,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#70",
        "Name": "podda2",
        "War Attack": 1,
        "Clan Capital Attack": 2,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#71",
        "Name": "Cat",
        "War Attack": 0,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#72",
        "Name": "griff",
        "War Attack": 3,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#73",
        "Name": "coc",
        "War Attack": 5,
        "Clan Capital Attack": 2,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#74",
        "Name": "ANSAAR75",
        "War Attack": 5,
        "Clan Capital Attack": 6,
        "Clan Games": 4,
        "Clan Capital Maxed": 2
    },
    {
        "Unique ID": "COCAR#75",
        "Name": "TOFITA",
        "War Attack": 25,
        "Clan Capital Attack": 11,
        "Clan Games": 4,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#76",
        "Name": "Mdoge",
        "War Attack": 2,
        "Clan Capital Attack": 2,
        "Clan Games": 2,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#77",
        "Name": "abhi",
        "War Attack": 0,
        "Clan Capital Attack": 3,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#78",
        "Name": "erase",
        "War Attack": 5,
        "Clan Capital Attack": 5,
        "Clan Games": 1,
        "Clan Capital Maxed": 1
    },
    {
        "Unique ID": "COCAR#79",
        "Name": "am.ak",
        "War Attack": 1,
        "Clan Capital Attack": 7,
        "Clan Games": 1,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#80",
        "Name": "SPARSH",
        "War Attack": 0,
        "Clan Capital Attack": 2,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#81",
        "Name": "Jaryn",
        "War Attack": 7,
        "Clan Capital Attack": 2,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#82",
        "Name": "Dr.Neuro",
        "War Attack": 0,
        "Clan Capital Attack": 4,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#83",
        "Name": "NdaHH_",
        "War Attack": 1,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#84",
        "Name": "Spider-Man",
        "War Attack": 0,
        "Clan Capital Attack": 4,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#85",
        "Name": "midouja",
        "War Attack": 1,
        "Clan Capital Attack": 4,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#86",
        "Name": "arthur",
        "War Attack": 0,
        "Clan Capital Attack": 4,
        "Clan Games": 1,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#87",
        "Name": "Rabrabyeojhan",
        "War Attack": 1,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#88",
        "Name": "Brenne's CAMP!",
        "War Attack": 0,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#89",
        "Name": "mb102006",
        "War Attack": 0,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#90",
        "Name": "real_Maty1255",
        "War Attack": 0,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#91",
        "Name": "yungaid",
        "War Attack": 1,
        "Clan Capital Attack": 1,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    },
    {
        "Unique ID": "COCAR#92",
        "Name": "UILeMaNn",
        "War Attack": 0,
        "Clan Capital Attack": 0,
        "Clan Games": 0,
        "Clan Capital Maxed": 0
    }
]

@app.route("/")
def hello_world():
    return render_template('home.html',DM=data_mem,DNM=data_non_mem)

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)