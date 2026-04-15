import discord, random, asyncio, json, os, time, aiohttp
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timezone, timedelta

# ═══════════════════════════════════════════
#           KONFIGURACIJA
# ═══════════════════════════════════════════
BOT_NAME = "oleun"
VERSION  = "6.0 BALKAN EDITION"
TOKEN    = os.environ.get("DISCORD_TOKEN")

COLORS = {
    "default": 0x5865F2, "success": 0x2ECC71, "error":   0xE74C3C,
    "warning": 0xF39C12, "info":    0x3498DB, "gold":    0xF1C40F,
    "balkan":  0xC8102E, "purple":  0x9B59B6, "fun":     0xFF69B4,
    "dark":    0x2C2F33, "teal":    0x1ABC9C, "love":    0xFF4D6D,
    "pink":    0xFF85A1,
}

JOBS = [
    "Radio si kao konobar 🍺", "Čuvao si baku 🧓", "Prodavao ćevape 🥙",
    "Vozio si taksi 🚕", "Radio si na građevini 🏗️", "Popravljao auta 🔧",
    "Čuvao parking 🚗", "Nosio poštu 📬", "Prodavao lubenicu 🍉",
    "Brao paprike u polju 🌶️", "Radio u pekari 🥖", "Čuvao ovce 🐑",
    "Prodavao karte na stanici 🚌", "Radio kao zaštitar 💪", "Prao automobile 🚿",
]

EIGHTBALL_REPLIES = [
    "🟢 Definitivno da!", "🟢 Sve znakovi govore — DA.",
    "🟢 Bez ikakve sumnje, majstore!", "🟢 Računaj na to, brate.",
    "🟡 Pitaj ponovo malo kasnije.", "🟡 Nisam baš siguran, brate.",
    "🟡 Teško reći u ovom trenutku.", "🟡 Magla mi zaklanja odgovor.",
    "🔴 Ne računaj na to.", "🔴 Odgovor je jasno — NE.",
    "🔴 Izgledi su jako loši.", "🔴 Zaboravi na to, majstore.",
]

# ═══════════════════════════════════════════
#    MEMOVI (veliki bazen sa rotacijom)
# ═══════════════════════════════════════════
MEMES = [
    "Kad kažeš 'samo još 5 minuta' a prođe 3 sata. 😴📱",
    "Baka: 'Jesi li jeo?' Ti: 'Jesam.' Baka: 'A jesi li gladan?' 🍽️👵",
    "Kad upališ klimu na 16°C a napolju je 40°C. ❄️🥵",
    "Turbofolk u 3 ujutru, sutra na posao u 7. 🎶😵",
    "Kad kažeš 'idemo na kafu' a završiš na roštilju do zore. 🥩🍻",
    "Svaki Balkanac ima ujaka koji sve zna popraviti. 🔧😂",
    "'Sačekaj 5 minuta' — Balkan vreme: 45 minuta minimum. ⏰🤌",
    "Kad pitaš baku za recept: 'Malo ovog, malo onog, dok ne bude dobro.' 📏👵",
    "Kad kaže 'idem odmah' a gleda TV već sat vremena. 📺🛋️",
    "Ništa me ne boli više nego kad mi telefon padne na lice u krevetu. 📱😩",
    "Balkan dijetа: ne jedeš između obroka. Obroci su svaki sat. 🍴⏱️",
    "Komšija u 11 noću: buši zidove. Normalnost. 🔨🏠",
    "Kad mama kaže 'pričekaj dok dođemo kući' — Bog te čuvaj. 😰🏡",
    "'Idemo samo na malo' — 6 sati kasnije. 😂⌛",
    "Kad vidiš stranca u selu svi izlaze da gledaju. 👀🏡",
    "Balkan autopilot: čim sjedneš — telefon u ruci. 📱🧠",
    "Svaka baka misli da je njeno dijete premršavo. Vaga se ne slaže. ⚖️👵",
    "Na Balkanu se ne kaže 'hvala' u kafani. Prstom se kuca po stolu. 🫵☕",
    "Kad kažeš da si sit a vidiš čevape. 🥙😤",
    "Balkanska logika: ne možeš biti bolestan ljeti, samo zimi. ☀️🤧",
    "Baka čuva svaku vrećicu od kupovine već 30 godina. 🛍️♻️",
    "Kad ti kaže 'nisam ljuta' — bježi. 😬💨",
    "Balkanska dijalektika: svaka rasprava završi pričom o ratu. ⚔️🗣️",
    "Pranje auta = kiša za 2 sata garantovana. 🚗🌧️",
    "Kada slušaš muziku na slušalicama a mama govori s tobom. 🎧😤",
    "Spavanje na plaži sa šeširom na licu. Balkanski ljetni odmor. 🏖️👒",
    "Na Balkanu svadbena muzika mora biti glasnija od aviona. ✈️🎵",
    "'Ajde brzo' — 20 minuta čekanja. 🏃⏳",
    "Kad dobiješ viber poruku od mame u 2 noću: 'Jesi li stigao?' 📲😅",
    "Piknik bez kajmaka — nije piknik. 🧀🌿",
    "Svaki kvar na autu Balkanac može dijagnosticirati zvukom. 🚗👂",
    "Kad ti komšija javi vijest koja nije tvoja stvar. 📰🙄",
    "Ljeto = hvatanje klime ispod jorgana. 🛏️❄️",
    "Balkan parking: dvije linije? Staju četiri auta. 🚙😂",
    "Fritula je rješenje za sve životne probleme. 🍩🫶",
    "Kad dođe familija iznenada a kuća nije čista. 😱🧹",
    "Svako putovanje počinje sa 'imaš li pare za autoput?'. 🛣️💶",
    "Baka na kafi: zna sve o svima u gradu. 👵☕📰",
    "Balkanska statistika: 9 od 10 problema se rješava uz kafu. ☕📊",
    "'Otišao sam samo po hleb' — vratio se sa pola marketa. 🛒😅",
    "Kad igraš fudbal na ulici i lopta ode kod ljutog komšije. ⚽😰",
    "Svaki razgovor na Balkanu počne sa: 'Brate, slušaj ovo...' 🗣️👂",
    "Dnevna soba samo za goste. Gosti nikad ne dolaze. 🛋️🔒",
    "Šalter na pošti: radi jedan, čekaju trideset. 🏢😑",
    "Kad se probudi baka u 5 ujutru i odmah počne pjevati. 🌅🎵👵",
    "Balkanski sat: 'Dođi u 7' znači dođi u 8:30. 🕖😄",
    "Svaka kuća ima baku koja čuva bombone od 1998. 🍬👵",
    "Na Balkanu, ako ne jedeš treću porciju, nisi počašćen. 🍽️😅",
    "Kad završiš posao i nema struje za punjač. 🔌😩",
    "Balkanac na moru: čeka red u restoranu, naruči duplo, pojede četvoro. 🍴🌊",
    "Usred filma: 'Koliko još traje?' — Baš na napetom dijelu. 🎬😤",
    "Kad kaže 'jesi li gladan?' a hrana je već na stolu. 🍲🏃",
    "Svaka balkanska mama je doktor, kuhar i psiholog u jednom. 👩‍⚕️👩‍🍳🧠",
    "Kad ideš kod zubara a zub prestane boljeti čim sjedneš u čekaonicu. 🦷😤",
    "Balkan net: radi samo kad ne trebaš. 📶🙃",
    "Djeca na Balkanu idu van da se igraju — mama zna sve što su radila. 🏃👁️",
    "Kad vidiš kišu a majka te pita jesi li ponio kapu. 🌧️🧢",
    "Jedina stvar brža od vijesti na Balkanu — trač. 👄⚡",
    "Svaki rodjak želi znati kada se ženiš. Svake godine. 💍😭",
    "Na ljetovanju: sunce, more i debata gdje ćemo ručati 2 sata. 🌞🍽️",
    "Balkanac u inostranstvu: pronađe Balkanca u roku 10 minuta. 🌍🤝",
    "Kad čistiš sobu a mama kaže 'baciš li to, ubijam te'. 🗑️😅",
    "Fijaker sa konjima sporiji od balkanskog interneta. 🐴📶",
    "Svaka baka krije novac u džepu kecelje. 💸👵",
    "Domaći sok od šljive — lijek za sve. 🍑💊",
    "Balkan dijalog: 'Jesi jeo?' 'Jesam.' 'Jedi još.' 🍽️🔄",
    "Kad nema struje — svi izađu napolje i postanu filozofi. 🕯️🧠",
    "Majka ne razumije 'meni ništa ne treba za rodjendan'. 🎁👩‍👦",
    "Na Balkanu kafu piješ u svakoj kući čak i ako si 'samo svrnuo'. ☕🏠",
    "Djeca na Balkanu nemaju 'slobodnog vremena' — ima posla uvijek. 🧹⏰",
    "Balkan parking 2: dvostruki parking je tradicija, ne greška. 🚗🚗",
    "Svako selo ima svog vračara i svi tvrde da ne vjeruju. 🔮😏",
    "Kad mama pita 'gdje si bio?' a ti bio u WC-u. 🚽😤",
    "Balkan zimovanje: pečenje kestena i debata o politici. 🌰🗳️",
    "Sendvič koji je spakovao ko znaš uvijek je bolji. 🥪❤️",
    "Svaki kafić ima isti TV kanal i uvijek su vijesti. 📺☕",
    "Balkanski wifi lozinka: nešto poput 'qwerty1234'. 📶😂",
    "Kad igraš tablić i gledaš protivnikove karte u odrazu prozora. 🃏👁️",
    "Balkan letovanje: čekaš godinu dana, provedeš 7 dana, žališ se pola godine. 🌊😤",
    "Svaka balkanska mama reciklira plastične flaše u vazi. 🌺♻️",
    "Kad rjeknete 'ajde' a niko se ne miče. 🚶🗿",
    "Balkan shopping: ideš po jedno, vratiš se sa svime osim tog jednog. 🛍️😅",
]

