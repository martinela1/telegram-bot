import os
from threading import Thread
from flask import Flask

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

app_web = Flask(__name__)


@app_web.route("/")
def home():
    return "Bot is alive"


def run():
    app_web.run(host="0.0.0.0", port=3000)


def keep_alive():
    Thread(target=run).start()


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


def calculeaza_numar(data):
    cifre = [int(c) for c in data if c.isdigit()]
    total = sum(cifre)

    while total > 9:
        total = sum(int(c) for c in str(total))

    return total


def cifra_personalitatii(data):
    cifre = [int(c) for c in data if c.isdigit()]
    if not cifre:
        return None
    zi = int("".join(str(c) for c in cifre))
    return calculeaza_numar(str(zi))


def cifra_realizarii(data):
    destin = calculeaza_numar(data)
    cifre = [c for c in data if c.isdigit()]
    if len(cifre) < 2:
        return None
    zi = int("".join(cifre[:2]))
    zi_redusa = calculeaza_numar(str(zi))
    return calculeaza_numar(str(destin + zi_redusa))


DESTIN_DESCRIERI = {
    1: """🌟 Destinul 1

Destinul 1 este drumul liderului, al pionierului și al omului care deschide uși acolo unde alții văd ziduri.

⚠️ Obstacole frecvente:
frica de eșec, lipsa curajului de a începe, dependența de validarea altora, conflicte cu autoritatea, orgoliu rănit, tendința de a controla tot.

✨ Când ești pe drumul corect:
apar oportunități noi, idei originale, dorința de a crea ceva al tău, succes prin inițiativă, oameni care te respectă și independență financiară.

💫 Lecția sufletului:
să conduci fără ego, să fii puternic fără aroganță și să reușești fără să calci peste alții.

🔑 Cheia destinului tău:
nu ai venit să urmezi drumul altora. Ai venit să îl creezi pe al tău.""",
    2: """🌙 Destinul 2

Destinul 2 este drumul diplomatului, al partenerului conștient și al sufletului sensibil care învață puterea blândeții.

⚠️ Obstacole frecvente:
frica de respingere, dependența afectivă, indecizie, lipsa limitelor, sacrificiu excesiv, anxietate, tendința de a pune pe alții pe primul loc.

✨ Când ești pe drumul corect:
apar relații bune, pace interioară, colaborări valoroase, intuiție puternică, susținere din partea oamenilor potriviți și succes prin parteneriate.

💫 Lecția sufletului:
să iubești fără să te pierzi, să ajuți fără să te sacrifici și să fii blând fără să devii slab.""",
    3: """🎨 Destinul 3

Destinul 3 este drumul creatorului, al comunicatorului și al omului care aduce culoare acolo unde alții văd rutină.

⚠️ Obstacole frecvente:
frica de ridicol, lipsa disciplinei, nevoia de validare, superficialitate, risipire de energie, amânare, dramatizare emoțională.

✨ Când ești pe drumul corect:
apar oportunități sociale, succes prin comunicare, oameni care te apreciază, idei creative, vizibilitate și optimism.

💫 Lecția sufletului:
să te exprimi fără frică, să creezi cu disciplină și să folosești talentul ca dar pentru lume.""",
    4: """🏗️ Destinul 4

Destinul 4 este drumul constructorului, al omului de bază și al celui care își construiește viața pas cu pas. Viața te împinge să înveți disciplina, răbdarea și puterea consecvenței.

De multe ori, acest destin vine cu întârzieri, obstacole și multă muncă. Poți simți că reușești mai greu decât alții, dar aceste experiențe nu sunt pedeapsă — sunt antrenament pentru rezistență și maturitate.

⚠️ Obstacole frecvente:
rigiditate, frica de schimbare, pesimism, muncă excesivă, autocritică, încăpățânare, tendința de a duce singur toate greutățile.

✨ Când ești pe drumul corect:
apar stabilitate financiară, respect profesional, construcții durabile, casă sau afacere solidă și rezultate care rezistă în timp.

🌑 Când te abați de la drum:
blocaje repetate, oboseală, frustrări, stagnare și sentimentul că viața este doar muncă și povară.

💫 Lecția sufletului:
să construiești fără să te împietrești, să muncești fără să te pierzi și să fii puternic fără rigiditate.

🔑 Cheia destinului tău:
nu ai venit să visezi fără temelie. Ai venit să transformi ideile în realitate.
""",
    5: """🔥 Destinul 5

Destinul 5 este drumul exploratorului, al omului adaptabil și al celui care transformă schimbarea în oportunitate. Viața te împinge să înveți curajul de a ieși din rutină, flexibilitatea și puterea de a renaște de mai multe ori.

De multe ori, acest destin vine cu schimbări bruște, mutări, despărțiri sau perioade imprevizibile. Poți simți că viața nu stă locului. Aceste experiențe nu sunt pedeapsă — sunt antrenament pentru libertate și maturizare.

⚠️ Obstacole frecvente:
instabilitate, impulsivitate, fuga de responsabilitate, excese, plictiseală rapidă, relații fluctuante, risipire de energie, decizii grăbite.

✨ Când ești pe drumul corect:
apar oportunități neașteptate, bani prin idei și mobilitate, călătorii benefice, contacte valoroase și succes prin comunicare și reinventare.

🌑 Când te abați de la drum:
haos, relații complicate, instabilitate financiară, dependențe, promisiuni nefinalizate și sentimentul că alergi fără direcție.

💫 Lecția sufletului:
să fii liber fără să distrugi, să te schimbi fără să fugi și să trăiești intens fără să te pierzi.

🔑 Cheia destinului tău:
nu ai venit să fii captiv într-o viață mică. Ai venit să transformi schimbarea în putere.
""",
    6: """💖 Destinul 6

Destinul 6 este drumul protectorului, al vindecătorului și al omului care aduce armonie acolo unde există haos. Viața te împinge să înveți responsabilitatea, maturitatea afectivă și puterea iubirii conștiente.

De multe ori, acest destin vine cu lecții legate de familie, relații și sacrificiu. Poți simți că duci multe poveri sau că oferi mai mult decât primești. Aceste experiențe nu sunt pedeapsă — sunt antrenament pentru echilibru și iubire matură.

⚠️ Obstacole frecvente:
dependență afectivă, control prin grijă, sacrificiu excesiv, gelozie, perfecționism, vinovăție, tendința de a salva pe toată lumea, uitarea propriilor nevoi.

✨ Când ești pe drumul corect:
apar relații stabile, casă armonioasă, respect, succes prin oameni și abundență prin ceea ce oferi din suflet.

🌑 Când te abați de la drum:
relații toxice, epuizare, dezamăgiri repetitive, sentimentul că ești folosit, poveri familiale și lipsă de apreciere.

💫 Lecția sufletului:
să iubești fără să te sacrifici, să ajuți fără să controlezi și să oferi fără să te abandonezi.

🔑 Cheia destinului tău:
nu ai venit doar să ai grijă de alții. Ai venit să înveți că și tu meriți iubire și echilibru.
""",
    7: """🔮 Destinul 7

Destinul 7 este drumul înțeleptului, al cercetătorului și al sufletului care evoluează prin introspecție. Viața te împinge să înveți discernământul, răbdarea, credința și puterea unei minți liniștite.

De multe ori, acest destin vine cu perioade de singurătate, retrageri sau momente în care simți că nu ești înțeles. Pot exista etape în care viața te obligă să stai cu tine însuți. Aceste experiențe nu sunt pedeapsă — sunt antrenament pentru profunzime și maturizare interioară.

⚠️ Obstacole frecvente:
izolare, neîncredere, scepticism excesiv, supragândire, răceală emoțională, anxietate, perfecționism mental, tendința de a evita apropierea.

✨ Când ești pe drumul corect:
apar claritate interioară, intuiție puternică, protecție subtilă, cunoaștere profundă și succes prin expertiză și liniște sufletească.

🌑 Când te abați de la drum:
singurătate apăsătoare, blocaje emoționale, neîncredere în viață, relații distante și sentimentul că nimeni nu te înțelege.

💫 Lecția sufletului:
să te retragi fără să te rupi de lume, să gândești fără să te blochezi și să cauți adevărul fără să pierzi conexiunea cu ceilalți.

🔑 Cheia destinului tău:
nu ai venit să fii ca toți ceilalți. Ai venit să vezi mai profund și să luminezi prin cunoaștere.
""",
    8: """💼 Destinul 8

Destinul 8 este drumul autorității, al reușitei materiale și al omului care învață să folosească puterea cu maturitate. Viața te împinge să înveți disciplina, justiția, răbdarea și relația sănătoasă cu banii și influența.

De multe ori, acest destin vine cu pierderi, întârzieri sau nedreptăți. Poți simți că viața te testează mai mult decât pe alții sau că succesul vine mai târziu. Aceste experiențe nu sunt pedeapsă — sunt antrenament pentru caracter și putere reală.

⚠️ Obstacole frecvente:
frica de lipsuri, control excesiv, rigiditate, muncă obsesivă, răceală emoțională, resentimente, tendința de a domina, neîncredere în oameni, atașament exagerat de statut.

✨ Când ești pe drumul corect:
apar stabilitate financiară, respect, poziție socială, afaceri solide și influență pozitivă, construite în timp.

🌑 Când te abați de la drum:
blocaje materiale, conflicte profesionale sau legale, epuizare, relații reci și sentimentul că muncești mult fără satisfacție.

💫 Lecția sufletului:
să faci bani fără să îți pierzi sufletul, să conduci fără să domini și să fii puternic fără să devii dur.

🔑 Cheia destinului tău:
nu ai venit doar să acumulezi. Ai venit să transformi puterea în valoare și respect.
""",
    9: """🌍 Destinul 9

Destinul 9 este drumul înțeleptului luptător, al sufletului generos și al omului care învață să transforme durerea în putere. Viața te împinge să înveți iertarea, maturitatea emoțională și folosirea energiei pentru un scop mai mare.

De multe ori, acest destin vine cu despărțiri, trădări sau perioade intense care te maturizează rapid. Poți simți că duci lupte grele sau că trebuie să fii puternic pentru mulți. Aceste experiențe nu sunt pedeapsă — sunt antrenament pentru o inimă mare și forță interioară.

⚠️ Obstacole frecvente:
furie acumulată, impulsivitate, tendința de a salva pe toată lumea, dramatizare, orgoliu rănit, relații intense dar obositoare, sacrificiu excesiv, dificultate în a renunța la trecut.

✨ Când ești pe drumul corect:
apar respect, misiune clară, oameni pe care îi inspiri, vindecare interioară și succes prin ajutor oferit altora.

🌑 Când te abați de la drum:
conflicte repetate, relații dureroase, epuizare, sentimentul că dai mult și primești puțin și o nemulțumire constantă.

💫 Lecția sufletului:
să lupți fără ură, să iubești fără sacrificiu excesiv și să fii puternic fără să porți războaie inutile.

🔑 Cheia destinului tău:
nu ai venit doar să supraviețuiești. Ai venit să transformi focul tău interior în lumină pentru lume.
""",
}
REALIZARE_DESCRIERI = {
    1: """🌟 Realizarea ta vine prin leadership, inițiativă și curajul de a-ți crea propriul drum.

Succesul apare atunci când ieși în față, iei decizii și nu mai depinzi de validarea altora. Ai nevoie de libertate, autonomie și control asupra direcției tale.

💰 Banii vin când începi ceva al tău și îți pui amprenta personală pe ceea ce faci.

🔹 Ți se potrivesc:
antreprenoriat, management, vânzări, marketing, consultanță, coaching, leadership, proiecte independente, brand personal.

🔹 Lucrezi cel mai bine:
singur sau în roluri unde ai putere de decizie și libertate mare.

⚠️ Te pot bloca:
orgoliul, graba, impulsivitatea, conflictele cu autoritatea și dorința de rezultate rapide.

🗝️ Cheia realizării tale:
construiește ceva al tău, învață să delegi și dezvoltă răbdarea.

❗️Autocunoașterea este esențială pentru tine.  
Când știi cine ești, devii lider autentic și atragi succesul natural.

✨ Când ești pe drumul corect:
apar oportunități, respect, vizibilitate și independență financiară.

❌ Când te abați:
frustrare, conflicte, stagnare și senzația că muncești pentru visul altuia.

🌱 Când ai control sănătos asupra direcției tale, începi să înflorești.""",
    2: """🌙 Realizarea ta vine prin colaborare, diplomație și relații armonioase.

Succesul apare atunci când unești oameni, creezi echilibru și transformi tensiunea în cooperare. Nu ești făcut să lupți singur, ci să construiești împreună.

💰 Banii vin prin parteneriate sănătoase, relații corecte și domenii unde contează tactul, sensibilitatea și comunicarea fină.

🔹 Ți se potrivesc:
psihologie, terapie, consiliere, HR, relații publice, beauty, design, educație, customer care, organizare evenimente, lucru cu clienții.

🔹 Lucrezi cel mai bine:
în echipă, în parteneriat sau într-un mediu calm și respectuos.

✨ Strălucești mai mult când ai oamenii potriviți lângă tine.

⚠️ Te pot bloca:
frica de conflict, indecizia, lipsa limitelor, dorința de a mulțumi pe toată lumea și dependența de aprobarea altora.

🗝️ Cheia realizării tale:
alege colaboratori sănătoși, pune limite clare și învață să îți ceri valoarea.

❗️Autocunoașterea este esențială pentru tine.  
Dacă nu știi ce meriți, riști să muncești pentru succesul altora, nu pentru al tău.

✨ Când ești pe drumul corect:
apar parteneriate bune, clienți fideli, liniște interioară și bani constanți.

❌ Când te abați:
relații toxice, epuizare emoțională, frustrări și sentimentul că dai mult și primești puțin.

🌱 Când înveți să te prețuiești, și lumea începe să te prețuiască.""",
    3: """🎤 Realizarea ta vine prin creativitate, comunicare și vizibilitate.

Succesul apare când te exprimi liber, inspiri și aduci energie în ceea ce faci. Nu ești făcut pentru rutină rigidă, ci pentru idei și impact.

💰 Banii vin din comunicare, imagine, creativitate și capacitatea ta de a atrage oameni.

🔹 Ți se potrivesc:
marketing, social media, PR, jurnalism, actorie, scris, content creation, vânzări, beauty, domenii creative.

🔹 Lucrezi cel mai bine:
în medii dinamice, cu libertate de exprimare și contact cu oamenii.

✨ Strălucești când ai public și vizibilitate.

⚠️ Te pot bloca:
lipsa disciplinei, risipirea energiei, amânarea, cheltuieli impulsive și nevoia de validare.

🗝️ Cheia realizării tale:
creează constant, dezvoltă un brand personal și transformă inspirația în sistem.

❗️Autocunoașterea te ajută să diferențiezi talentul real de distragere.

✨ Când ești pe drumul corect:
apar oportunități, popularitate, bani prin imagine și colaborări.

❌ Când te abați:
proiecte neterminate, stagnare și senzația că ai potențial nefolosit.

🌱 Când îți iei talentul în serios, viața te răsplătește.""",
    4: """⚡ Realizarea ta vine prin originalitate, inovație și curajul de a ieși din tipare.

Succesul apare când gândești diferit și transformi ideile neobișnuite în ceva concret.

💰 Banii vin din idei moderne, tehnologie, creativitate aplicată și proiecte neconvenționale.

🔹 Ți se potrivesc:
design, media, tehnologie, marketing digital, antreprenoriat, online business, proiecte inovatoare.

🔹 Lucrezi cel mai bine:
independent sau în medii flexibile unde ai libertate de creație.

✨ Strălucești când inovezi.

⚠️ Te pot bloca:
haosul, impulsivitatea, lipsa consecvenței și schimbările fără plan.

🗝️ Cheia realizării tale:
organizează-ți creativitatea și construiește sisteme în jurul ideilor tale.

❗️Autocunoașterea te ajută să nu confunzi rebeliunea cu direcția.

✨ Când ești pe drumul corect:
apar oportunități neașteptate, bani din idei originale și salturi rapide.

❌ Când te abați:
instabilitate, proiecte abandonate și lipsă de direcție.

🌱 Când îți organizezi diferența, începi să prosperi.""",
    5: """🌍 Realizarea ta vine prin mișcare, adaptare și conexiuni.

Succesul apare când ești în acțiune, comunici și profiți de oportunități.

💰 Banii vin din viteză, networking, vânzări și capacitatea ta de a te adapta rapid.

🔹 Ți se potrivesc:
marketing, comerț, online business, turism, PR, freelancing, negocieri, social media.

🔹 Lucrezi cel mai bine:
în sisteme flexibile, pe proiecte sau în medii dinamice.

✨ Strălucești când ești în mișcare.

⚠️ Te pot bloca:
impulsivitatea, lipsa constanței, risipirea energiei și schimbările fără strategie.

🗝️ Cheia realizării tale:
pune direcție peste libertate și diversifică sursele de venit.

❗️Autocunoașterea te ajută să nu confunzi agitația cu progresul.

✨ Când ești pe drumul corect:
apar bani din contacte, oportunități rapide și creștere accelerată.

❌ Când te abați:
haos, instabilitate și senzația că muncești fără direcție.

🌱 Când îți organizezi energia, începi să câștigi.""",
    6: """💎 Realizarea ta vine prin oameni, armonie și valoare emoțională.

Succesul apare când creezi încredere, frumusețe și relații stabile.

💰 Banii vin din servicii oferite cu suflet, imagine și relații de calitate.

🔹 Ți se potrivesc:
beauty, design, psihologie, educație, evenimente, gastronomie, imobiliare, PR.

🔹 Lucrezi cel mai bine:
cu oameni, în echipe sau în medii unde relațiile contează.

✨ Strălucești când creezi loialitate.

⚠️ Te pot bloca:
sacrificiul excesiv, lipsa limitelor și munca neplătită corect.

🗝️ Cheia realizării tale:
cere valoarea ta, pune limite și construiește relații pe termen lung.

❗️Autocunoașterea te ajută să nu confunzi grija cu autosacrificiul.

✨ Când ești pe drumul corect:
apar clienți fideli, bani constanți și stabilitate.

❌ Când te abați:
epuizare, frustrări și dezechilibru emoțional.

🌱 Când te prețuiești, începi să prosperi.""",
    7: """🧠 Realizarea ta vine prin cunoaștere, profunzime și expertiză.

Succesul apare când devii foarte bun într-un domeniu și transformi informația în valoare. Nu ești făcut pentru superficialitate, ci pentru claritate și precizie.

💰 Banii vin din analiză, intuiție și competență.

🔹 Ți se potrivesc:
psihologie, IT, analiză date, medicină, consultanță, educație, strategie, scris, terapii alternative, astrologie, audit.

🔹 Lucrezi cel mai bine:
singur, în liniște, pe proiecte de concentrare.

✨ Strălucești ca specialist.

⚠️ Te pot bloca:
perfecționismul, amânarea, izolarea, lipsa promovării și frica de expunere.

🗝️ Cheia realizării tale:
monetizează cunoașterea și construiește reputație de expert.

❗️Autocunoașterea te ajută să nu te ascunzi de lume.

✨ Când ești pe drumul corect:
apar bani prin expertiză, respect și clienți de calitate.

❌ Când te abați:
lipsă de vizibilitate, bani puțini și proiecte blocate.

🌱 Când îți valorifici mintea, începi să prosperi.""",
    8: """👑 Realizarea ta vine prin putere, disciplină și construcție pe termen lung.

Succesul apare când gândești strategic și creezi ceva solid în timp. Nu ești făcut pentru rezultate rapide fără bază, ci pentru creștere reală și durabilă.

💰 Banii vin din responsabilitate, management și decizii mature.

🔹 Ți se potrivesc:
business, antreprenoriat, finanțe, investiții, imobiliare, management, drept, logistică, leadership.

🔹 Lucrezi cel mai bine:
în poziții de conducere sau în locuri unde poți urca treptat spre vârf.

✨ Strălucești când conduci și organizezi.

⚠️ Te pot bloca:
controlul excesiv, rigiditatea, munca obsesivă, lipsa flexibilității și dezechilibrul între bani și viață.

🗝️ Cheia realizării tale:
gândește pe termen lung, construiește stabil și dezvoltă leadership matur.

❗️Autocunoașterea te ajută să nu confunzi puterea cu controlul.

✨ Când ești pe drumul corect:
apar bani mari în timp, respect, influență și stabilitate materială.

❌ Când te abați:
pierderi, epuizare, conflicte de putere și relații reci.

🌱 Când conduci cu înțelepciune, începi să prosperi.""",
    9: """🔥 Realizarea ta vine prin impact, curaj și influență asupra oamenilor.

Succesul apare când ceea ce faci ajunge la alții și îi inspiră. Nu ești făcut pentru o viață mică, ci pentru a crea schimbare și sens.

💰 Banii vin când îmbini pasiunea cu o misiune reală și oferi valoare oamenilor.

🔹 Ți se potrivesc:
coaching, educație, medicină, psihologie, leadership, antreprenoriat, artă, activism, ONG, politică.

🔹 Lucrezi cel mai bine:
independent sau în roluri unde inspiri, motivezi și conduci.

✨ Strălucești când ai un scop mare.

⚠️ Te pot bloca:
sacrificiul excesiv, impulsivitatea, conflictele, lipsa limitelor și tendința de a da prea mult fără echilibru.

🗝️ Cheia realizării tale:
alege proiecte cu sens, cere valoarea ta și direcționează energia spre construcție.

❗️Autocunoașterea te ajută să nu lupți din rană, ci din claritate.

✨ Când ești pe drumul corect:
apar oameni care te urmează, bani cu sens, influență pozitivă și împlinire.

❌ Când te abați:
epuizare, conflicte, lipsă de direcție și rezultate instabile.

🌱 Când îți folosești energia pentru un scop mai mare, începi să prosperi.""",
}
PERSONALITATE_DESCRIERI = {
    1: """🌙 Cifra Personalității 1

Tu porți vibrația inițiatorului.
Planeta: Soarele | Zi norocoasă: duminică

ENERGIE;
Directă, puternică și impunătoare. Ești perceput ca independent, hotărât și greu de influențat.

PUNCTE FORTE
Leadership, curaj, inițiativă, voință puternică, decizie rapidă, încredere, originalitate și capacitatea de a porni proiecte.

UMBRA
Orgoliu, încăpățânare, control, impulsivitate, nerăbdare, tendința de a domina și dificultatea de a asculta.

PROFESII
Antreprenor, lider, manager, vânzări, marketing, coach, avocat, politică, sport, brand personal.

RELAȚII
Ai nevoie de respect și admirație sinceră. Nu suporți controlul sau lipsa de loialitate.

CHEIA TA
Nu ești făcut să urmezi, ci să creezi propriul drum.

PIETRE NOROCOASE
Ametist, lapis lazuli, rubin""",
    2: """🌙 Cifra Personalității 2

Tu porți vibrația diplomatului și a celui care unește.
Planeta: Luna | Zi norocoasă: luni (vineri)

ENERGIE
Fină, receptivă și intuitivă. Ești perceput ca blând, empatic și ușor de apropiat. Simți mult, chiar și în tăcere.

PUNCTE FORTE
Intuiție puternică, empatie, diplomație, răbdare, loialitate, inteligență emoțională, capacitatea de a uni oameni și talent de mediator.

UMBRA
Hipersensibilitate, indecizie, frică de conflict, dependență emoțională, tendința de a te pune pe locul doi și lipsa limitelor clare.

PROFESII
Psiholog, terapeut, consilier, HR, profesor, designer, beauty, artă, PR, customer care, organizare evenimente.

RELAȚII
Ai nevoie de afecțiune, siguranță și atenție sinceră. Nu suporți răceala, respingerea sau lipsa de interes.

CHEIA TA
Nu te-ai născut să trăiești în umbra altora, ci să înțelegi că sensibilitatea ta este o putere.

PIETRE NOROCOASE
Perla, piatra lunii, opal, acvamarin""",
    3: """🌙 Cifra Personalității 3

Tu porți vibrația creatorului și a comunicatorului.
Planeta: Jupiter | Zi norocoasă: joi (duminică)

ENERGIE
Expansivă, caldă și jucăușă. Ești perceput ca sociabil, luminos și ușor de remarcat. Transmiți energie vie chiar și în tăcere.

PUNCTE FORTE
Creativitate, carismă, talent verbal, inteligență socială, simț artistic, inspirație, adaptabilitate și capacitatea de a motiva oamenii.

UMBRA
Risipire, superficialitate, lipsă de focus, promisiuni nefinalizate, dramatizare și nevoia excesivă de atenție.

PROFESII
Marketing, media, televiziune, radio, actorie, jurnalism, social media, scris, PR, vânzări, organizare evenimente.

RELAȚII
Ai nevoie de conversație, admirație și energie pozitivă. Nu suporți rutina sau oamenii care te limitează.

CHEIA TA
Nu te-ai născut să trăiești mic, ci să luminezi și să inspiri prin talentul tău.

PIETRE NOROCOASE
Ametist, citrin, topaz galben, safir galben""",
    4: """🌙 Cifra Personalității 4

Tu porți vibrația constructorului și a omului de bază.
Planeta: Rahu (Uranus) | Zi norocoasă: sâmbătă (duminică)

ENERGIE
Serioasă, stabilă și practică. Ești perceput ca responsabil, muncitor și de încredere. Transmiți forță și control.

PUNCTE FORTE
Disciplină, perseverență, organizare, loialitate, rezistență, realism și capacitatea de a construi lucruri durabile.

UMBRA
Rigiditate, încăpățânare, control excesiv, frică de schimbare, pesimism și tendința de a duce totul singur.

PROFESII
Inginerie, construcții, imobiliare, contabilitate, administrație, logistică, arhitectură, finanțe, IT tehnic.

RELAȚII
Ai nevoie de stabilitate și loialitate. Nu suporți nesiguranța sau lipsa de seriozitate.

CHEIA TA
Nu te-ai născut doar să muncești, ci să construiești ceva care rămâne.

PIETRE NOROCOASE
Onix, hematit, cuarț fumuriu, granat""",
    5: """🌙 Cifra Personalității 5

Tu porți vibrația libertății și a schimbării.
Planeta: Mercur | Zi norocoasă: miercuri (vineri)

ENERGIE
Rapidă, magnetică și adaptabilă. Ești perceput ca interesant, sociabil și imprevizibil. Transmiți energie de mișcare și curiozitate.

PUNCTE FORTE
Inteligență rapidă, adaptabilitate, farmec personal, comunicare, spirit comercial, flexibilitate și capacitatea de a găsi soluții repede.

UMBRA
Instabilitate, impulsivitate, superficialitate, lipsă de focus, promisiuni nefinalizate și tendința de a evita responsabilitățile.

PROFESII
Vânzări, marketing, publicitate, social media, jurnalism, turism, transport, relații publice, antreprenoriat, negocieri.

RELAȚII
Ai nevoie de libertate, joacă și conexiune mentală. Nu suporți rutina sau controlul.

CHEIA TA
Nu te-ai născut să fii limitat, ci să transformi libertatea în succes.

PIETRE NOROCOASE
Smarald, agat verde, citrin, acvamarin""",
    6: """🌙 Cifra Personalității 6

Tu porți vibrația iubirii, frumuseții și responsabilității.
Planeta: Venus | Zi norocoasă: vineri (luni)

ENERGIE
Calmă, caldă și atractivă. Ești perceput ca grijuliu, elegant și ușor de iubit. Transmiți confort și siguranță.

PUNCTE FORTE
Farmec personal, empatie, responsabilitate, loialitate, simț estetic, organizare, generozitate și capacitatea de a crea armonie.

UMBRA
Sacrificiu excesiv, control prin grijă, gelozie, perfecționism, posesivitate, dependență emoțională și dificultatea de a pune limite.

PROFESII
Beauty, design, modă, cosmetologie, psihologie, terapie, educație, organizare evenimente, HR, gastronomie, hotelerie, artă.

RELAȚII
Ai nevoie de iubire, loialitate și siguranță. Nu suporți răceala, lipsa de respect sau relațiile dezechilibrate.

CHEIA TA
Nu te-ai născut doar să ai grijă de alții, ci să înveți că și tu meriți iubire.

PIETRE NOROCOASE
Cuarț roz, smarald, jad, opal""",
    7: """🌙 Cifra Personalității 7

Tu porți vibrația înțeleptului și a căutătorului de adevăr.
Planeta: Ketu | Zi norocoasă: luni (joi)

ENERGIE
Profundă, misterioasă și intuitivă. Ești perceput ca diferit, greu de citit și foarte inteligent. Transmiți liniște și profunzime.

PUNCTE FORTE
Intuiție puternică, analiză, discernământ, profunzime, independență mentală, observație fină și capacitate de autocunoaștere.

UMBRA
Izolare, răceală emoțională, neîncredere, supragândire, scepticism excesiv și dificultatea de a te deschide emoțional.

PROFESII
Psihologie, cercetare, IT, analiză date, medicină, terapii alternative, spiritualitate, astrologie, scris, consultanță.

RELAȚII
Ai nevoie de spațiu personal și conexiune autentică. Nu suporți superficialitatea sau invazia emoțională.

CHEIA TA
Nu te-ai născut să fii ca ceilalți, ci să descoperi adevăruri profunde.

PIETRE NOROCOASE
Ametist, labradorit, ochi de pisică, piatra lunii""",
    8: """🌙 Cifra Personalității 8

Tu porți vibrația puterii, succesului și responsabilității.
Planeta: Saturn | Zi norocoasă: sâmbătă (vineri)

ENERGIE
Puternică, serioasă și magnetică. Ești perceput ca autoritar, ambițios și greu de ignorat. Transmiți forță și control.

PUNCTE FORTE
Ambiție, disciplină, rezistență, leadership, gândire strategică, perseverență și capacitatea de a gestiona bani și responsabilități.

UMBRA
Control excesiv, rigiditate, răceală emoțională, muncă obsesivă, pesimism și dificultatea de a arăta vulnerabilitate.

PROFESII
Business, antreprenoriat, management, finanțe, imobiliare, drept, politică, administrație, investiții, conducere.

RELAȚII
Ai nevoie de respect și loialitate. Nu suporți lipsa de maturitate sau jocurile emoționale.

CHEIA TA
Nu te-ai născut doar să faci bani, ci să folosești puterea corect și conștient.

PIETRE NOROCOASE
Onix, safir albastru, hematit, obsidian""",
    9: """Cifra Personalității 9

Tu porți vibrația curajului, protecției și a sufletului luptător.
Planeta: Marte | Zi norocoasă: marți (duminică)

ENERGIE
Intensă, pasională și protectoare. Ești perceput ca puternic, direct și curajos. Transmiți forță și determinare.

PUNCTE FORTE
Curaj, generozitate, energie mare, spirit protector, leadership, determinare și capacitatea de a inspira și ridica pe alții.

UMBRA
Impulsivitate, furie, conflictualitate, dramatizare, sacrificiu excesiv și tendința de a intra în lupte inutile.

PROFESII
Antreprenoriat, sport, poliție, armată, medicină, coaching, vânzări, management, activism, domenii unde contează acțiunea.

RELAȚII
Ai nevoie de pasiune, loialitate și respect. Nu suporți răceala sau lipsa de implicare.

CHEIA TA
Nu te-ai născut să porți războaie inutile, ci să transformi forța ta în lumină.

PIETRE NOROCOASE
Rubin, granat, jasp roșu, coral roșu""",
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔢 Cifra Destinului", callback_data="destin")],
        [
            InlineKeyboardButton(
                "🌙 Cifra Personalității", callback_data="personalitate"
            )
        ],
        [InlineKeyboardButton("⭐ Cifra Realizării", callback_data="realizare")],
    ]

    await update.message.reply_text(
        "Bine ai venit ✨\n\nAlege ce vrei să calculezi:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def send_full_text(query, descriere):
    cta = """

🗝️❗️Vrei să afli exact în ce an se activează banii tăi și când vine saltul financiar? În canalul meu privat Telegram primești zilnic Tarot, numerologie și ghidare practică. Intră în comunitatea mea privată.

🔮❗️ Ai o întrebare care nu-ți dă pace?
Tarot Express este pentru momentele în care vrei un răspuns rapid, clar și personalizat la 2 întrebări importante.
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "🌙 Intră în comunitatea privată",
                url="https://t.me/tanya_astrovedic_bot",
            )
        ],
        [
            InlineKeyboardButton(
                "🔮 Tarot Express",
                callback_data="tarot_express",
            )
        ],
    ]
    print("🔥 FINAL BUTTON BLOCK RUNNING")

    await query.message.reply_text(
        descriere + cta, reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    print("CLICK:", query.data)

    if query.data == "destin":
        context.chat_data["mod"] = "destin"
        await query.message.reply_text(
            "Introdu data completă de naștere. Exemplu: 14.08.2000"
        )

    elif query.data == "personalitate":
        context.chat_data["mod"] = "personalitate"
        await query.message.reply_text("Introdu doar ziua nașterii. Exemplu: 16")

    elif query.data == "realizare":
        context.chat_data["mod"] = "realizare"
        print("MODE SET TO:", context.chat_data.get("mod"))

        await query.message.reply_text(
            "Introdu data completă de naștere. Exemplu: 14.08.2000"
        )

    elif query.data.startswith("destin_full_"):
        numar = int(query.data.split("_")[-1])
        descriere = DESTIN_DESCRIERI.get(
            numar, "Interpretarea completă va fi adăugată curând."
        )
        await send_full_text(query, descriere)

    elif query.data.startswith("realizare_full_"):
        numar = int(query.data.split("_")[-1])
        descriere = REALIZARE_DESCRIERI.get(
            numar, "Interpretarea completă va fi adăugată curând."
        )
        await send_full_text(query, descriere)

    elif query.data.startswith("personalitate_full_"):
        numar = int(query.data.split("_")[-1])
        descriere = PERSONALITATE_DESCRIERI.get(
            numar, "Interpretarea completă va fi adăugată curând."
        )
        await send_full_text(query, descriere)

    elif query.data == "tarot_express":
        keyboard = [
            [
                InlineKeyboardButton(
                    "💬 Scrie pe WhatsApp",
                    url="https://wa.me/37378175360?text=Salut,%20vreau%20Tarot%20Express",
                )
            ]
        ]

        with open("attached_assets/tarot_express.png_1777884187659.png", "rb") as photo:
            await query.message.reply_photo(
                photo=photo,
                caption="🔮 Tarot Express",
                reply_markup=InlineKeyboardMarkup(keyboard),
            )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    mod = context.chat_data.get("mod")
    print("MODE READ:", mod)
    if mod == "destin":
        numar = calculeaza_numar(text)

        intro = f"""🔢 Cifra Destinului tău este: {numar}

Ce înseamnă cifra destinului?

Cifra destinului arată drumul principal al vieții tale, lecțiile pe care sufletul tău vine să le învețe și direcția în care ești chemat să evoluezi.

Nu se activează complet din copilărie. Devine tot mai puternică odată cu maturizarea, mai ales după 28–35 de ani.

Fiecare cifră are lumină și umbră:
✨ lumina = potențialul tău real
🌑 umbra = lecțiile pe care trebuie să le depășești
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "👇 Descoperă ce înseamnă pentru tine",
                    callback_data="destin_full_" + str(numar),
                )
            ]
        ]

        await update.message.reply_text(
            intro, reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    elif mod == "realizare":
        numar = cifra_realizarii(text)

        if numar is None:
            await update.message.reply_text(
                "Te rog introdu data completă. Exemplu: 14.08.2000"
            )
            return

        intro = f"""🌟 Cifra Realizării tale este: {numar}

Ce înseamnă cifra realizării?

Cifra realizării arată cum vine succesul la tine, prin ce tip de muncă faci bani mai ușor și ce stil profesional ți se potrivește.

Ea vorbește despre carieră, statut, independență financiară și modul în care îți construiești prosperitatea.

✨ Este energia prin care îți transformi potențialul în rezultate concrete.
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "👇 Descoperă ce înseamnă pentru tine",
                    callback_data="realizare_full_" + str(numar),
                )
            ]
        ]

        await update.message.reply_text(
            intro, reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    elif mod == "personalitate":
        numar = cifra_personalitatii(text)

        intro = f"""🌙 Cifra Personalității tale este: {numar}

Ce înseamnă cifra personalității?

Cifra personalității se calculează din ziua nașterii tale și arată felul în care te manifești în exterior, cum te văd ceilalți și ce energie transmiți.

✨ Este prima impresie pe care o lași în lume.
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "👇 Descoperă ce înseamnă pentru tine",
                    callback_data="personalitate_full_" + str(numar),
                )
            ]
        ]

        await update.message.reply_text(
            intro, reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return


def main():
    # keep_alive()

    app = (
        ApplicationBuilder()
        .token("8519523498:AAFvZce0LcA2myifu1MTPOM18-jKP6cJSoM")
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Botul rulează...")
    app.run_polling()


if __name__ == "__main__":
    main()
