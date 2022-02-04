import googletrans
print(googletrans.LANGUAGES)


from googletrans import Translator
 
d = {}
translator = Translator()
for i in googletrans.LANGUAGES:
    text1 = googletrans.LANGUAGES[i]
    trans1 = translator.translate(text1, src='en', dest='ko')
    d[i] = trans1.text
    print(i, trans1.text)
print(d)