MEME_STATE: dict = {}  # guild_id -> shuffled list of remaining indices

def get_next_meme(guild_id: int) -> str:
    key = str(guild_id)
    if key not in MEME_STATE or not MEME_STATE[key]:
        idxs = list(range(len(MEMES)))
        random.shuffle(idxs)
        MEME_STATE[key] = idxs
    return MEMES[MEME_STATE[key].pop()]

# ═══════════════════════════════════════════
#    VJEŠALA — rječnik
# ═══════════════════════════════════════════
VJASALA_RJECNIK = [
    "RAKIJA","CEVAPI","BALKON","KAFANA","MARKET","TRAKTOR","KOMSIJA","BONTON",
    "FUDBAL","PAPRIKA","BUREK","KAJMAK","SARMA","KIFLA","PEKARA","BAKLAVA",
    "KOMPJUTER","INTERNET","MOBITEL","PUNJAC","SLUSALICE","TASTATURA","MIŠKA",
    "PLANINA","JEZERO","RIJEKA","SUMSKA","LIVADA","VRELO","KLISURA","BRDOVIT",
    "LIJENOST","MUDROST","HRABROST","ZIVAHNA","BRZINA","TOPLINA","VESELJE",
    "BAKA","DJED","STRIC","UJNA","BRAT","SESTRA","MAJKA","OTAC","DIJETE",
    "KREVET","STOLICA","ORMAR","ZAVJESA","TEPIH","OGLEDALO","PROZOR","VRATA",
    "KOKOSOVO","JAGODA","MALINA","BOROVNICA","SMOKVA","SLJIVA","TRESNJA",
    "AUTOMOBIL","MOTOCIKL","BICIKL","AVION","BROD","VAGON","TRAMVAJ","METRO",
    "GITARA","VIOLINA","BUBNJEVI","FLAUTA","KLAVIR","HARMONIKA","SAKSOFON",
    "POLICAJAC","VATROGASAC","LJEKAR","UCITELJ","NOVINAR","ARHITEKT","INZENJER",
    "SUNCOKREO","RUZA","LAVANDA","KAKTUS","TULIPAN","JORGOVANA","MASLACAK",
    "OBLAK","MUNJA","GROM","SNIJEG","ROSA","MAGLA","VJETAR","OLUJA","DUGA",
    "LEPTIR","PCELICA","BUBAMARA","VJEVERICA","JELEN","LISICA","MEDVJED","VUK",
    "TORTA","KOLAC","KROFNA","PALACINKA","WAFFLE","BROWNIE","TIRAMISU","MACARON",
    "KUHINJA","KUPATILO","HODNIK","PODRUM","TAVAN","GARAZ","BALKON","TERASA",
    "SLOBODA","JEDNAKOST","LJUBAV","NADA","VJERA","SREĆA","ISTINA","PRAVDA",
    "GIMNASTIKA","PLIVANJE","ATLETIKA","KOSARKA","ODBOJKA","TENIS","SAHI","BOKS",
    "JANUAR","FEBRUAR","OKTOBAR","NOVEMBAR","DECEMBAR","SUBOTA","NEDJELJA",
    "DUGACAK","KRATAK","VISOK","NIZAK","DEBEO","MRSAV","BRZO","POLAKO","GLASNO",
]

VJASALA_FAZE = [
    "```\n  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========```",
    "```\n  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========```",
]

# ═══════════════════════════════════════════
#    INTENTS & BOT
# ═══════════════════════════════════════════
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ═══════════════════════════════════════════
#    PODACI
# ═══════════════════════════════════════════
DATA_FILE = "oleun_data.json"
data = {"economy": {}, "xp": {}, "warnings": {}}

def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            data["economy"]  = loaded.get("economy", {})
            data["xp"]       = loaded.get("xp", {})
            data["warnings"] = loaded.get("warnings", {})

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

load_data()

def get_economy(uid):
    key = str(uid)
    if key not in data["economy"]:
        data["economy"][key] = {"balance": 500, "last_work": 0, "last_daily": 0}
    d = data["economy"][key]
    d.setdefault("last_daily", 0)
    return d

def get_xp(uid):
    key = str(uid)
    if key not in data["xp"]:
        data["xp"][key] = {"xp": 0, "level": 1}
    return data["xp"][key]

def add_xp(uid, amount):
    d = get_xp(uid)
    d["xp"] += amount
    needed = d["level"] * 100
    if d["xp"] >= needed:
        d["xp"] -= needed
        d["level"] += 1
        return True
    return False

def get_warnings(guild_id, uid):
    gk, uk = str(guild_id), str(uid)
    data["warnings"].setdefault(gk, {})
    data["warnings"][gk].setdefault(uk, [])
    return data["warnings"][gk][uk]

# ═══════════════════════════════════════════
#    EMBED HELPER
# ═══════════════════════════════════════════
def em(title, desc="", color=COLORS["balkan"], fields=None, footer=None, thumb=None, image=None):
    e = discord.Embed(title=title, description=desc, color=color, timestamp=datetime.now(timezone.utc))
    if fields:
        for n, v, inline in fields:
            e.add_field(name=n, value=v or "\u200b", inline=inline)
    e.set_footer(text=footer or f"{BOT_NAME} {VERSION}")
    if thumb:  e.set_thumbnail(url=thumb)
    if image:  e.set_image(url=image)
    return e

# ═══════════════════════════════════════════
#    GIF HELPER (nekos.best)
# ═══════════════════════════════════════════
async def get_gif(action: str) -> str | None:
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://nekos.best/api/v2/{action}", timeout=aiohttp.ClientTimeout(total=5)) as r:
                if r.status == 200:
                    j = await r.json()
                    return j["results"][0]["url"]
    except:
        pass
    return None

# ═══════════════════════════════════════════
#    EVENTI
# ═══════════════════════════════════════════
@bot.event
async def on_ready():
    print(f"\n{'═'*45}\n  {BOT_NAME} {VERSION} — ONLINE\n{'═'*45}")
    for guild in bot.guilds:
        try:
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync(guild=guild)
            print(f"  ✔ {guild.name} ({guild.member_count} članova)")
        except Exception as e:
            print(f"  ✘ {guild.name}: {e}")
    print(f"{'═'*45}\n")
    change_status.start()

@bot.event
async def on_member_join(member):
    chan = discord.utils.get(member.guild.text_channels, name="welcome")
    if not chan: return
    e = discord.Embed(
        title=f"🎉 Dobrodošao, {member.display_name}!",
        description=f"Hej {member.mention}! Drago nam je što si stigao! 🇷🇸\nUpoznaj se, ispoštuj pravila i uživaj! 🍻",
        color=COLORS["success"], timestamp=datetime.now(timezone.utc)
    )
    e.set_thumbnail(url=member.display_avatar.url)
    e.add_field(name="👥 Član broj", value=f"`{member.guild.member_count}`", inline=True)
    e.set_footer(text=f"{BOT_NAME} • Dobrodošlica")
    await chan.send(embed=e)

@bot.event
async def on_member_remove(member):
    chan = discord.utils.get(member.guild.text_channels, name="welcome")
    if not chan: return
    e = discord.Embed(
        title=f"👋 {member.display_name} je napustio server",
        description=f"Žao nam je što ode {member.mention}. Srećno! 🙏",
        color=COLORS["error"], timestamp=datetime.now(timezone.utc)
    )
    e.set_thumbnail(url=member.display_avatar.url)
    e.set_footer(text=f"{BOT_NAME} • Oproštaj")
    await chan.send(embed=e)

