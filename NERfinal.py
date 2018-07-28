
import re
import string
import polyglot
from polyglot.text import Text, Word
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("ner.html",lang="",ner="")

@app.route("/query")
def query():
    persons=[]
    organizations=[]
    locations=[]

    article = request.args.get('article')
    exclude = set(string.punctuation)

    #remove_punctuation
    article=''.join(ch for ch in article if ch not in exclude)

    #remove_english_letters
    article=re.sub(r'[a-zA-Z?]', '',article).strip()

    text = Text(article)

    #language detection
    language=text.language.name

    #NER
    ner=text.entities

    for entity in ner:
        if entity.tag=='I-PER':
           edit_per=" ".join(entity)
           if  edit_per  not in persons:
              persons.append(edit_per)
		elif entity.tag=='I-ORG':
             edit_org=" ".join(entity)
             if edit_org not in organizations:
                organizations.append(edit_org)

        else:
            edit_loc=" ".join(entity)
            if edit_loc not in locations:
               locations.append(edit_loc)

    persons=",".join(persons)
    organizations=",".join(organizations)
    locations=",".join(locations)

    key_words=persons+","+organizations+","+locations
    #key_words=(itertools.chain(persons,organizations,locations))
    #for x in key_words:
       # data=x.text()
    return render_template("ner.html",lang=language,per=persons,org=organizations,loc=locations,key=key_words)

if __name__ == '__main__':
    app.run(host='',port=)
