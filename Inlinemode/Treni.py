import botogram

import API
import Bot

from Inlinemode import Inline

def inline(bot, chains, update):
    update_id = update.inline_query.id
    sender = update.inline_query.sender
    query = update.inline_query.query

    data, success, error = API.orarioTreni.cercaTreno(query)
    messaggio = API.Messaggi.treno1(data)

    bot.api.call("answerInlineQuery", {
                    "switch_pm_text":"Serve aiuto? Premi qui!",
                    "switch_pm_parameter":"inline",
                    "inline_query_id": update_id,
                    "cache_time": 0,
                    "results":'[{'+
                        '"type":"article",'+
                        '"id":"1",'+
                        '"title":"Ho trovato il treno '+query+'",'+
                        '"thumb_url":"http://i.imgur.com/polck8Z.png",'+
                        '"description":"Clicca qui per visualizzare le informazioni sul treno '+query+'",'+
                        '"input_message_content":{'+
                            '"message_text":"'+messaggio+'",'+
                            '"parse_mode":"HTML"'+
                        '}, '+
                        '"reply_markup":{"inline_keyboard":'+
                            '['+
                            '[{"text":"🚉Lista fermate", "callback_data":"list@'+query+'"}, {"text":"🔄Aggiorna le informazioni","callback_data":"agg$'+query+'"}],'+
                            '[{"text":"🔙Vai al menù inline","callback_data":"home"}]'+
                            ']'+
                        '}'+
                    '}]'
            })


    return

    try:
        bot.api.call("answerInlineQuery", {
                        "switch_pm_text":"Non sai come si usa? Clicca qui!",
                        "switch_pm_parameter":"inline",
                        "inline_query_id": update_id,
                        "cache_time": 0,
                        "results":'[{'+
                            '"type":"article",'+
                            '"id":"1",'+
                            '"title":"Stazioni che iniziano con '+query+'",'+
                            '"thumb_url":"http://i.imgur.com/HdI91z6.png",'+
                            '"description":"Ho trovato molte stazioni che iniziano con '+query+', premi qui per selezionarne una!",'+
                            '"input_message_content":{'+
                                '"message_text":"'+messaggio+'",'+
                                '"parse_mode":"HTML"'+
                            '}, '+
                            '"reply_markup":{"inline_keyboard":'+
                                inline_keyboard+
                            '}'+
                        '}]'
                })

    except botogram.api.APIError:
        testo = "Ho trovato troppe stazioni <b>con quel nome</b>.\nRiprova con una ricerca più <b>specifica</b>"
        bot.api.call("answerInlineQuery", {
                        "switch_pm_text":"Non sai come si usa? Clicca qui!",
                        "switch_pm_parameter":"inline",
                        "inline_query_id": update_id,
                        "cache_time": 0,
                        "results":'[{'+
                            '"type":"article",'+
                            '"id":"1",'+
                            '"title":"Troppe stazioni trovate!",'+
                            '"thumb_url":"http://i.imgur.com/f8whiXJ.png",'+
                            '"description":"Ho troppe stazioni che iniziano con '+query+'. Sii più specifico!",'+
                            '"input_message_content":{'+
                                '"message_text":"'+messaggio+'",'+
                                '"parse_mode":"HTML"'+
                            '}, '+
                            '"reply_markup":{"inline_keyboard":'+
                                '['+
                                '[{"text":"🔙Vai al bot","url":"telegram.me/dev_orario_treni_bot?start=inline"}]'+
                                ']'+
                            '}'+
                        '}]'
                        '}]'
                })