@bot.event
async def on_message(message):
    if message.author.bot: return

    # ── Kaladont handler ──────────────────────────────
    if message.channel.id in kaladont_games and not message.content.startswith("/"):
        game = kaladont_games[message.channel.id]
        word = message.content.upper().strip()
        letters = game["letters"]
        req = game["word"][-letters:]

        async def reject(reason: str):
            err = await message.channel.send(
                embed=em("❌ " + reason, f"Potrebno: počinje sa **`{req}`**", color=COLORS["error"]),
                delete_after=5
            )
            try: await message.delete()
            except: pass

        if not word.isalpha():
            pass  # ignore non-word messages silently
        elif len(word) < 3:
            await reject("Prekratka! Min 3 slova.")
        elif word[:letters] != req:
            await reject(f"Mora početi sa **`{req}`**! Tvoja: `{word}`")
        elif word in game["used"]:
            await reject(f"`{word}` je već bila!")
        else:
            game["word"] = word
            game["used"].add(word)
            game["chain"].append((word, message.author.display_name))
            try: await message.delete()
            except: pass
            if game["msg"]:
                try:
                    await game["msg"].edit(
                        embed=kaladont_embed(game, f"✅ **{message.author.display_name}** → `{word}`", COLORS["success"])
                    )
                except: pass
        return  # don't process XP for kaladont channel messages

    # ── XP ────────────────────────────────────────────
    if random.random() < 0.12:
        if add_xp(message.author.id, random.randint(5, 20)):
            save_data()
            lvl = get_xp(message.author.id)["level"]
            lv_em = discord.Embed(
                title="🎊 LEVEL UP!",
                description=f"{message.author.mention} prešao na **Level {lvl}**! Svaka čast! 🏆",
                color=COLORS["gold"], timestamp=datetime.now(timezone.utc)
            )
            lv_em.set_thumbnail(url=message.author.display_avatar.url)
            lv_em.set_footer(text=f"{BOT_NAME} • XP Sistem")
            await message.channel.send(embed=lv_em, delete_after=10)
    await bot.process_commands(message)

@bot.command(name="sync")
@commands.has_permissions(administrator=True)
async def sync_cmd(ctx):
    try:
        bot.tree.copy_global_to(guild=ctx.guild)
        synced = await bot.tree.sync(guild=ctx.guild)
        await ctx.send(embed=em("✅ Sinhronizovano!", f"`{len(synced)}` komandi registrovano.", color=COLORS["success"]))
    except Exception as e:
        await ctx.send(embed=em("❌ Greška", str(e), color=COLORS["error"]))

@tasks.loop(seconds=30)
async def change_status():
    statuses = [
        discord.Activity(type=discord.ActivityType.playing,   name=f"/help | {BOT_NAME}"),
        discord.Activity(type=discord.ActivityType.watching,  name="Balkanske drame 🎭"),
        discord.Activity(type=discord.ActivityType.competing, name="kocki i rakiji 🍻"),
        discord.Activity(type=discord.ActivityType.listening, name="turbofolk 🎶"),
        discord.CustomActivity(name="💰 Ekonomija • 🎮 Igre • ❤️ Ljubav"),
    ]
    await bot.change_presence(activity=random.choice(statuses))

# ═══════════════════════════════════════════
#    INFO & UTILS
# ═══════════════════════════════════════════
@bot.tree.command(name="ping", description="🏓 Provjeri brzinu bota")
async def ping(i: discord.Interaction):
    ms = round(bot.latency * 1000)
    status, color = ("🟢 Odlično", COLORS["success"]) if ms < 80 else ("🟡 Dobro", COLORS["warning"]) if ms < 180 else ("🔴 Sporo", COLORS["error"])
    await i.response.send_message(embed=em("🏓 Pong!", color=color, fields=[
        ("📡 Latency", f"`{ms}ms`", True), ("📊 Status", status, True), ("🤖 Bot", f"`{bot.user}`", True)
    ]))

@bot.tree.command(name="serverinfo", description="📊 Informacije o serveru")
async def serverinfo(i: discord.Interaction):
    g = i.guild
    bots, humans = sum(1 for m in g.members if m.bot), g.member_count - sum(1 for m in g.members if m.bot)
    await i.response.send_message(embed=em(f"🏰 {g.name}", color=COLORS["purple"], thumb=g.icon.url if g.icon else None, fields=[
        ("👑 Vlasnik",   g.owner.mention,                                        True),
        ("👥 Članovi",   f"`{humans}` ljudi • `{bots}` botova",                 True),
        ("📅 Kreiran",   g.created_at.strftime("%d.%m.%Y."),                    True),
        ("💬 Kanali",    f"`{len(g.text_channels)}` tekst • `{len(g.voice_channels)}` voice", True),
        ("🏷️ Uloge",    f"`{len(g.roles)-1}`",                                  True),
        ("🚀 Boostovi",  f"`{g.premium_subscription_count or 0}`",              True),
    ]))

