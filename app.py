from flask import Flask , render_template,jsonify
from database import load_from_db


app = Flask(__name__)



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
def coc_ancient_ruins():
    mem_list=load_from_db()
    return render_template('home.html',DM=mem_list,DNM=data_non_mem)

if __name__ == '__main__':
  app.run(host='0.0.0.0',debug=True)