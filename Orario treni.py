"""
----------------------------------------------------------------------------------
GENERAL INFO
Orario treni: Il bot del vero pendolare!
Versione: 2.0
Telegram: @OrarioTreniBot
Supporto: @MarcoBuster
----------------------------------------------------------------------------------
"""
import botogram
import botogram.objects.base
#Grazie a Pietro Albini (botogram) per l'aiuto in CallBackQuery
class CallbackQuery(botogram.objects.base.BaseObject):
    required = {
        "id": str,
        "from": botogram.User,
        "data": str,
    }
    optional = {
        "inline_message_id": str,
        "message": botogram.Message,
    }

botogram.Update.optional["callback_query"] = CallbackQuery
class InlineQuery(botogram.objects.base.BaseObject):
    required = {
        "id": str,
        "from": botogram.User,
        "query": str,
    }
    optional = {
        "location": botogram.Location,
        "offest": str,
    }
    replace_keys = {
        "from": "sender"
    }
botogram.Update.optional["inline_query"] = InlineQuery
import json
import urllib.request
from datetime import datetime
import datetime
import time
import sqlite3
bot = botogram.create("TOKEN")
bot.about = "Con questo bot potrai tracciare il tuo treno comodamente da Telegram. Per iniziare fai /start"
bot.owner = "@MarcoBuster"
bot.lang = "it"
conn = sqlite3.connect('utenti.db')
c = conn.cursor()
try:
    c.execute('''CREATE TABLE news(user_id INTEGER, iscritto INTEGER''')
except:
    pass
conn.commit()
#Comando /news
#Visualizza i messaggi per l'iscrizione alle news e altre informazioni
#Utilizzo: /news
@bot.command("news")
def news(chat, message, args):
    message.reply("*Orario treni NEWS!*\nIscriviti alle notizie per avere notifiche instantanee su *scioperi*, *avvisi* e molto altro riguardo le ferrovie in Italia!")
    message.reply("*Come iscriversi?*\nIscriversi è molto semplice: basta scrivere /newson. Puoi disiscriverti quando vuoi facendo /newsoff")
#Comando /newson
#Iscrizione alle news
#Utilizzo: /newson
@bot.command("newson")
def newson(chat, message):
    iscritto = True
    c.execute('''SELECT EXISTS(SELECT * FROM news where user_id=?)''',(message.chat.id,))
    if str(c.fetchone()) == "(0,)": #Codice da migliorare
        try:
            c.execute('''INSERT INTO news(user_id, iscritto) VALUES(?, ?)''',(message.chat.id, 1))
            conn.commit()
            message.reply("*Fatto!*\nOra sei iscritto! Per disiscriverti fai /newsoff")
        except:
            message.reply("*Errore*\nQualcosa è andato storto.\nForse stai inviando comandi troppo velocemente?\nContatta lo sviluppatore @MarcoBuster")
    else:
        message.reply("*Errore*\nAttenzione! Sei già registrato alle news! Non dirmi che vuoi ricevere post doppi!")
#Comando /viewnews
#Visualizza la lista delle persone iscritte alle news
#UTilizzo: /viewnews [SOLO AMMINISTRATORI]
@bot.command("viewnews")
def viewnews(chat, message):
    try:
        c.execute('''SELECT * from news''')
        rows = c.fetchall()
        for row in rows:
            chat.send(str(row))
    except:
        pass
    conn.commit()
#Comando /newsoff
#Discrizione alle news
#Utilizzo: /newsoff
@bot.command("newsoff")
def newsoff(chat, message):
    iscritto = False
    c.execute('''SELECT EXISTS(SELECT * FROM news where user_id=?)''',(message.chat.id,))
    if str(c.fetchone()) == "(0,)": #Codice da migliorare
        message.reply("*Errore*\nTi sei già disiscritto o non ti sei mai iscritto! Va bene che mi odi, ma è inutile continuare!\nPer iscriverti fai /newson")
    else:
        try:
            c.execute('''DELETE FROM news where user_id=?''',(message.chat.id,))
            message.reply("*Disiscritto*\nDisiscrizione completata!\nPer iscriverti fai /newson")
        except:
            message.reply("*Errore*\nContatta @MarcoBuster per supporto")
    conn.commit()
#Comando /post
#Posta una news
#Utiizzo: /post <messaggio> [SOLO AMMINISTRATORE]
@bot.command("post")
def post(chat, message, args):
    if str(message.chat.id) == "26170256":
        messaggio_news = str(args)
        message.reply("*Ecco il messaggio che stai per inviare*: "+messaggio_news+"\n_Confermare?_")
        message.reply("*Confermato*")
        c.execute('''SELECT user_id FROM news''')
        utenteid= c.fetchall()
        message.reply("*Lista dei destinatari* :"+str(utenteid))
        for k in range(0,10000):
            try:
                #Codice ovviamente da cambiare in seguito
                message.reply("*Messaggio inviato a: *"+str(utenteid[k]).replace("(","").replace(")","").replace(",",""))
                bot.send(str(utenteid[k]).replace("(","").replace(")","").replace(",",""), str(messaggio_news).replace("'","").replace(",","").replace("[","").replace("]","").replace("ccc","\n"))
                continue
            except Exception as e:
                print(str(e))
                pass
                continue
#Comando: /info
#Visualizza le informazioni sul bot
#Utilizzo: /info
@bot.command("info")
def infocommand(chat, message, args):
    help(chat, message, args)
#Comando: /help
#Visualizza le informazioni sul bot
#Utilizzo: /help
@bot.command("help")
def helpcommand(chat, message, args):
    m1 = ("*Orario treni*\n_Con questo bot potrai cercare un treno, una fermata di un treno, una stazione, un itinerario e averne le informazioni principali._\n")
    m2 = ("*Comando /treno*\nPer cercare un treno dal numero fare questo comando:\n`/treno numero-treno`.\n*Suggerimento*\nRicorda che puoi cercare un treno anche scrivendo in chat il numero di treno, senza necessariamente scrivere `/treno` prima.")
    m3 = ("*Comando /fermata*\nPer cercare le informazioni di un treno rispetto a una stazione (_binario, ritardo, ecc..._) fare:\n`/fermata numero-treno numero-fermata`\n_In numero fermata inserire il numero che trovate facendo_: \n`/fermata numero-treno lista`")
    m4 = ("*Comandi /arrivi e /partenze*\nPer cercare il tabellone arrivi o partenze di una stazione fare:\n`/arrivi nome-stazione` o `/partenze nome-stazione`\n*Suggerimento*\nRicorda che puoi cercare le *partenze* di una stazione semplicemente scrivendo il nome della stazione in chat")
    m5 = ("*Comando /itinerario*\nPer cercare un treno che ferma tra due stazioni, fare:\n`/itinerario stazione1 stazione2`\n*Solo in questo comando*, i nomi delle stazioni vanno inserite con il punto al posto dello spazio.\nPer esempio `MILANO CENTRALE` diventa `MILANO.CENTRALE`")
    m6 = ("*Comando /traccia*\nPer tracciare un treno e essere notificati del cambiamento della stazione (di ultimo rilevamento) o di grave accumulo di ritardo, fare: `/traccia numero-treno minuti-massimi`\nIl campo minuti massimi è facoltativo, se non impostato sarà impostato a 20m")
    m7 = ("*Votaci!*\n[Vota il bot cliccando qui](https://telegram.me/storebot?start=OrarioTreniBot)\n*Grazie per il supporto!*\n[Canale con notizie, aggiornamenti e molto altro sul bot qui](https://telegram.me/OrarioTreni) \n_Aiuto, domande, questioni tecniche:_ @MarcoBuster")
    m = m1+"\n"+m2+"\n"+m3+"\n"+m4+"\n"+m5+"\n"+m6+"\n"+m7
    message.reply(m)
    print("Qualcuno ha utilizzato il comando /help senza problemi")
