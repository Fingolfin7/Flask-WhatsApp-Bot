import requests
import wikipediaapi
import randfacts
from datetime import datetime
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/sms", methods=['POST'])
def sms_reply():
    today = datetime.today()

    # Fetch the message
    msg = request.form.get('Body').lower()

    # response object
    resp = MessagingResponse()

    if msg.lower().find("hi") != -1:
        phase = "morning"
        if 12 <= today.hour < 18:
            phase = "afternoon"
        elif today.hour > 18:
            phase = "evening"

        resp.message(f"Good {phase}. Here are the available commands.\n"
                     f"#quote (search for a quote)\n"
                     f"#poem (search for a poem title)\n"
                     f"#wiki (quick wikipedia summary)\n"
                     f"#fact (random fact)\n")

    if "#quote" in msg:
        query = msg.replace('#quote ', '')
        r = requests.get(f'http://api.quotable.io/search/quotes?query={query}')
        if r.status_code == 200:
            data = r.json()
            search_result = data['results'][0]
            quote = f'{search_result["content"]} ({search_result["author"]})'
        else:
            print()
            quote = "Sorry I can't find that quote right now, please try again later."
        resp.message(quote)
    if "#poem" in msg:
        title, author = [section.strip() for section in msg.replace('#poem ', '').split(";")]
        print(title, author)
        if author and title:
            r = requests.get(f'https://poetrydb.org/title,author/{title};{author}')
        elif author:
            r = requests.get(f'https://poetrydb.org/author/{author}')
        else:
            r = requests.get(f'https://poetrydb.org/title/{title}')

        if r.status_code != 200:
            quote = "Sorry I can't find that poem now, please try again later."
            resp.message(quote)
            return str(resp)

        if 'status' and 'reason' in r.json():
            try:
                others = requests.get(f'https://poetrydb.org/title/{title}').json()
                print(others)
                found_list = ["{} by {}".format(poem['title'], poem['author']) for poem in others]
                found_list = "\n".join(found_list)
            except:
                found_list = ""
            quote = f"Couldn't find '{title}' by '{author}'."
            if len(found_list) > 0:
                quote += f"\nFound these: \n\n{found_list}"
        else:
            if title or title and author:
                data = r.json()[0]
                text = "\n".join(data["lines"])
                if len(text) >= 1600:
                    quote = f"{data['title']} by {data['author']} is too long to send!"
                else:
                    quote = f'{data["title"]} by {data["author"]}\n\n' \
                            f'{text}'
            else:
                data = r.json()
                quote = f"Poems by {data[0]['author']}:\n"
                quote += "\n".join([poem['title'] for poem in data[:5]])
                if len(r.json()) > 5:
                    quote += "\n    +many more..."
        resp.message(quote)
    elif "#wiki" in msg:
        query = msg.replace('#wiki ', '')
        wiki = wikipediaapi.Wikipedia('en')
        try:
            page = wiki.page(query)
            url = page.fullurl
            summary = page.summary[0:1500]
            resp.message(f'According to wikipedia..\n\n{summary}...\n{url}')
        except:
            resp.message("Sorry can't find anything.\nTry another search..")

    elif "#fact" in msg:
        try:
            facts = randfacts.get_fact()
            resp.message(facts)
        except:
            resp.message('Sorry.. No Facts Found!!')

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
