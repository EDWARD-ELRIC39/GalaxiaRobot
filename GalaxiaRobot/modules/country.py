# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""


import flag
from countryinfo import CountryInfo

from GalaxiaRobot import telethn as borg
from GalaxiaRobot.events import register


@register(pattern="^/country (.*)")
async def msg(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    lol = input_str
    country = CountryInfo(lol)
    try:
        a = country.info()
    except:
        await event.reply("ᴄᴏᴜɴᴛʀʏ ɴᴏᴛ ᴀᴠᴀɪᴀʙʟᴇ ᴄᴜʀʀᴇɴᴛʟʏ")
    name = a.get("name")
    bb = a.get("altSpellings")
    hu = ""
    for p in bb:
        hu += p + ",  "

    area = a.get("area")
    borders = ""
    hell = a.get("borders")
    for fk in hell:
        borders += fk + ",  "

    call = ""
    WhAt = a.get("callingCodes")
    for what in WhAt:
        call += what + "  "

    capital = a.get("capital")
    currencies = ""
    fker = a.get("currencies")
    for FKer in fker:
        currencies += FKer + ",  "

    HmM = a.get("demonym")
    geo = a.get("geoJSON")
    pablo = geo.get("features")
    Pablo = pablo[0]
    PAblo = Pablo.get("geometry")
    EsCoBaR = PAblo.get("type")
    iso = ""
    iSo = a.get("ISO")
    for hitler in iSo:
        po = iSo.get(hitler)
        iso += po + ",  "
    fla = iSo.get("alpha2")
    nox = fla.upper()
    okie = flag.flag(nox)

    languages = a.get("languages")
    lMAO = ""
    for lmao in languages:
        lMAO += lmao + ",  "

    nonive = a.get("nativeName")
    waste = a.get("population")
    reg = a.get("region")
    sub = a.get("subregion")
    tik = a.get("timezones")
    tom = ""
    for jerry in tik:
        tom += jerry + ",   "

    GOT = a.get("tld")
    lanester = ""
    for targaryen in GOT:
        lanester += targaryen + ",   "

    wiki = a.get("wiki")

    caption = f"""<b><u>Information Gathered Successfully</b></u>
<b>
ᴄᴏᴜɴᴛʀʏ ɴᴀᴍᴇ:- {name}
ᴀʟᴛᴇʀɴᴀᴛɪᴠᴇ ꜱᴘᴇʟʟɪɴɢꜱ:- {hu}
ᴄᴏᴜɴᴛʀʏ ᴀʀᴇᴀ:- {area} square kilometers
ʙᴏʀᴅᴇʀꜱ:- {borders}
ᴄᴀʟʟɪɴɢ ᴄᴏᴅᴇꜱ:- {call}
ᴄᴏᴜɴᴛʀʏ Capital:- {capital}
Country's ᴄᴜʀʀᴇɴᴄʏ:- {currencies}
ᴄᴏᴜɴᴛʀʏ ғʟᴀɢ:- {okie}
ᴅᴇᴍᴏɴʏᴍ:- {HmM}
ᴄᴏᴜɴᴛʀʏ ᴛʏᴘᴇ:- {EsCoBaR}
ɪꜱᴏ ɴᴀᴍᴇꜱ:- {iso}
ʟᴀɴɢᴜᴀɢᴇꜱ:- {lMAO}
ɴᴀᴛɪᴠᴇ ɴᴀᴍᴇ:- {nonive}
ᴘᴏᴘᴜʟᴀᴛɪᴏɴ:- {waste}
ʀᴇɢɪᴏɴ:- {reg}
ꜱᴜʙ ʀᴇɢɪᴏɴ:- {sub}
ᴛɪᴍᴇ ᴢᴏɴᴇꜱ:- {tom}
ᴛᴏᴘ ʟᴇᴠᴇʟ ᴅᴏᴍᴀɪɴ:- {lanester}
ᴡɪᴋɪᴘᴇᴅɪᴀ:- {wiki}</b>

ɢᴀᴛʜᴇʀᴇᴅ ʙʏ. ⍟ ɢᴀʟᴀxɪᴀ ʀᴏʙᴏᴛ. ⍟ .</b>
"""

    await borg.send_message(
        event.chat_id,
        caption,
        parse_mode="HTML",
    )

    await event.delete()