#Comando: /treno
#Cerca un treno e restituisce le informazioni principali
#Utilizzo: /treno <numero di treno>
@bot.command("treno")
def treno(chat, message, args):
    try:
        id_treno = (args[0])
    except Exception as e:
        message.reply("*Errore*\nNon hai inviato nessun numero di treno.\nScrivi qui direttamente in chat il numero di treno, oppure fai `/treno numero-treno`")
    print ("Qualcuno ha cercato il treno: ",(args[0]))
    content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
    response = urllib.request.urlopen(content)
    id_stazione = (str(response.read()).split("-")[-1][:-3])
    try:
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
    except:
        message.reply("*Errore, non trovato (404)*:\n_That’s an error. That’s all we know:_\n-Il numero di treno inserito non è valido;\n-Non stai utilizzando il comando correttamente. Usa /help per il tutorial del comando")
    content = response.read()
    data = json.loads(content.decode("utf8"))
    orarioPartenza = datetime.datetime.fromtimestamp(data['orarioPartenza'] / 1000).strftime('%H:%M')
    orarioArrivo = datetime.datetime.fromtimestamp(data['orarioArrivo'] / 1000).strftime('%H:%M')
    try:
        oraUltimoRilevamento = datetime.datetime.fromtimestamp(data['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
    except:
        oraUltimoRilevamento = "Il treno non è ancora partito"
    testo=("_Informazioni sul treno _"+"_"+id_treno+"_"+"\n*Stazione di partenza*: "+data['origineZero']+" ("+(orarioPartenza)+")""\n*Stazione di arrivo*: "+data['destinazioneZero']+" ("+(orarioArrivo)+")"+"\n*Ritardo*: "+str(data['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data['stazioneUltimoRilevamento']+" ("+(oraUltimoRilevamento)+")\n*Premi sul tasto in basso per aggiornare le informazioni del treno*")
    #Invia il messaggio utilizzando bot.api.call
    bot.api.call("sendMessage", {"chat_id": chat.id, "text":testo,"parse_mode":"Markdown","reply_markup":'{"inline_keyboard":[[{"text":"Aggiorna le informazioni sul treno","callback_data": "'+str(id_treno)+'"}]]}'})
    #Processando la callback
def process_callback(bot, chains, update):
    message = update.callback_query.message
    chat = message.chat
    callback_q = str(update.callback_query.data)
    if callback_q.find('t') >= 0: #Il bot deve tracciare il treno
        id_treno = str(callback_q).replace("t","") #Semplicemente toglie la "t" al numero di treno in modo da essere utilizzabile
        stop = 1200 #Il tracciamento si spegnerà dopo 1200 secondi
        #Cerca il treno
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        try:
            info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
            response = urllib.request.urlopen(info)
        except:
            message.reply("*Errore, non trovato (404)*:\n_That’s an error. That’s all we know:_\n-Il numero di treno inserito non è valido;\n-Non stai utilizzando il comando correttamente. Usa /info per il tutorial del comando")
            tracciamento = False
            return #Se il treno non esiste, return
        tracciamento = True
        content = response.read()
        data = json.loads(content.decode("utf8"))
        orarioPartenza = datetime.datetime.fromtimestamp(data['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo = datetime.datetime.fromtimestamp(data['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento = datetime.datetime.fromtimestamp(data['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento = "Il treno non è ancora partito"
        ritardo = data['ritardo']
        stazioneUltimoRilevamento = data['stazioneUltimoRilevamento']
        if tracciamento is True and data['destinazioneZero'] == stazioneUltimoRilevamento:
            message.reply("*Errore*\nQuesto treno è già arrivato a destinazione!")
            tracciamento = False
            return
        testo=("_Informazioni sul treno _"+"_"+id_treno+"_"+"\n*Stazione di partenza*: "+data['origineZero']+" ("+(orarioPartenza)+")""\n*Stazione di arrivo*: "+data['destinazioneZero']+" ("+(orarioArrivo)+")"+"\n*Ritardo*: "+str(data['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data['stazioneUltimoRilevamento']+" ("+(oraUltimoRilevamento)+")\n*Sto tracciando il treno*")
        try:
            bot.api.call("editMessageText", {"chat_id": chat.id, "message_id": message.message_id, "text":str(testo),"parse_mode":"Markdown","reply_markup":'{"inline_keyboard":[[{"text":"Aggiorna le informazioni sul treno","callback_data": "'+str(id_treno)+'"}]]}'}) #Qui non c'è il tasto per tracciare il treno altrimenti sarebbe illimitato
        except:
            pass

        while tracciamento is True and stop > 0 and data['destinazioneZero'] != stazioneUltimoRilevamento: #Inizia il loop, quando le informazioni cambieranno sul treno verrà inviato un messaggio
            info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
            response = urllib.request.urlopen(info)
            content = response.read()
            data = json.loads(content.decode("utf8"))
            ritardo2 = data['ritardo']
            stop = stop-1
            stazioneUltimoRilevamento2 = data['stazioneUltimoRilevamento']
            differenzaritardo = ritardo2 - ritardo
            if stazioneUltimoRilevamento != stazioneUltimoRilevamento2: #Se le stazioni sono diverse...
                try:
                    oraUltimoRilevamento2 = datetime.datetime.fromtimestamp(data['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
                except:
                    oraUltimoRilevamento2 = "Il treno non è ancora partito"
                message.reply("*Traccia treno*\n_Il treno "+id_treno+" ha cambiato stazione!_\n*Stazione precedente*: "+stazioneUltimoRilevamento+" ("+oraUltimoRilevamento+")"+"\n*Stazione corrente*: "+stazioneUltimoRilevamento2+" ("+oraUltimoRilevamento2+")"+"\n*Ritardo: *"+str(ritardo2)+"m")
                stazioneUltimoRilevamento = data['stazioneUltimoRilevamento']
                oraUltimoRilevamento = data['oraUltimoRilevamento']
            if differenzaritardo == 10 or differenzaritardo > 10: #Se il treno ha subito un grave ritardo...
                message.reply("*Traccia treno*\n_Il treno "+id_treno+" ha accumulato ritardo!_\n*Ritardo precedente*: "+str(ritardo)+"m\n*Ritardo attuale:* "+str(ritardo2)+"m")
                ritardo = data['ritardo']
            if stop == 1: #Quando il tracciamento è finito...
                message.reply("*Traccia treno*\nFine del tracciamento del treno "+id_treno)
            time.sleep(1)
            continue
            if stop == 0:
                return #RESET
    else: #Il bot deve solo aggiornare il messaggio
        #Aggiornamento delle informazioni...
        id_treno = str(update.callback_query.data)
        callback_id = update.callback_query.id
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data = json.loads(content.decode("utf8"))
        orarioPartenza = datetime.datetime.fromtimestamp(data['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo = datetime.datetime.fromtimestamp(data['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento = datetime.datetime.fromtimestamp(data['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento = "Il treno non è ancora partito"
        testo=("_Informazioni sul treno _"+"_"+id_treno+"_"+"\n*Stazione di partenza*: "+data['origineZero']+" ("+(orarioPartenza)+")""\n*Stazione di arrivo*: "+data['destinazioneZero']+" ("+(orarioArrivo)+")"+"\n*Ritardo*: "+str(data['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data['stazioneUltimoRilevamento']+" ("+(oraUltimoRilevamento)+")\n*Premi sul tasto in basso per aggiornare le informazioni del treno*")
        try:
            #Edita il messaggio senza il tastino "TRACCIA TRENO"
            bot.api.call("editMessageText", {"chat_id": chat.id, "message_id": message.message_id, "text":str(testo),"parse_mode":"Markdown","reply_markup":'{"inline_keyboard":[[{"text":"Aggiorna le informazioni sul treno","callback_data": "'+str(id_treno)+'"}]]}'}) #Qui non c'è il tasto per tracciare il treno altrimenti sarebbe illimitato
        except Exception as e:
            pass
        bot.api.call("answerCallbackQuery", {"callback_query_id": str(callback_id), "text": "Messaggio aggiornato", "show_alert":False}) #Avviso sopra lo schermo
        return
bot.register_update_processor("callback_query", process_callback)
#INLINE MODE
def process_inline(bot, chains, update):
    #Inline mode
    user = update.inline_query.sender
    testo = update.inline_query.query
    if testo != None:
        try:
            int(testo)
        except:
            #Il numero di treno inserito non è un numero, quindi come può essere un numero di treno valido? return immediato...
            bot.api.call("answerInlineQuery", {"inline_query_id":update.inline_query.id, "cache_time":0, "results":'[{"type":"article","id":"2","title":"ERRORE","description":"Attenzione! Il numero di treno inserito non è un numero di treno","input_message_content":{"message_text":"*Errore*\n_Non ho digitato un numero di treno. _\nPer utilizzare questo bot devo scrivere, in qualsiasi chat, `@OrarioTreniBot numero di treno`","parse_mode":"Markdown"}}]'})
            return
        id_treno = str(testo)
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        try:
            info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
            response = urllib.request.urlopen(info)
        except:
            #Il treno non esiste
            bot.api.call("answerInlineQuery", {"inline_query_id":update.inline_query.id, "cache_time":0, "results":'[{"type":"article","id":"2","title":"ERRORE","description":"Attenzione! Numero di treno inesistente!","input_message_content":{"message_text":"*Errore*\n_Il treno non esiste_\nPer utilizzare questo bot devo scrivere, in qualsiasi chat, `@OrarioTreniBot numero di treno`","parse_mode":"Markdown"}}]'})
            return
        content = response.read()
        data = json.loads(content.decode("utf8"))
        orarioPartenza = datetime.datetime.fromtimestamp(data['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo = datetime.datetime.fromtimestamp(data['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento = datetime.datetime.fromtimestamp(data['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento = "Il treno non è ancora partito"
        testo=("_Informazioni sul treno _"+"_"+id_treno+"_"+"\n*Stazione di partenza*: "+data['origineZero']+" ("+(orarioPartenza)+")""\n*Stazione di arrivo*: "+data['destinazioneZero']+" ("+(orarioArrivo)+")"+"\n*Ritardo*: "+str(data['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data['stazioneUltimoRilevamento']+" ("+(oraUltimoRilevamento)+")")
        descrizione = "Cerca il treno "+id_treno
        #Fa uscire le informazioni sul treno
        bot.api.call("answerInlineQuery", {"inline_query_id":update.inline_query.id, "cache_time":0, "switch_pm_text":"Vai al bot per altre funzioni","results":'[{"type":"article","id":"1","title":"Cerca treno","description":"'+str(descrizione)+'","input_message_content":{"message_text":"'+testo+'","parse_mode":"Markdown"}}]'})
    if testo == None:
        print("Testo none")
        bot.api.call("answerInlineQuery", {"inline_query_id":update.inline_query.id, "cache_time":0, "results":'[{"type":"article","id":"2","title":"ERRORE","description":"Attenzione! Non hai scritto nessun numero di treno!","input_message_content":{"message_text":"*Errore*\n_Non ho digitato nessun numero di treno. _\nPer utilizzare questo bot devo scrivere, in qualsiasi chat, `@OrarioTreniBot numero di treno`","parse_mode":"Markdown"}}]'})
bot.register_update_processor("inline_query", process_inline)
#Comando: /fermata
#Visualizza le informazioni di un treno rispetto a una fermata specifica
#Utilizzo: /fermata <numero di treno> <numero di fermata>:lista
@bot.command("fermata")
def fermata(chat, message, args):
    id_treno= (args[0])
    content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
    response = urllib.request.urlopen(content)
    id_stazione = (str(response.read()).split("-")[-1][:-3])
    try:
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
    except:
        message.reply("_Errore_\n*Non ho trovato nulla. Forse perché...*:\n-Il numero di treno inserito non è valido;\n-Il treno non è ancora partito;\n-Non stai utilizzando il comando correttamente. Usa /info per il tutorial del comando")
    content = response.read()
    data = json.loads(content.decode("utf8"))
    staz = (args[1])
    try:
        s= int(args[1])
    except:
        pass
    try:
        sOrarioArrivoP = str(datetime.datetime.fromtimestamp(data['fermate'][s]['arrivo_teorico'] / 1000).strftime('%H:%M'))
    except:
        sOrarioArrivoP = "--"
    try:
        sOrarioArrivoR = str(datetime.datetime.fromtimestamp(data['fermate'][s]['arrivoReale'] / 1000).strftime('%H:%M'))
    except:
        sOrarioArrivoR = "--"
    try:
        sOrarioPartenzaP = str(datetime.datetime.fromtimestamp(data['fermate'][s]['partenza_teorica'] / 1000).strftime('%H:%M'))
    except:
        sOrarioPartenzaP = "--"
    try:
        sOrarioPartenzaR = str(datetime.datetime.fromtimestamp(data['fermate'][s]['partenzaReale'] / 1000).strftime('%H:%M'))
    except:
        sOrarioPartenzaR = "--"
    try:
        ritardoArrivo = str(data['fermate'][s]['ritardoArrivo'])
    except:
        ritardoArrivo = "--"
    try:
        ritardoPartenza = str(data['fermate'][s]['ritardoPartenza'])
    except:
        ritardoPartenza = "--"
    if (staz == "lista"):
        message.reply("*Lista stazioni*\n_Ecco la lista delle fermata, per vedere le informazioni di una fermata in dettaglio fare_\n `/fermata "+id_treno+" numero fermata`\n_Il numero fermata è il numeretto, nella lista seguente, prima del nome della stazione_")
        b=""
        for k in range(0,51):
            try:
                a=str("["+str(k)+"] "+data['fermate'][k]['stazione'])
            except:
                break
            b=b+a
            b+="\n"
        message.reply(b)
    else:
        binario = data['fermate'][s]['binarioProgrammatoArrivoDescrizione']
        if (binario=="None"):
            binario = "Errore di Trenitalia/Trenord."
        else:
            binario = str(binario)
        message.reply("*Informazioni di un treno rispetto a una fermata specifica*:_ "+data['fermate'][s]['stazione']+"_\n*Arrivo programmato: *"+sOrarioArrivoP+"\n*Arrivo reale: *"+sOrarioArrivoR+"\n*Ritardo arrivo: *"+ritardoArrivo+"m\n*Partenza programmata: *"+sOrarioPartenzaP+"\n*Partenza reale: *"+sOrarioPartenzaR+"\n*Ritardo partenza: *"+ritardoPartenza+"m\n*Binario: *"+binario)
#Comando: /statistiche
#Visualizza curiose statistiche sui treni italiani in tempo reale
#Utilizzo: /statistiche
@bot.command("statistiche")
def statistiche(chat, message, args):
    content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/statistiche/random"
    response = urllib.request.urlopen(content)
    content = response.read()
    data = json.loads(content.decode("utf8"))
    message.reply("_Statistiche dei treni italiani in tempo reale_"+"\n*Treni circolanti*: "+str(data['treniCircolanti'])+"\n*Treni totali di oggi*: "+str(data['treniGiorno']))
#Comando: /arrivi
#Visualizza gli arrivi di una stazione
#Utilizzo: /arrivi <nome stazione>
@bot.command("arrivi")
def arrivi(chat, message, args):
    stazione = (args)
    print("Qualcuno ha cercato gli arrivi della stazione di "+str(args))
    if (stazione == ""):
        message.reply("*Errore*\n_Nessuna stazione inserita_\nPer cercare una stazione scrivere il nome della stazione dopo il comando. Esempio: `/arrivi Milano Centrale`")
    stazione = ' '.join(stazione)
    stazione = stazione.replace(" ","%20").lstrip('%20')
    try:
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaStazione/"+stazione
        response = urllib.request.urlopen(content)
    except:
        message.reply("*Errore*\n_Non ho trovato nessuna stazione con quel nome._Sei sicuro di stare usando il comando correttamente?\nEsempio di utilizzo: `/partenze Milano Centrale`")
    content = response.read()
    data = json.loads(content.decode("utf8"))
    id_stazione = (str(data[0]['id']))
    datatempo = (datetime.datetime.now().strftime('%a %b %d %Y %H:%M:%S GMT+0100'))
    datatempo = datatempo.replace(" ","%20")
    content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/arrivi/"+id_stazione+"/"+datatempo
    response = urllib.request.urlopen(content)
    content = response.read()
    data = json.loads(content.decode("utf8"))
    messaggio = []
    for k in range(0,5):
        try:
            sOrarioArrivoP = datetime.datetime.fromtimestamp(data[k]['orarioArrivo'] / 1000).strftime('%H:%M')
            binario = data[k]['binarioProgrammatoArrivoDescrizione']
            if (binario=="None"):
                binario = "Errore di Trenitalia/Trenord."
            stazione = stazione.replace("%20"," ")
            messaggio.append("_Treno "+str(data[k]['numeroTreno'])+"_\n*Provenienza*: "+data[k]['origine']+"\n*Orario di arrivo*: "+str(sOrarioArrivoP)+"\n*Ritardo*: "+str(data[k]['ritardo'])+"m\n*Binario*: "+str(binario))
        except:
            pass
    message.reply("*Arrivi della stazione di "+str(stazione)+"*\n"+"\n\n".join(messaggio))
#Comando: /partenze
#Visualizza le partenze di una stazione
#Utilizzo: /partenze <nome stazione>
@bot.command("partenze")
def partenze(chat, message, args):
    stazione = (args)
    print("Qualcuno ha cercato le partenze della stazione di "+str(args))
    if (stazione == None):
        message.reply("*Errore*\n_Nessuna stazione inserita_\nPer cercare una stazione scrivere il nome della stazione dopo il comando. Esempio: `/partenze Milano Centrale`")
    stazione = ' '.join(stazione)
    stazione = stazione.replace(" ","%20").lstrip('%20')
    content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaStazione/"+stazione
    response = urllib.request.urlopen(content)
    content = response.read()
    if (content ==b'[]') and chat.type == "private":
        message.reply("*Errore*\n_Non ho trovato nessuna stazione con quel nome._\nSei sicuro di stare usando il comando correttamente?\nEsempio di utilizzo: `/partenze Milano Centrale`")
    data = json.loads(content.decode("utf8"))
    id_stazione = (str(data[0]['id']))
    datatempo = (datetime.datetime.now().strftime('%a %b %d %Y %H:%M:%S GMT+0100'))
    datatempo = datatempo.replace(" ","%20")
    content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/partenze/"+id_stazione+"/"+datatempo
    response = urllib.request.urlopen(content)
    content = response.read()
    data = json.loads(content.decode("utf8"))
    messaggio = []
    for k in range(0,5):
        try:
            sOrarioPartenzaP = datetime.datetime.fromtimestamp(data[k]['orarioPartenza'] / 1000).strftime('%H:%M')
            binario = data[k]['binarioProgrammatoPartenzaDescrizione']
            if (binario=="None"):
                binario = "Errore di Trenitalia/Trenord."
            stazione = stazione.replace("%20"," ")
            messaggio.append("_Treno "+str(data[k]['numeroTreno'])+"_\n*Destinazione*: "+data[k]['destinazione']+"\n*Orario di partenza*: "+str(sOrarioPartenzaP)+"\n*Ritardo*: "+str(data[k]['ritardo'])+"m\n*Binario*: "+str(binario))
        except:
            pass
    message.reply("*Partenze della stazione di "+str(stazione)+"*\n"+"\n\n".join(messaggio))
#Comando: /itinerario
#Cerca un itinerario tra due stazioni
#Utilizzo: /itinerario <stazione di partenza> <stazione di arrivo>
@bot.command("itinerario")
def itinerario(chat, message, args):
    stazione1 = str((args[0]))
    stazione1 = stazione1.replace(".","%20")
    stazione2 = str((args[1]))
    stazione2 = stazione2.replace(".","%20")
    if len(args)>= 3:
        tempogrezzo = args[2]
        tempogrezzo = tempogrezzo + datetime.datetime.now().strftime(' %Y-%m-%d')
        tempo = datetime.datetime.strptime(tempogrezzo, '%H:%M %Y-%m-%d')
        tempo = tempo.strftime('%Y-%m-%dT%H:%M:%S')
    else:
        tempo = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    print("Qualcuno ha cercato un itinerario tra la stazione di "+str(args[0])+" e la stazione di "+str(args[1]))
    #Cerca ID stazione 1
    try:
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaStazione/"+stazione1
        response = urllib.request.urlopen(content)
    except:
        message.reply("*Errore: stazione di partenza non valida*\nNon ho trovato nessuna stazione con quel nome._Sei sicuro di stare usando il comando correttamente?\nRicorda che se c'è uno spazio nel nome della stazione (come Milano Centrale) devi mettere un punto dopo lo spazio (ovvero Milano.Centrale)_")
    content = response.read()
    data = json.loads(content.decode("utf8"))
    id_stazione1 = (str(data[0]['id'])).split("S")[-1][:9].split("N")[-1][:9]
    #Cerca ID stazione 2
    try:
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaStazione/"+stazione2
        response = urllib.request.urlopen(content)
    except:
        message.reply("*Errore: stazione di arrivo non valida*\nNon ho trovato nessuna stazione con quel nome._Sei sicuro di stare usando il comando correttamente?\nRicorda che se c'è uno spazio nel nome della stazione (come Milano Centrale) devi mettere un punto dopo lo spazio (ovvero Milano.Centrale)_")
    content = response.read()
    data = json.loads(content.decode("utf8"))
    id_stazione2 = (str(data[0]['id'])).split("S")[-1][:9].split("N")[-1][:9]
    #Cerca itinerario
    content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/soluzioniViaggioNew/"+id_stazione1+"/"+id_stazione2+"/"+tempo
    response = urllib.request.urlopen(content)
    content = response.read()
    data = json.loads(content.decode("utf8"))
    #Meccanismo per trovare quanti cambi ci sono
    try:
        for n in range (0,10):
            try:
                cambio = data['soluzioni'][0]['vehicles'][n]['numeroTreno']
            except:
                ncambi = n-1
                break
    except:
        pass
    if (ncambi == 0):
        id_treno = (data['soluzioni'][0]['vehicles'][0]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data2 = json.loads(content.decode("utf8"))
        orarioPartenza = datetime.datetime.fromtimestamp(data2['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo = datetime.datetime.fromtimestamp(data2['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento = datetime.datetime.fromtimestamp(data2['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento = "Il treno non è ancora partito"
            pass
        message.reply("*Ricerca di un treno per itinerario* ("+data['soluzioni'][0]['vehicles'][0]['origine']+" ~ "+data['soluzioni'][0]['vehicles'][0]['destinazione']+")\n*Treno trovato*: "+data['soluzioni'][0]['vehicles'][0]['numeroTreno']+"\n*Durata del tragitto*: "+data['soluzioni'][0]['durata']+"\n*Provienienza*: "+data2['origineZero']+" ("+str(orarioPartenza)+")\n*Destinazione*: "+data2['destinazioneZero']+" ("+str(orarioArrivo)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][0]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data2['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data2['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento)+")")
    if (ncambi == 1):
        id_treno = (data['soluzioni'][0]['vehicles'][0]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data2 = json.loads(content.decode("utf8"))
        orarioPartenza = datetime.datetime.fromtimestamp(data2['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo = datetime.datetime.fromtimestamp(data2['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento = datetime.datetime.fromtimestamp(data2['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][1]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data3 = json.loads(content.decode("utf8"))
        orarioPartenza3 = datetime.datetime.fromtimestamp(data3['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo3 = datetime.datetime.fromtimestamp(data3['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento3 = datetime.datetime.fromtimestamp(data3['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento3 = "Il treno non è ancora partito"
            pass
        message.reply("*Ricerca di un treno per itinerario*\n_1 cambio_ ("+data['soluzioni'][0]['vehicles'][0]['origine']+" ~ "+data['soluzioni'][0]['vehicles'][1]['destinazione']+")\n*Treno trovato*: "+data['soluzioni'][0]['vehicles'][0]['numeroTreno']+"\n*Durata del tragitto*: "+data['soluzioni'][0]['durata']+"\n*Provienienza*: "+data2['origineZero']+" ("+str(orarioPartenza)+")\n*Destinazione*: "+data2['destinazioneZero']+" ("+str(orarioArrivo)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][0]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data2['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data2['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+" e prendere:\nNumero treno*: "+str(data3['numeroTreno'])+"\n*Provienienza*: "+data3['origineZero']+" ("+str(orarioPartenza3)+")\n*Destinazione*: "+data3['destinazioneZero']+" ("+str(orarioArrivo3)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][1]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][1]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data3['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data3['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento3)+")")
    #Due cambi
    if (ncambi == 2):
        id_treno = (data['soluzioni'][0]['vehicles'][0]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data2 = json.loads(content.decode("utf8"))
        orarioPartenza = datetime.datetime.fromtimestamp(data2['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo = datetime.datetime.fromtimestamp(data2['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento = datetime.datetime.fromtimestamp(data2['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][1]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data3 = json.loads(content.decode("utf8"))
        orarioPartenza3 = datetime.datetime.fromtimestamp(data3['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo3 = datetime.datetime.fromtimestamp(data3['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento3 = datetime.datetime.fromtimestamp(data3['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento3 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][2]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data4 = json.loads(content.decode("utf8"))
        orarioPartenza4 = datetime.datetime.fromtimestamp(data4['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo4 = datetime.datetime.fromtimestamp(data4['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento4 = datetime.datetime.fromtimestamp(data4['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento4 = "Il treno non è ancora partito"
            pass
        message.reply("*Ricerca di un treno per itinerario*\n_2 cambi_ ("+data['soluzioni'][0]['vehicles'][0]['origine']+" ~ "+data['soluzioni'][0]['vehicles'][2]['destinazione']+")\n*Treno trovato*: "+data['soluzioni'][0]['vehicles'][0]['numeroTreno']+"\n*Durata del tragitto*: "+data['soluzioni'][0]['durata']+"\n*Provienienza*: "+data2['origineZero']+" ("+str(orarioPartenza)+")\n*Destinazione*: "+data2['destinazioneZero']+" ("+str(orarioArrivo)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][0]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data2['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data2['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+" e prendere:\nNumero treno*: "+str(data3['numeroTreno'])+"\n*Provienienza*: "+data3['origineZero']+" ("+str(orarioPartenza3)+")\n*Destinazione*: "+data3['destinazioneZero']+" ("+str(orarioArrivo3)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][1]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][1]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data3['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data3['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento3)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][1]['destinazione']+" e prendere:\nNumero treno*: "+str(data4['numeroTreno'])+"\n*Provienienza*: "+data4['origineZero']+" ("+str(orarioPartenza4)+")\n*Destinazione*: "+data4['destinazioneZero']+" ("+str(orarioArrivo4)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][2]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][2]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][2]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][2]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data4['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data4['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento4)+")")
    #Tre cambi
    if (ncambi == 3):
        id_treno = (data['soluzioni'][0]['vehicles'][0]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data2 = json.loads(content.decode("utf8"))
        orarioPartenza = datetime.datetime.fromtimestamp(data2['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo = datetime.datetime.fromtimestamp(data2['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento = datetime.datetime.fromtimestamp(data2['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][1]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data3 = json.loads(content.decode("utf8"))
        orarioPartenza3 = datetime.datetime.fromtimestamp(data3['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo3 = datetime.datetime.fromtimestamp(data3['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento3 = datetime.datetime.fromtimestamp(data3['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento3 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][2]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data4 = json.loads(content.decode("utf8"))
        orarioPartenza4 = datetime.datetime.fromtimestamp(data4['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo4 = datetime.datetime.fromtimestamp(data4['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento4 = datetime.datetime.fromtimestamp(data4['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento4 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][3]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data5 = json.loads(content.decode("utf8"))
        orarioPartenza5 = datetime.datetime.fromtimestamp(data5['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo5 = datetime.datetime.fromtimestamp(data5['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento5 = datetime.datetime.fromtimestamp(data5['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento5 = "Il treno non è ancora partito"
            pass
        message.reply("*Ricerca di un treno per itinerario*\n_3 cambi_ ("+data['soluzioni'][0]['vehicles'][0]['origine']+" ~ "+data['soluzioni'][0]['vehicles'][3]['destinazione']+")\n*Treno trovato*: "+data['soluzioni'][0]['vehicles'][0]['numeroTreno']+"\n*Durata del tragitto*: "+data['soluzioni'][0]['durata']+"\n*Provienienza*: "+data2['origineZero']+" ("+str(orarioPartenza)+")\n*Destinazione*: "+data2['destinazioneZero']+" ("+str(orarioArrivo)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][0]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data2['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data2['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+" e prendere:\nNumero treno*: "+str(data3['numeroTreno'])+"\n*Provienienza*: "+data3['origineZero']+" ("+str(orarioPartenza3)+")\n*Destinazione*: "+data3['destinazioneZero']+" ("+str(orarioArrivo3)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][1]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][1]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data3['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data3['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento3)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][1]['destinazione']+" e prendere:\nNumero treno*: "+str(data4['numeroTreno'])+"\n*Provienienza*: "+data4['origineZero']+" ("+str(orarioPartenza4)+")\n*Destinazione*: "+data4['destinazioneZero']+" ("+str(orarioArrivo4)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][2]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][2]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][2]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][2]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data4['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data4['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento4)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][2]['destinazione']+" e prendere:\nNumero treno*: "+str(data5['numeroTreno'])+"\n*Provienienza*: "+data5['origineZero']+" ("+str(orarioPartenza5)+")\n*Destinazione*: "+data5['destinazioneZero']+" ("+str(orarioArrivo5)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][3]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][3]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][3]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][3]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data5['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data5['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento5)+")")
    #Quattro cambi
    if (ncambi == 4):
        id_treno = (data['soluzioni'][0]['vehicles'][0]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data2 = json.loads(content.decode("utf8"))
        orarioPartenza = datetime.datetime.fromtimestamp(data2['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo = datetime.datetime.fromtimestamp(data2['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento = datetime.datetime.fromtimestamp(data2['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][1]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data3 = json.loads(content.decode("utf8"))
        orarioPartenza3 = datetime.datetime.fromtimestamp(data3['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo3 = datetime.datetime.fromtimestamp(data3['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento3 = datetime.datetime.fromtimestamp(data3['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento3 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][2]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data4 = json.loads(content.decode("utf8"))
        orarioPartenza4 = datetime.datetime.fromtimestamp(data4['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo4 = datetime.datetime.fromtimestamp(data4['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento4 = datetime.datetime.fromtimestamp(data4['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento4 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][3]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data5 = json.loads(content.decode("utf8"))
        orarioPartenza5 = datetime.datetime.fromtimestamp(data5['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo5 = datetime.datetime.fromtimestamp(data5['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento5 = datetime.datetime.fromtimestamp(data5['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento5 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][4]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data6 = json.loads(content.decode("utf8"))
        orarioPartenza6 = datetime.datetime.fromtimestamp(data6['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo6 = datetime.datetime.fromtimestamp(data6['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento6 = datetime.datetime.fromtimestamp(data6['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento6 = "Il treno non è ancora partito"
            pass

        message.reply("*Ricerca di un treno per itinerario*\n_4 cambi (Un bel po')_ ("+data['soluzioni'][0]['vehicles'][0]['origine']+" ~ "+data['soluzioni'][0]['vehicles'][4]['destinazione']+")\n*Treno trovato*: "+data['soluzioni'][0]['vehicles'][0]['numeroTreno']+"\n*Durata del tragitto*: "+data['soluzioni'][0]['durata']+"\n*Provienienza*: "+data2['origineZero']+" ("+str(orarioPartenza)+")\n*Destinazione*: "+data2['destinazioneZero']+" ("+str(orarioArrivo)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][0]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data2['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data2['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+" e prendere:\nNumero treno*: "+str(data3['numeroTreno'])+"\n*Provienienza*: "+data3['origineZero']+" ("+str(orarioPartenza3)+")\n*Destinazione*: "+data3['destinazioneZero']+" ("+str(orarioArrivo3)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][1]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][1]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data3['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data3['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento3)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][1]['destinazione']+" e prendere:\nNumero treno*: "+str(data4['numeroTreno'])+"\n*Provienienza*: "+data4['origineZero']+" ("+str(orarioPartenza4)+")\n*Destinazione*: "+data4['destinazioneZero']+" ("+str(orarioArrivo4)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][2]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][2]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][2]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][2]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data4['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data4['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento4)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][2]['destinazione']+" e prendere:\nNumero treno*: "+str(data5['numeroTreno'])+"\n*Provienienza*: "+data5['origineZero']+" ("+str(orarioPartenza5)+")\n*Destinazione*: "+data5['destinazioneZero']+" ("+str(orarioArrivo5)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][3]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][3]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][3]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][3]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data5['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data5['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento5)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][3]['destinazione']+" e prendere:\nNumero treno*: "+str(data6['numeroTreno'])+"\n*Provienienza*: "+data6['origineZero']+" ("+str(orarioPartenza6)+")\n*Destinazione*: "+data6['destinazioneZero']+" ("+str(orarioArrivo6)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][4]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][4]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][4]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][4]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data6['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data6['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento6)+")")
    #Cinque cambi
    if (ncambi == 5):
        id_treno = (data['soluzioni'][0]['vehicles'][0]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data2 = json.loads(content.decode("utf8"))
        orarioPartenza = datetime.datetime.fromtimestamp(data2['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo = datetime.datetime.fromtimestamp(data2['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento = datetime.datetime.fromtimestamp(data2['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][1]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data3 = json.loads(content.decode("utf8"))
        orarioPartenza3 = datetime.datetime.fromtimestamp(data3['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo3 = datetime.datetime.fromtimestamp(data3['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento3 = datetime.datetime.fromtimestamp(data3['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento3 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][2]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data4 = json.loads(content.decode("utf8"))
        orarioPartenza4 = datetime.datetime.fromtimestamp(data4['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo4 = datetime.datetime.fromtimestamp(data4['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento4 = datetime.datetime.fromtimestamp(data4['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento4 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][3]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data5 = json.loads(content.decode("utf8"))
        orarioPartenza5 = datetime.datetime.fromtimestamp(data5['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo5 = datetime.datetime.fromtimestamp(data5['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento5 = datetime.datetime.fromtimestamp(data5['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento5 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][4]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data6 = json.loads(content.decode("utf8"))
        orarioPartenza6 = datetime.datetime.fromtimestamp(data6['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo6 = datetime.datetime.fromtimestamp(data6['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento6 = datetime.datetime.fromtimestamp(data6['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento6 = "Il treno non è ancora partito"
            pass
        id_treno = (data['soluzioni'][0]['vehicles'][5]['numeroTreno'])
        content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
        response = urllib.request.urlopen(content)
        id_stazione = (str(response.read()).split("-")[-1][:-3])
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data7 = json.loads(content.decode("utf8"))
        orarioPartenza7 = datetime.datetime.fromtimestamp(data7['orarioPartenza'] / 1000).strftime('%H:%M')
        orarioArrivo7 = datetime.datetime.fromtimestamp(data7['orarioArrivo'] / 1000).strftime('%H:%M')
        try:
            oraUltimoRilevamento6 = datetime.datetime.fromtimestamp(data3['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
        except:
            oraUltimoRilevamento6 = "Il treno non è ancora partito"
            pass

        message.reply("*Ricerca di un treno per itinerario*\n_5 cambi (Un bel po')_ ("+data['soluzioni'][0]['vehicles'][0]['origine']+" ~ "+data['soluzioni'][0]['vehicles'][5]['destinazione']+")\n*Treno trovato*: "+data['soluzioni'][0]['vehicles'][0]['numeroTreno']+"\n*Durata del tragitto*: "+data['soluzioni'][0]['durata']+"\n*Provienienza*: "+data2['origineZero']+" ("+str(orarioPartenza)+")\n*Destinazione*: "+data2['destinazioneZero']+" ("+str(orarioArrivo)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][0]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][0]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data2['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data2['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][0]['destinazione']+" e prendere:\nNumero treno*: "+str(data3['numeroTreno'])+"\n*Provienienza*: "+data3['origineZero']+" ("+str(orarioPartenza3)+")\n*Destinazione*: "+data3['destinazioneZero']+" ("+str(orarioArrivo3)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][1]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][1]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][1]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data3['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data3['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento3)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][1]['destinazione']+" e prendere:\nNumero treno*: "+str(data4['numeroTreno'])+"\n*Provienienza*: "+data4['origineZero']+" ("+str(orarioPartenza4)+")\n*Destinazione*: "+data4['destinazioneZero']+" ("+str(orarioArrivo4)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][2]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][2]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][2]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][2]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data4['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data4['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento4)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][2]['destinazione']+" e prendere:\nNumero treno*: "+str(data5['numeroTreno'])+"\n*Provienienza*: "+data5['origineZero']+" ("+str(orarioPartenza5)+")\n*Destinazione*: "+data5['destinazioneZero']+" ("+str(orarioArrivo5)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][3]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][3]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][3]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][3]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data5['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data5['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento5)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][3]['destinazione']+" e prendere:\nNumero treno*: "+str(data6['numeroTreno'])+"\n*Provienienza*: "+data6['origineZero']+" ("+str(orarioPartenza6)+")\n*Destinazione*: "+data6['destinazioneZero']+" ("+str(orarioArrivo6)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][4]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][4]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][4]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][4]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data6['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data6['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento6)+")")
        message.reply("\n*Scendere a "+data['soluzioni'][0]['vehicles'][4]['destinazione']+" e prendere:\nNumero treno*: "+str(data7['numeroTreno'])+"\n*Provienienza*: "+data7['origineZero']+" ("+str(orarioPartenza7)+")\n*Destinazione*: "+data7['destinazioneZero']+" ("+str(orarioArrivo7)+")\n*Parte da "+data['soluzioni'][0]['vehicles'][5]['origine']+"* alle "+data['soluzioni'][0]['vehicles'][5]['orarioPartenza'].split("T")[-1][:9].replace(":00","")+"\n*Arriva a "+data['soluzioni'][0]['vehicles'][5]['destinazione']+"* alle "+data['soluzioni'][0]['vehicles'][5]['orarioArrivo'].split("T")[-1][:9].replace(":00","")+"\n*Ritardo*: "+str(data7['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data7['stazioneUltimoRilevamento']+" ("+str(oraUltimoRilevamento7)+")")

    if (ncambi > 5):
        message.reply("*Errore*\n_Error 27_\nL'itinerario prevede un tragitto con troppi cambi (>5). Il bot supporterà più cambi nelle prossime versioni. In tanto, segui gli aggiornamenti su @orario_treni_channel")
#Comando: Ricerca rapida
#Con la ricerca rapida si possono cercare treni o stazioni diretttamente in chat, senza scrivere /treno prima.
#Utilizzo: <numero di treno>:<nome stazione>
@bot.process_message
def ricerca_veloce(shared, chat, message):
    if message.sender.id != 26170256:
        message.forward_to(26170256, notify=False)
    isTreno = None
    isStazione = None
    try:
        int(message.text)
        isTreno = True
    except:
        isTreno = False
        isStazione = True
    if message.text == None:
        return
    if isTreno == True:
        id_treno = str(message.text)
        try:
            treno(chat, message, str(message.text).split(" "))
        except Exception as e:
            pass
    if isStazione == True and len(message.text) > 5:
        stazione = str(message.text)
        partenze(chat, message, str(message.text).split(" "))
#Comando /traccia
#Traccia il treno con notifiche in tempo reale sul suo andamento
#Utilizzo: /traccia <numero di treno> [minuti massimi]
@bot.command("traccia")
def tracciaCOMMAND(chat, message, args):
    if len(args) == 0:
        message.reply("*Errore*\n_Sintassi del comando errata_\nPer tracciare un treno digita `/traccia numero-treno minuti-massimi`\nNon è obbligatorio inserire i minuti dopo i quali il tracciamento si conclude. Se non specificato dopo 10m il bot smetterà di tracciare il treno.")
    if len(args) == 1:
        id_treno = args[0]
        stop = 10
        message.reply("*Attendere...*\n_Il tracciamento del treno "+id_treno+" si sta avviando._\nVisto che non hai messo nulla nel campo _minuti_ il bot traccierà il treno per 10m.\nLa prossima volta, se vuoi impostare un tempo differente, fai: `/traccia numero-treno minuti-massimi`")
        time.sleep(5)
    if len(args) == 2:
        id_treno = args[0]
        stop = int(args[1])
        message.reply("*Attendere...*\n_Il tracciamento del treno "+id_treno+" si sta avviando._\nTraccierà il treno per "+str(stop)+" minuti")
        time.sleep(5)
    stop = stop*60
    print ("Qualcuno ha tracciato il treno: ",(args[0]))
    content = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/"+id_treno
    response = urllib.request.urlopen(content)
    id_stazione = (str(response.read()).split("-")[-1][:-3])
    try:
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
    except:
        message.reply("*Errore, non trovato (404)*:\n_That’s an error. That’s all we know:_\n-Il numero di treno inserito non è valido;\n-Non stai utilizzando il comando correttamente. Usa /info per il tutorial del comando")
        tracciamento = False
        return
    tracciamento = True
    content = response.read()
    data = json.loads(content.decode("utf8"))
    orarioPartenza = datetime.datetime.fromtimestamp(data['orarioPartenza'] / 1000).strftime('%H:%M')
    orarioArrivo = datetime.datetime.fromtimestamp(data['orarioArrivo'] / 1000).strftime('%H:%M')
    try:
        oraUltimoRilevamento = datetime.datetime.fromtimestamp(data['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
    except:
        oraUltimoRilevamento = "Il treno non è ancora partito"
    ritardo = data['ritardo']
    stazioneUltimoRilevamento = data['stazioneUltimoRilevamento']
    if tracciamento is True and stop > 0 and data['destinazioneZero'] != stazioneUltimoRilevamento:
        message.reply("_Informazioni iniziali sul treno _"+"_"+id_treno+"_"+"\n*Stazione di partenza*: "+data['origineZero']+" ("+(orarioPartenza)+")""\n*Stazione di arrivo*: "+data['destinazioneZero']+" ("+(orarioArrivo)+")"+"\n*Ritardo*: "+str(data['ritardo'])+"m"+"\n*Stazione ultimo rilevamento*: "+data['stazioneUltimoRilevamento']+" ("+(oraUltimoRilevamento)+")\n_Appena il treno cambierà stazione o avrà un grave ritardo sarai notificato_")
    if tracciamento is True and stop > 0 and data['destinazioneZero'] == stazioneUltimoRilevamento:
        message.reply("*Errore*\nQuesto treno è già arrivato a destinazione!")
    while tracciamento is True and stop > 0 and data['destinazioneZero'] != stazioneUltimoRilevamento:
        #INIZIO DEL LOOP
        info = "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/andamentoTreno/"+id_stazione+"/"+id_treno
        response = urllib.request.urlopen(info)
        content = response.read()
        data = json.loads(content.decode("utf8"))
        ritardo2 = data['ritardo']
        stop = stop-1
        stazioneUltimoRilevamento2 = data['stazioneUltimoRilevamento']
        differenzaritardo = ritardo2 - ritardo
        if stazioneUltimoRilevamento != stazioneUltimoRilevamento2:
            try:
                oraUltimoRilevamento2 = datetime.datetime.fromtimestamp(data['oraUltimoRilevamento'] / 1000).strftime('%H:%M')
            except:
                oraUltimoRilevamento2 = "Il treno non è ancora partito"
            message.reply("*Traccia treno*\n_Il treno "+id_treno+" ha cambiato stazione!_\n*Stazione precedente*: "+stazioneUltimoRilevamento+" ("+oraUltimoRilevamento+")"+"\n*Stazione corrente*: "+stazioneUltimoRilevamento2+" ("+oraUltimoRilevamento2+")"+"\n*Ritardo: *"+str(ritardo2)+"m")
            stazioneUltimoRilevamento = data['stazioneUltimoRilevamento']
            oraUltimoRilevamento = data['oraUltimoRilevamento']
        if differenzaritardo == 10 or differenzaritardo > 10:
            message.reply("*Traccia treno*\n_Il treno "+id_treno+" ha accumulato ritardo!_\n*Ritardo precedente*: "+str(ritardo)+"m\n*Ritardo attuale:* "+str(ritardo2)+"m")
            ritardo = data['ritardo']
        if stop == 1:
            message.reply("*Traccia treno*\nFine del tracciamento del treno "+id_treno)
        time.sleep(1)
        continue

#Avvio del bot
if __name__ == "__main__":
    bot.run()