@bot.tree.command(name="userinfo", description="👤 Informacije o korisniku")
async def userinfo(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    eco, xpd = get_economy(u.id), get_xp(u.id)
    warns = len(get_warnings(i.guild.id, u.id))
    await i.response.send_message(embed=em(f"👤 {u.display_name}", color=u.accent_color or COLORS["default"], thumb=u.display_avatar.url, fields=[
        ("🆔 ID",          f"`{u.id}`",                                            True),
        ("📅 Pridružio",   u.joined_at.strftime("%d.%m.%Y.") if u.joined_at else "N/A", True),
        ("🏷️ Top uloga",  u.top_role.mention,                                    True),
        ("💰 Balans",      f"`{eco['balance']:,} 💶`",                            True),
        ("📈 Level",       f"`{xpd['level']}`",                                   True),
        ("⚠️ Upozorenja",  f"`{warns}`",                                           True),
    ]))

@bot.tree.command(name="avatar", description="🖼️ Prikaži avatar korisnika")
async def avatar(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    await i.response.send_message(embed=em(f"🖼️ {u.display_name}",
        f"[PNG]({u.display_avatar.with_format('png').url}) • [JPG]({u.display_avatar.with_format('jpg').url}) • [WEBP]({u.display_avatar.with_format('webp').url})",
        color=COLORS["info"], image=u.display_avatar.url))

@bot.tree.command(name="say", description="🗣️ Bot šalje poruku")
@app_commands.checks.has_permissions(manage_messages=True)
async def say(i: discord.Interaction, tekst: str, kanal: discord.TextChannel = None):
    target = kanal or i.channel
    await target.send(tekst, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))
    await i.response.send_message(embed=em("✅ Poslato!", f"Kanal: {target.mention}", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="setname", description="✏️ Promeni ime bota")
@app_commands.checks.has_permissions(administrator=True)
async def setname(i: discord.Interaction, ime: str):
    try:
        await bot.user.edit(username=ime)
        e = em("✅ Ime promenjeno!", f"Novo ime: **{ime}**", color=COLORS["success"])
    except discord.HTTPException as ex:
        e = em("❌ Greška", f"{ex}\n*Max 2 promene na 10 min*", color=COLORS["error"])
    await i.response.send_message(embed=e, ephemeral=True)

@bot.tree.command(name="setavatar", description="🖼️ Promeni sliku bota")
@app_commands.checks.has_permissions(administrator=True)
async def setavatar(i: discord.Interaction, url: str):
    await i.response.defer(ephemeral=True)
    try:
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url) as resp:
                if resp.status != 200:
                    return await i.followup.send(embed=em("❌ Greška", "Ne mogu preuzeti sliku.", color=COLORS["error"]), ephemeral=True)
                img = await resp.read()
        await bot.user.edit(avatar=img)
        e = em("✅ Avatar promenjen!", "Nova slika je postavljena!", color=COLORS["success"], thumb=url)
    except Exception as ex:
        e = em("❌ Greška", str(ex), color=COLORS["error"])
    await i.followup.send(embed=e, ephemeral=True)

# ═══════════════════════════════════════════
#    MODERACIJA
# ═══════════════════════════════════════════
@bot.tree.command(name="ban", description="🔨 Banuj korisnika")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(i: discord.Interaction, korisnik: discord.Member, razlog: str = "Bez razloga"):
    if korisnik.top_role >= i.user.top_role:
        return await i.response.send_message(embed=em("❌ Greška", "Ne možeš banovati nekoga sa višom ulogom!", color=COLORS["error"]), ephemeral=True)
    await korisnik.ban(reason=razlog)
    await i.response.send_message(embed=em("🔨 Banovan", color=COLORS["error"], thumb=korisnik.display_avatar.url, fields=[
        ("👤 Korisnik", f"{korisnik} (`{korisnik.id}`)", False),
        ("📝 Razlog", razlog, False), ("🛡️ Moderator", i.user.mention, False),
    ]))

@bot.tree.command(name="kick", description="👢 Izbaci korisnika")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(i: discord.Interaction, korisnik: discord.Member, razlog: str = "Bez razloga"):
    if korisnik.top_role >= i.user.top_role:
        return await i.response.send_message(embed=em("❌ Greška", "Ne možeš izbaciti nekoga sa višom ulogom!", color=COLORS["error"]), ephemeral=True)
    await korisnik.kick(reason=razlog)
    await i.response.send_message(embed=em("👢 Izbačen", color=COLORS["warning"], thumb=korisnik.display_avatar.url, fields=[
        ("👤 Korisnik", f"{korisnik} (`{korisnik.id}`)", False),
        ("📝 Razlog", razlog, False), ("🛡️ Moderator", i.user.mention, False),
    ]))

@bot.tree.command(name="timeout", description="⏱️ Ućutkaj korisnika")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout_cmd(i: discord.Interaction, korisnik: discord.Member, minuta: int = 10, razlog: str = "Bez razloga"):
    if not 1 <= minuta <= 1440:
        return await i.response.send_message(embed=em("❌ Greška", "Između 1 i 1440 minuta!", color=COLORS["error"]), ephemeral=True)
    await korisnik.timeout(discord.utils.utcnow() + timedelta(minutes=minuta), reason=razlog)
    await i.response.send_message(embed=em("⏱️ Ućutkan", color=COLORS["warning"], thumb=korisnik.display_avatar.url, fields=[
        ("👤 Korisnik", korisnik.mention, True), ("⏳ Trajanje", f"`{minuta}` min", True),
        ("📝 Razlog", razlog, False), ("🛡️ Moderator", i.user.mention, True),
    ]))

@bot.tree.command(name="warn", description="⚠️ Upozori korisnika")
@app_commands.checks.has_permissions(manage_messages=True)
async def warn(i: discord.Interaction, korisnik: discord.Member, razlog: str = "Kršenje pravila"):
    warns = get_warnings(i.guild.id, korisnik.id)
    warns.append({"razlog": razlog, "moderator": str(i.user), "vreme": datetime.now(timezone.utc).strftime("%d.%m.%Y. %H:%M")})
    save_data()
    await i.response.send_message(embed=em("⚠️ Upozorenje", color=COLORS["warning"], thumb=korisnik.display_avatar.url, fields=[
        ("👤 Korisnik", korisnik.mention, True), ("📊 Ukupno", f"`{len(warns)}`", True),
        ("📝 Razlog", razlog, False), ("🛡️ Moderator", i.user.mention, True),
    ]))

@bot.tree.command(name="warnings", description="📋 Upozorenja korisnika")
@app_commands.checks.has_permissions(manage_messages=True)
async def warnings_cmd(i: discord.Interaction, korisnik: discord.Member):
    warns = get_warnings(i.guild.id, korisnik.id)
    if not warns:
        return await i.response.send_message(embed=em(f"📋 {korisnik.display_name}", "Nema upozorenja! ✅", color=COLORS["success"]), ephemeral=True)
    desc = "\n".join([f"`{n+1}.` **{w['razlog']}** — {w['vreme']}" for n, w in enumerate(warns)])
    await i.response.send_message(embed=em(f"📋 {korisnik.display_name} — Upozorenja", desc, color=COLORS["warning"], thumb=korisnik.display_avatar.url), ephemeral=True)

@bot.tree.command(name="clearwarnings", description="🗑️ Obriši upozorenja")
@app_commands.checks.has_permissions(administrator=True)
async def clearwarnings(i: discord.Interaction, korisnik: discord.Member):
    data["warnings"].get(str(i.guild.id), {}).pop(str(korisnik.id), None)
    save_data()
    await i.response.send_message(embed=em("✅ Obrisano", f"Sva upozorenja za {korisnik.mention} su uklonjena.", color=COLORS["success"]), ephemeral=True)

@bot.tree.command(name="clear", description="🧹 Obriši poruke")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(i: discord.Interaction, kolicina: int = 10):
    await i.response.defer(ephemeral=True)
    deleted = await i.channel.purge(limit=max(1, min(kolicina, 100)))
    await i.followup.send(embed=em("🧹 Čišćenje završeno", color=COLORS["success"], fields=[
        ("🗑️ Obrisano", f"`{len(deleted)}` poruka", True), ("📌 Kanal", i.channel.mention, True),
    ]), ephemeral=True)

# ═══════════════════════════════════════════
#    EKONOMIJA & LEVEL
# ═══════════════════════════════════════════
@bot.tree.command(name="baki", description="💰 Provjeri stanje novca")
async def baki(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    d = get_economy(u.id)
    last = time.strftime("%H:%M", time.localtime(d["last_work"])) if d["last_work"] else "Nikad"
    await i.response.send_message(embed=em(f"💰 {u.display_name} — Novčanik", color=COLORS["gold"], thumb=u.display_avatar.url, fields=[
        ("💶 Balans", f"`{d['balance']:,} 💶`", True), ("💼 Poslednji posao", last, True),
    ]))

@bot.tree.command(name="posao", description="💼 Radi i zaradi (svaki sat)")
@app_commands.checks.cooldown(1, 3600, key=lambda i: i.user.id)
async def posao(i: discord.Interaction):
    d = get_economy(i.user.id)
    earn = random.randint(150, 600)
    d["balance"] += earn; d["last_work"] = time.time(); save_data()
    await i.response.send_message(embed=em("💼 Posao završen!", f"*{random.choice(JOBS)}*", color=COLORS["success"], fields=[
        ("💶 Zarada", f"`+{earn} 💶`", True), ("🏦 Balans", f"`{d['balance']:,} 💶`", True), ("⏰ Sledeći", "za 1 sat", True),
    ]))

@bot.tree.command(name="daily", description="🎁 Dnevna nagrada")
@app_commands.checks.cooldown(1, 86400, key=lambda i: i.user.id)
async def daily(i: discord.Interaction):
    d = get_economy(i.user.id)
    reward = random.randint(300, 800)
    d["balance"] += reward; d["last_daily"] = time.time(); save_data()
    await i.response.send_message(embed=em("🎁 Dnevna nagrada!", "Vrati se sutra! 🔄", color=COLORS["gold"], fields=[
        ("💶 Nagrada", f"`+{reward} 💶`", True), ("🏦 Balans", f"`{d['balance']:,} 💶`", True),
    ]))

@bot.tree.command(name="daj", description="🤝 Pošalji pare drugaru")
async def daj(i: discord.Interaction, korisnik: discord.Member, iznos: int):
    if iznos <= 0: return await i.response.send_message(embed=em("❌ Greška", "Iznos mora biti pozitivan!", color=COLORS["error"]), ephemeral=True)
    if korisnik.id == i.user.id: return await i.response.send_message(embed=em("❌ Greška", "Ne možeš sebi slati!", color=COLORS["error"]), ephemeral=True)
    s, r = get_economy(i.user.id), get_economy(korisnik.id)
    if s["balance"] < iznos: return await i.response.send_message(embed=em("❌ Nemaš dovoljno", f"Imaš samo `{s['balance']:,} 💶`!", color=COLORS["error"]), ephemeral=True)
    s["balance"] -= iznos; r["balance"] += iznos; save_data()
    await i.response.send_message(embed=em("🤝 Transakcija uspešna", color=COLORS["success"], fields=[
        ("📤 Od", i.user.mention, True), ("📥 Za", korisnik.mention, True), ("💶 Iznos", f"`{iznos:,} 💶`", True),
    ]))

@bot.tree.command(name="kradi", description="🕵️ Pokušaj ukrasti (rizično!)")
@app_commands.checks.cooldown(1, 7200, key=lambda i: i.user.id)
async def kradi(i: discord.Interaction, korisnik: discord.Member):
    if korisnik.id == i.user.id: return await i.response.send_message(embed=em("❌", "Ne možeš krasti sam sebe!", color=COLORS["error"]), ephemeral=True)
    if korisnik.bot: return await i.response.send_message(embed=em("❌", "Botovi nemaju para!", color=COLORS["error"]), ephemeral=True)
    s, r = get_economy(i.user.id), get_economy(korisnik.id)
    if r["balance"] < 100: return await i.response.send_message(embed=em("❌", "Siromašna žrtva, nema šta ukrasti.", color=COLORS["error"]), ephemeral=True)
    await i.response.defer()
    await asyncio.sleep(2)
    amount = random.randint(50, min(600, r["balance"]))
    if random.random() < 0.38:
        r["balance"] -= amount; s["balance"] += amount
        e = em("🕵️ Krađa uspešna!", "Niko te nije video. Za sad... 👀", color=COLORS["gold"], fields=[
            ("💰 Ukradeno", f"`{amount:,} 💶`", True), ("👤 Žrtva", korisnik.mention, True), ("🏦 Balans", f"`{s['balance']:,} 💶`", True),
        ])
    else:
        fine = random.randint(100, 350)
        s["balance"] = max(0, s["balance"] - fine)
        e = em("🚔 Uhvaćen si!", f"{korisnik.mention} te je prijavio policiji! 🤡", color=COLORS["error"], fields=[
            ("💸 Kazna", f"`{fine:,} 💶`", True), ("🏦 Balans", f"`{s['balance']:,} 💶`", True),
        ])
    save_data(); await i.followup.send(embed=e)

@bot.tree.command(name="rank", description="📈 Level i XP")
async def rank(i: discord.Interaction, korisnik: discord.Member = None):
    u = korisnik or i.user
    d = get_xp(u.id)
    needed = d["level"] * 100
    filled = min(d["xp"] * 10 // needed, 10)
    bar = "🟦" * filled + "⬛" * (10 - filled)
    pct = round(d["xp"] / needed * 100)
    await i.response.send_message(embed=em(f"📈 {u.display_name} — Rank", f"{bar} `{pct}%`", color=COLORS["purple"], thumb=u.display_avatar.url, fields=[
        ("🏆 Level", f"`{d['level']}`", True), ("⭐ XP", f"`{d['xp']}/{needed}`", True), ("📊 Do sledećeg", f"`{pct}%`", True),
    ]))

@bot.tree.command(name="leaderboard", description="🏅 Top lista servera")
@app_commands.choices(tip=[app_commands.Choice(name="XP & Leveli", value="xp"), app_commands.Choice(name="Novac 💶", value="novac")])
async def leaderboard(i: discord.Interaction, tip: str = "xp"):
    await i.response.defer()
    medals = ["🥇", "🥈", "🥉"]
    if tip == "xp":
        srt = sorted(data["xp"].items(), key=lambda x: (x[1]["level"], x[1]["xp"]), reverse=True)[:10]
        lines = []
        for n, (uid, d) in enumerate(srt):
            try: user = await bot.fetch_user(int(uid)); name = user.display_name
            except: name = f"#{uid[:4]}"
            lines.append(f"{medals[n] if n<3 else f'`{n+1}.`'} **{name}** — Level `{d['level']}` • `{d['xp']} XP`")
        e = em("🏅 Top Lista — XP", "\n".join(lines) or "Nema podataka.", color=COLORS["purple"])
    else:
        srt = sorted(data["economy"].items(), key=lambda x: x[1]["balance"], reverse=True)[:10]
        lines = []
        for n, (uid, d) in enumerate(srt):
            try: user = await bot.fetch_user(int(uid)); name = user.display_name
            except: name = f"#{uid[:4]}"
            lines.append(f"{medals[n] if n<3 else f'`{n+1}.`'} **{name}** — `{d['balance']:,} 💶`")
        e = em("🏅 Top Lista — Bogatstvo", "\n".join(lines) or "Nema podataka.", color=COLORS["gold"])
    await i.followup.send(embed=e)

# ═══════════════════════════════════════════
#    IGRE
# ═══════════════════════════════════════════
class KPM(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=30); self.user = user; self.msg = None

    async def on_timeout(self):
        for c in self.children: c.disabled = True
        if self.msg: await self.msg.edit(embed=em("⏱️ Vreme isteklo!", "Igra otkazana.", color=COLORS["error"]), view=self)

    async def play(self, i, choice):
        if i.user != self.user: return await i.response.send_message(embed=em("❌", "Nije tvoja igra!", color=COLORS["error"]), ephemeral=True)
        bot_c = random.choice(["🪨 Kamen", "📄 Papir", "✂️ Makaze"])
        win_map = {("Kamen","Makaze"),("Papir","Kamen"),("Makaze","Papir")}
        cw, bw = choice.split()[1], bot_c.split()[1]
        if choice == bot_c: res, color = "🤝 Nerešeno!", COLORS["warning"]
        elif (cw, bw) in win_map: res, color = "🏆 Pobedio si!", COLORS["success"]
        else: res, color = "💀 Izgubio si!", COLORS["error"]
        for c in self.children: c.disabled = True
        await i.response.edit_message(embed=em(f"🎮 KPM — {res}", color=color, fields=[
            ("👤 Ti", choice, True), ("🤖 Bot", bot_c, True), ("📊 Rezultat", res, False),
        ]), view=self); self.stop()

    @discord.ui.button(label="🪨 Kamen",  style=discord.ButtonStyle.primary)
    async def r(self, i, b): await self.play(i, "🪨 Kamen")
    @discord.ui.button(label="📄 Papir",  style=discord.ButtonStyle.success)
    async def p(self, i, b): await self.play(i, "📄 Papir")
    @discord.ui.button(label="✂️ Makaze", style=discord.ButtonStyle.danger)
    async def s(self, i, b): await self.play(i, "✂️ Makaze")

@bot.tree.command(name="kpm", description="🎮 Kamen-Papir-Makaze")
async def kpm(i: discord.Interaction):
    v = KPM(i.user)
    m = await i.response.send_message(embed=em("🎮 Kamen-Papir-Makaze", f"{i.user.mention}, odaberi potez! ⏱️ 30s", color=COLORS["balkan"]), view=v)
    v.msg = await m.original_response()

@bot.tree.command(name="slots", description="🎰 Slot mašina")
@app_commands.checks.cooldown(1, 15, key=lambda i: i.user.id)
async def slots(i: discord.Interaction):
    await i.response.defer()
    await asyncio.sleep(1)
    symbols = ["🍒","🍋","🍊","🍇","💎","7️⃣","⭐","🔔"]
    reels = [random.choice(symbols) for _ in range(3)]
    d = get_economy(i.user.id)
    if reels[0]==reels[1]==reels[2]:
        reward = 1500 if reels[0] in ("💎","7️⃣") else 600
        res, color = f"🎉 JACKPOT! `+{reward} 💶`", COLORS["gold"]; d["balance"] += reward
    elif reels[0]==reels[1] or reels[1]==reels[2]:
        reward = 80; res, color = f"✨ Dobitak! `+{reward} 💶`", COLORS["success"]; d["balance"] += reward
    else:
        loss = 25; res, color = f"😢 Prazno. `-{loss} 💶`", COLORS["error"]; d["balance"] = max(0, d["balance"]-loss)
    save_data()
    await i.followup.send(embed=em("🎰 Slot Mašina", f"**{' ║ '.join(reels)}**", color=color, fields=[
        ("🎯 Rezultat", res, False), ("🏦 Balans", f"`{d['balance']:,} 💶`", True),
    ]))

@bot.tree.command(name="rulet", description="🔫 Ruski rulet (za hrabre!)")
@app_commands.checks.cooldown(1, 600, key=lambda i: i.user.id)
async def rulet(i: discord.Interaction):
    await i.response.defer(); await asyncio.sleep(2)
    d = get_economy(i.user.id)
    if random.random() < 0.167:
        e = em("💀 PUCANJ!", "Metak je bio u komori... 😵\nBolje sreće sledeći put — ako bude sledeći put.", color=COLORS["error"])
    else:
        reward = random.randint(300, 1000); d["balance"] += reward; save_data()
        e = em("🔫 Preživeo si!", "Klik. Metak nije bio tu. Nisi bogat, ali si živ! 😅", color=COLORS["success"], fields=[
            ("💶 Nagrada", f"`+{reward} 💶`", True), ("🏦 Balans", f"`{d['balance']:,} 💶`", True),
        ])
    await i.followup.send(embed=e)

@bot.tree.command(name="flip", description="🪙 Baci novčić — možeš kladiti")
async def flip(i: discord.Interaction, oklada: int = 0):
    d = get_economy(i.user.id)
    if oklada < 0: return await i.response.send_message(embed=em("❌", "Oklada ne može biti negativna!", color=COLORS["error"]), ephemeral=True)
    if oklada > d["balance"]: return await i.response.send_message(embed=em("❌ Nemaš dovoljno", f"Imaš `{d['balance']:,} 💶`", color=COLORS["error"]), ephemeral=True)
    await i.response.defer(); await asyncio.sleep(1)
    won = random.choice([True, False])
    if oklada > 0:
        if won: d["balance"] += oklada; extra = f"\n💶 Zaradio `+{oklada} 💶`!"
        else: d["balance"] -= oklada; extra = f"\n💸 Izgubio `-{oklada} 💶`!"
        save_data()
    else: extra = ""
    await i.followup.send(embed=em(f"🪙 {'Glava! 👤' if won else 'Pismo! 📜'}",
        f"**{'Glava 👤' if won else 'Pismo 📜'}**{extra}",
        color=COLORS["success"] if won else COLORS["error"],
        fields=[("🏦 Balans", f"`{d['balance']:,} 💶`", True)] if oklada>0 else None
    ))

@bot.tree.command(name="8ball", description="🎱 Postavi pitanje magičnoj kugli")
async def eightball(i: discord.Interaction, pitanje: str):
    await i.response.send_message(embed=em("🎱 Magična Kugla", color=COLORS["purple"], fields=[
        ("❓ Pitanje", pitanje, False), ("💬 Odgovor", random.choice(EIGHTBALL_REPLIES), False),
    ]))

@bot.tree.command(name="meme", description="🤣 Nasumični Balkan meme")
async def meme(i: discord.Interaction):
    await i.response.send_message(embed=em("🤣 Balkan Meme", get_next_meme(i.guild.id), color=COLORS["fun"]))

# ═══════════════════════════════════════════
#    VJEŠALA (Hangman)
# ═══════════════════════════════════════════
class VjesalaModal(discord.ui.Modal, title="Unesi slovo"):
    slovo = discord.ui.TextInput(label="Slovo (jedno)", min_length=1, max_length=1, placeholder="Npr: A")

    def __init__(self, hangman_view):
        super().__init__()
        self.hv = hangman_view

    async def on_submit(self, i: discord.Interaction):
        await self.hv.guess(i, self.slovo.value.upper().strip())

class VjesalaView(discord.ui.View):
    def __init__(self, user: discord.Member, word: str):
        super().__init__(timeout=300)
        self.user    = user
        self.word    = word.upper()
        self.guessed: set = set()
        self.wrong   = 0
        self.max_w   = 6
        self.over    = False

    def display_word(self):
        return " ".join(c if c in self.guessed else "\\_ " for c in self.word)

    def make_embed(self, title=None, color=None):
        wrong_letters = [l for l in sorted(self.guessed) if l not in self.word]
        right_letters = [l for l in sorted(self.guessed) if l in self.word]
        t = title or "🎮 Vješala"
        c = color or COLORS["balkan"]
        e = discord.Embed(title=t, color=c, timestamp=datetime.now(timezone.utc))
        e.add_field(name="🔤 Riječ", value=f"`{self.display_word()}`", inline=False)
        e.add_field(name="💀 Vješalo", value=VJASALA_FAZE[self.wrong], inline=True)
        e.add_field(name="❌ Pogrešna", value=" ".join(wrong_letters) or "—", inline=True)
        e.add_field(name="✅ Tačna", value=" ".join(right_letters) or "—", inline=True)
        e.add_field(name="❤️ Životi", value=f"`{self.max_w - self.wrong}/{self.max_w}`", inline=True)
        e.set_footer(text=f"{BOT_NAME} {VERSION} • Pogodi slovo klikom!")
        return e

    async def guess(self, i: discord.Interaction, letter: str):
        if i.user != self.user:
            return await i.response.send_message(embed=em("❌", "Nije tvoja igra!", color=COLORS["error"]), ephemeral=True)
        if not letter.isalpha():
            return await i.response.send_message(embed=em("❌", "Unesi samo slovo!", color=COLORS["error"]), ephemeral=True)
        if letter in self.guessed:
            return await i.response.send_message(embed=em("⚠️", f"Slovo **{letter}** si već pokušao!", color=COLORS["warning"]), ephemeral=True)
        self.guessed.add(letter)
        if letter not in self.word:
            self.wrong += 1
        won  = all(c in self.guessed for c in self.word)
        lost = self.wrong >= self.max_w
        if won:
            self.over = True; self.children[0].disabled = True
            await i.response.edit_message(embed=self.make_embed(f"🏆 Pobijedio si! Riječ: **{self.word}**", COLORS["success"]), view=self)
            self.stop()
        elif lost:
            self.over = True; self.children[0].disabled = True
            await i.response.edit_message(embed=self.make_embed(f"💀 Izgubio si! Bila je: **{self.word}**", COLORS["error"]), view=self)
            self.stop()
        else:
            await i.response.edit_message(embed=self.make_embed(), view=self)

    async def on_timeout(self):
        if not self.over:
            self.children[0].disabled = True
            try:
                await self.message.edit(embed=self.make_embed(f"⏱️ Vreme isteklo! Bila je: **{self.word}**", COLORS["error"]), view=self)
            except: pass

    @discord.ui.button(label="✏️ Unesi slovo", style=discord.ButtonStyle.primary, emoji="🔤")
    async def enter(self, i: discord.Interaction, b: discord.ui.Button):
        if i.user != self.user:
            return await i.response.send_message(embed=em("❌", "Nije tvoja igra!", color=COLORS["error"]), ephemeral=True)
        await i.response.send_modal(VjesalaModal(self))

    @discord.ui.button(label="🏳️ Predaj se", style=discord.ButtonStyle.danger)
    async def give_up(self, i: discord.Interaction, b: discord.ui.Button):
        if i.user != self.user:
            return await i.response.send_message(embed=em("❌", "Nije tvoja igra!", color=COLORS["error"]), ephemeral=True)
        self.over = True
        for c in self.children: c.disabled = True
        await i.response.edit_message(embed=self.make_embed(f"🏳️ Predao si! Bila je: **{self.word}**", COLORS["warning"]), view=self)
        self.stop()

@bot.tree.command(name="vjasala", description="🎮 Igra Vješala — pogodi skrivenu riječ!")
async def vjasala(i: discord.Interaction):
    word = random.choice(VJASALA_RJECNIK)
    v    = VjesalaView(i.user, word)
    msg  = await i.response.send_message(embed=v.make_embed(), view=v)
    v.message = await msg.original_response()

# ═══════════════════════════════════════════
#    KALADONT
# ═══════════════════════════════════════════
KALADONT_START_WORDS = [
    "BALKON","RAKIJA","KAFANA","FUDBAL","TANJIR","SUNCE","ZIVOT","RIJEKA",
    "PLANINA","DRVO","KAMEN","VATRA","ZEMLJA","VJETAR","OBLAK","JEZERO",
    "MOST","GRAD","SELO","POLJE","BRDO","DOLINA","SPILJA","OCEAN",
    "MAJKA","OTAC","BRAT","SESTRA","BAKA","DJED","PRIJATELJ","KOMŠIJA",
    "GITARA","MUZIKA","PJESMA","PLES","RADIO","POZORIŠTE","BIOSKOP",
    "AUTOMOBIL","AVION","BROD","VAGON","BICIKL","MOTOCIKL","TRAKTOR",
    "JABUKA","KRUŠKA","ŠLJIVA","TREŠNJA","BANANA","NARANDZA","GROŽĐE",
    "CEVAPI","BUREK","SARMA","KAJMAK","PITA","PALAČINKA","KOLAC",
    "ŠKOLA","BOLNICA","CRKVA","DŽAMIJA","STADION","BIBLIOTEKA","MUZEJ",
]

kaladont_games: dict = {}  # channel_id -> {word, used, starter, letters, chain, msg}

def kaladont_embed(game: dict, status: str = "", color=None):
    chain   = game["chain"]
    letters = game["letters"]
    word    = game["word"]
    req     = word[-letters:]
    c       = color or 0x1ABC9C

    # Max 8 prikazanih, starije sakrij
    display = chain[-8:]
    hidden  = len(chain) - len(display)
    icons   = ["🔵", "🟣", "🟤", "🟠", "🟡", "🔵", "🟣", "🟤"]

    rows = []
    if hidden:
        rows.append(f"> *╌╌ {hidden} ranijih rijeci ╌╌*")
        rows.append("> ⬇")

    for idx, (w, who) in enumerate(display):
        is_last  = idx == len(display) - 1
        icon     = "🔴" if is_last else icons[idx % len(icons)]
        word_fmt = f"**{w}**" if is_last else w
        name_fmt = f"*{who}*"
        rows.append(f"> {icon}  {word_fmt}  ·  {name_fmt}")
        if not is_last:
            rows.append(">         ⬇")

    chain_str = "\n".join(rows) if rows else "> *Lanac je prazan...*"

    line = "⎯" * 28
    e = discord.Embed(
        title="🔤  K A L A D O N T",
        description=(
            f"{chain_str}\n"
            f"> {line}\n"
            f"> ➡️  Sledeća počinje sa:  **` {req} `**"
        ),
        color=c,
        timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="📊 Rijeci ukupno", value=f"`{len(chain)}`",  inline=True)
    e.add_field(name="🎯 Zadnja",        value=f"`{word}`",         inline=True)
    e.add_field(name="🔢 Težina",        value=f"`{letters}` slova", inline=True)
    if status:
        e.add_field(name="\u200b", value=status, inline=False)
    e.set_footer(text=f"{BOT_NAME} {VERSION}  •  Napiši novu riječ direktno u chat!")
    return e

class KaladontView(discord.ui.View):
    def __init__(self, channel_id: int):
        super().__init__(timeout=None)
        self.channel_id = channel_id

    @discord.ui.button(label="🏁 Završi igru", style=discord.ButtonStyle.danger)
    async def zavrsi(self, i: discord.Interaction, b: discord.ui.Button):
        game = kaladont_games.get(self.channel_id)
        if not game:
            return await i.response.send_message(embed=em("❌", "Nema aktivne igre.", color=COLORS["error"]), ephemeral=True)
        if i.user.id != game["starter"] and not i.user.guild_permissions.manage_messages:
            return await i.response.send_message(embed=em("❌", "Samo pokretač ili mod može završiti igru!", color=COLORS["error"]), ephemeral=True)
        count = len(game["chain"])
        del kaladont_games[self.channel_id]
        b.disabled = True
        e = discord.Embed(
            title="🏁 Kaladont završen!",
            description=f"Igra gotova! Ukupno izgovoreno **{count}** rijeci. 🎉",
            color=COLORS["gold"], timestamp=datetime.now(timezone.utc)
        )
        e.set_footer(text=f"{BOT_NAME} {VERSION}")
        await i.response.edit_message(embed=e, view=self)
        self.stop()

@bot.tree.command(name="kaladont", description="🔤 Pokretanje igre Kaladont — ulančaj riječi!")
@app_commands.describe(slova="Koliko zadnjih slova mora nova rijec početi (1, 2 ili 3)")
@app_commands.choices(slova=[
    app_commands.Choice(name="1 slovo (lakše)", value=1),
    app_commands.Choice(name="2 slova (normalno)", value=2),
    app_commands.Choice(name="3 slova (teže)", value=3),
])
async def kaladont(i: discord.Interaction, slova: int = 2):
    if i.channel.id in kaladont_games:
        return await i.response.send_message(
            embed=em("⚠️ Igra već teče!", "U ovom kanalu je već aktivan Kaladont. Završi prvu!", color=COLORS["warning"]), ephemeral=True)
    start_word = random.choice(KALADONT_START_WORDS)
    game = {
        "word":    start_word,
        "used":    {start_word},
        "starter": i.user.id,
        "letters": slova,
        "chain":   [(start_word, "🤖 Bot")],
        "msg":     None,
    }
    kaladont_games[i.channel.id] = game
    v = KaladontView(i.channel.id)
    await i.response.send_message(
        embed=kaladont_embed(game, f"🎮 {i.user.mention} pokrenuo igru! Napišite novu riječ direktno u chat!"),
        view=v
    )
    resp = await i.original_response()
    game["msg"] = resp

# ═══════════════════════════════════════════
#    TOPLO-HLADNO
# ═══════════════════════════════════════════
toplo_games: dict = {}  # channel_id -> {"secret": int, "guesses": int, "starter": int, "min": int, "max": int}

TEMPERATURE = [
    (0,  0,   "🎯 TAČNO!",       COLORS["gold"]),
    (1,  5,   "🔥 VRELO je!",    0xFF4500),
    (6,  15,  "♨️ Jako toplo!",  COLORS["error"]),
    (16, 30,  "🌡️ Toplo...",     COLORS["warning"]),
    (31, 60,  "😐 Mlako...",     COLORS["info"]),
    (61, 120, "❄️ Hladno!",      0x87CEEB),
    (121,999, "🥶 Ledeno!",      0x4169E1),
]

def get_temperature(diff: int):
    for lo, hi, label, color in TEMPERATURE:
        if lo <= diff <= hi:
            return label, color
    return "🥶 Ledeno!", 0x4169E1

class ToploModal(discord.ui.Modal, title="Toplo-Hladno — Pogodi broj!"):
    broj = discord.ui.TextInput(label="Tvoj broj", min_length=1, max_length=5, placeholder="Unesi broj...")

    def __init__(self, view):
        super().__init__(); self.tv = view

    async def on_submit(self, i: discord.Interaction):
        try:
            guess = int(self.broj.value.strip())
        except ValueError:
            return await i.response.send_message(embed=em("❌", "Unesi cijeli broj!", color=COLORS["error"]), ephemeral=True)
        await self.tv.process_guess(i, guess)

class ToploView(discord.ui.View):
    def __init__(self, channel_id: int, starter: discord.Member, secret: int, max_num: int):
        super().__init__(timeout=None)
        self.channel_id = channel_id
        self.max_num    = max_num
        toplo_games[channel_id] = {"secret": secret, "guesses": 0, "starter": starter.id, "history": []}

    def make_embed(self, result: str = "", color=None, solved=False):
        game = toplo_games.get(self.channel_id, {})
        guesses = game.get("guesses", 0)
        history = game.get("history", [])[-5:]
        c = color or COLORS["info"]
        e = discord.Embed(title="🌡️ Toplo-Hladno", color=c, timestamp=datetime.now(timezone.utc))
        e.add_field(name="🎯 Raspon", value=f"`1 — {self.max_num}`", inline=True)
        e.add_field(name="🔢 Pokušaji", value=f"`{guesses}`", inline=True)
        if result: e.add_field(name="📡 Signal", value=result, inline=False)
        if history and not solved:
            e.add_field(name="📜 Zadnji pokušaji", value="\n".join(history), inline=False)
        e.set_footer(text=f"{BOT_NAME} {VERSION} • Klikni i pogodi broj!")
        return e

    async def process_guess(self, i: discord.Interaction, guess: int):
        game = toplo_games.get(self.channel_id)
        if not game:
            return await i.response.send_message(embed=em("❌", "Igra nije aktivna!", color=COLORS["error"]), ephemeral=True)
        if not 1 <= guess <= self.max_num:
            return await i.response.send_message(
                embed=em("❌ Van raspona!", f"Unesi broj između `1` i `{self.max_num}`!", color=COLORS["error"]), ephemeral=True)
        game["guesses"] += 1
        secret = game["secret"]
        diff   = abs(guess - secret)
        label, color = get_temperature(diff)
        direction = "⬆️ više" if guess < secret else "⬇️ manje" if guess > secret else ""
        hint = f"`{guess}` → {label}" + (f" ({direction})" if direction else "")
        game["history"].append(hint)
        if diff == 0:
            for c in self.children: c.disabled = True
            del toplo_games[self.channel_id]
            e = discord.Embed(
                title=f"🎯 {i.user.mention} pogodio/la!",
                description=f"Tajna je bila **`{secret}`**!\n🏆 Pogođeno za **{game['guesses']}** pokušaja!",
                color=COLORS["gold"], timestamp=datetime.now(timezone.utc)
            )
            e.set_footer(text=f"{BOT_NAME} {VERSION}")
            await i.response.edit_message(embed=e, view=self)
            self.stop()
        else:
            await i.response.edit_message(embed=self.make_embed(hint, color), view=self)

    @discord.ui.button(label="🔢 Pogodi broj", style=discord.ButtonStyle.primary, emoji="🌡️")
    async def guess_btn(self, i: discord.Interaction, b: discord.ui.Button):
        if self.channel_id not in toplo_games:
            return await i.response.send_message(embed=em("❌", "Igra nije aktivna.", color=COLORS["error"]), ephemeral=True)
        await i.response.send_modal(ToploModal(self))

    @discord.ui.button(label="🏁 Završi igru", style=discord.ButtonStyle.danger)
    async def zavrsi(self, i: discord.Interaction, b: discord.ui.Button):
        game = toplo_games.get(self.channel_id)
        if not game:
            return await i.response.send_message(embed=em("❌", "Nema aktivne igre.", color=COLORS["error"]), ephemeral=True)
        if i.user.id != game["starter"] and not i.user.guild_permissions.manage_messages:
            return await i.response.send_message(embed=em("❌", "Samo pokretač ili mod može završiti igru!", color=COLORS["error"]), ephemeral=True)
        secret = game["secret"]
        del toplo_games[self.channel_id]
        for c in self.children: c.disabled = True
        e = discord.Embed(title="🏁 Igra završena!",
            description=f"Tajna je bila **`{secret}`**!\nNiko nije pogodio ovaj put. 😅",
            color=COLORS["warning"], timestamp=datetime.now(timezone.utc))
        e.set_footer(text=f"{BOT_NAME} {VERSION}")
        await i.response.edit_message(embed=e, view=self)
        self.stop()

@bot.tree.command(name="toplo-hladno", description="🌡️ Pogodi tajni broj — Toplo ili Hladno!")
@app_commands.describe(maksimum="Maksimalni broj (default 100, max 1000)")
async def toplo_hladno(i: discord.Interaction, maksimum: int = 100):
    if i.channel.id in toplo_games:
        return await i.response.send_message(
            embed=em("⚠️ Igra već teče!", "U ovom kanalu je već aktivna igra. Završi prvu!", color=COLORS["warning"]), ephemeral=True)
    maksimum = max(10, min(maksimum, 1000))
    secret = random.randint(1, maksimum)
    v = ToploView(i.channel.id, i.user, secret, maksimum)
    await i.response.send_message(
        embed=v.make_embed(f"🎮 {i.user.mention} pokrenuo igru!\nPogodi broj od `1` do `{maksimum}`!", COLORS["info"]),
        view=v
    )

# ═══════════════════════════════════════════
#    LJUBAVNE / SOCIJALNE KOMANDE
# ═══════════════════════════════════════════
async def social_cmd(i: discord.Interaction, target: discord.Member, action: str, txt: str, color_key: str = "love"):
    await i.response.defer()
    gif = await get_gif(action)
    opis = txt.replace("{from}", i.user.mention).replace("{to}", target.mention)
    e = discord.Embed(description=opis, color=COLORS[color_key], timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    if gif: e.set_image(url=gif)
    await i.followup.send(embed=e)

@bot.tree.command(name="zagrljaj", description="🤗 Zagrli nekog na serveru")
async def zagrljaj(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "hug", "🤗 {from} grli {to}! Aww, tako slatko! 💕", "love")

@bot.tree.command(name="poljubac", description="💋 Pošalji poljubac nekome")
async def poljubac(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "kiss", "💋 {from} šalje poljubac {to}! 😘", "pink")

@bot.tree.command(name="mazi", description="🥰 Pomazi nekoga nježno")
async def mazi(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "pat", "🥰 {from} mazi {to} po glavi! Predobro! ✨", "love")

@bot.tree.command(name="tapsi", description="👋 Tapši nekoga prijateljski")
async def tapsi(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "handshake", "👋 {from} tapše {to}! Aj, brate! 🤝", "teal")

@bot.tree.command(name="high5", description="🙌 Daj peticu nekome")
async def high5(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "highfive", "🙌 {from} daje peticu {to}! Dobra ekipa! ⚡", "success")

@bot.tree.command(name="cudan", description="😠 Budi ćudan prema nekome")
async def cudan(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "poke", "😠 {from} je ćudan prema {to}! Ajde, brate... 😤", "warning")

@bot.tree.command(name="pocetkaj", description="🤕 Pocektaj nekoga za fun")
async def pocetkaj(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "slap", "🤕 {from} pocektao {to}! Za malu ljutu... 😵", "error")

@bot.tree.command(name="srce", description="❤️ Pošalji srce nekome")
async def srce(i: discord.Interaction, korisnik: discord.Member):
    poruke = [
        "❤️ {from} šalje srce {to}! Aww! 🥺",
        "💖 {from} voli {to}! Toliko slatko! 💕",
        "🌹 {from} poklanja ruže {to}! Romantično! 🌹",
        "💝 {from} šalje ljubav {to}! Neka traje! 💝",
    ]
    e = discord.Embed(description=random.choice(poruke).replace("{from}", i.user.mention).replace("{to}", korisnik.mention), color=COLORS["love"], timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

@bot.tree.command(name="mazenje", description="🐱 Pomazi nekoga kao mačku")
async def mazenje(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "cuddle", "🐱 {from} mazi {to} kao svoju mačku! Predivno! 🌸", "pink")

@bot.tree.command(name="zbunjen", description="😵 Pokaži zbunjenost prema nekome")
async def zbunjen(i: discord.Interaction, korisnik: discord.Member):
    await social_cmd(i, korisnik, "confused", "😵 {from} je totalno zbunjen zbog {to}! 🌀", "warning")

@bot.tree.command(name="pljes", description="👏 Aplaudiraj nekome")
async def pljes(i: discord.Interaction, korisnik: discord.Member):
    e = discord.Embed(description=f"👏 {i.user.mention} aplaudira {korisnik.mention}! Bravo, majstore! 🎊", color=COLORS["gold"], timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

@bot.tree.command(name="brak", description="💍 Zaprosio nekoga (za fun)")
async def brak(i: discord.Interaction, korisnik: discord.Member):
    if korisnik.id == i.user.id:
        return await i.response.send_message(embed=em("❌", "Ne možeš se zarositi sam sebi!", color=COLORS["error"]), ephemeral=True)
    odgovori = [
        f"💍 {i.user.mention} zaprosio {korisnik.mention}! 😍 Hoćeš li? 🥂",
        f"💒 {i.user.mention} klekne pred {korisnik.mention} i kaže: 'Hoćeš li biti moj/moja?' 💍",
        f"🌹 {i.user.mention} donosi ruže i prsten {korisnik.mention}! Romantika! 😘",
    ]
    e = discord.Embed(description=random.choice(odgovori), color=COLORS["love"], timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{BOT_NAME} {VERSION}")
    await i.response.send_message(embed=e)

# ═══════════════════════════════════════════
#    HELP
# ═══════════════════════════════════════════
@bot.tree.command(name="help", description="📖 Sve dostupne komande")
async def help_cmd(i: discord.Interaction):
    e = discord.Embed(
        title=f"📖 {BOT_NAME} — Sve Komande",
        description=f"Verzija **{VERSION}** | Prefix: `!` | Slash: `/`",
        color=COLORS["balkan"], timestamp=datetime.now(timezone.utc)
    )
    e.add_field(name="ℹ️ Info & Utiliti",  value="`/ping` `/serverinfo` `/userinfo` `/avatar` `/say` `/setname` `/setavatar`", inline=False)
    e.add_field(name="🛡️ Moderacija",      value="`/ban` `/kick` `/timeout` `/warn` `/warnings` `/clearwarnings` `/clear`", inline=False)
    e.add_field(name="💰 Ekonomija",        value="`/baki` `/posao` `/daily` `/daj` `/kradi` `/rank` `/leaderboard`", inline=False)
    e.add_field(name="🎮 Igre",             value="`/kpm` `/slots` `/rulet` `/flip` `/8ball` `/vjasala` `/kaladont` `/toplo-hladno` `/meme`", inline=False)
    e.add_field(name="❤️ Ljubav & Akcije", value="`/zagrljaj` `/poljubac` `/mazi` `/tapsi` `/high5` `/srce` `/mazenje` `/brak` `/pocetkaj` `/cudan` `/pljes` `/zbunjen`", inline=False)
    e.set_footer(text=f"{BOT_NAME} {VERSION} • Napravio za Balkan servere 🇷🇸")
    e.set_thumbnail(url=bot.user.display_avatar.url)
    await i.response.send_message(embed=e)

# ═══════════════════════════════════════════
#    ERROR HANDLING
# ═══════════════════════════════════════════
@bot.tree.error
async def on_app_error(i: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        mins, secs = divmod(int(error.retry_after), 60)
        t = f"{mins}min {secs}s" if mins else f"{secs}s"
        e = em("⏳ Cooldown!", f"Sačekaj još **{t}**.", color=COLORS["warning"])
    elif isinstance(error, app_commands.MissingPermissions):
        e = em("🛡️ Nemaš dozvole!", "Nisi ovlašćen za ovu komandu.", color=COLORS["error"])
    elif isinstance(error, app_commands.BotMissingPermissions):
        e = em("🤖 Bot nema dozvole!", "Daj mi potrebne dozvole.", color=COLORS["error"])
    else:
        e = em("❌ Greška!", f"`{str(error)[:200]}`", color=COLORS["error"])
        print(f"[ERROR] {error}")
    try:
        if i.response.is_done(): await i.followup.send(embed=e, ephemeral=True)
        else: await i.response.send_message(embed=e, ephemeral=True)
    except: pass

# ═══════════════════════════════════════════
#    POKRETANJE
# ═══════════════════════════════════════════
if __name__ == "__main__":
    print(f"\n{BOT_NAME} {VERSION} STARTUJE...\n")
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("POGRESAN TOKEN!")
    except Exception as e:
        print(f"Greška: {e}")
