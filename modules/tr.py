import urllib
import misc
from simplejson import loads
from misc import _

def main(bot, args):
    '''tr <from_lang> <to_lang> <text>\nTranslate text.\nSee also: wtf'''

    if len(args) > 2:
        if args[0] == args[1]:
            return 'baka baka baka!'
        else:
            return translate(args[0], args[1], ' '.join(args[2:]))

def translate(from_l, to_l, text):
    text = urllib.quote(text.encode('utf-8'))
    try:
        data = misc.readUrl('http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q=%s&langpair=%s%%7C%s' %(text, from_l, to_l))
        if not data: return 'can\'t get data'
    except:
        return _("google is not available, sorry.")
   
    try:
        convert = loads(data)
        status = convert['responseStatus']

        results = convert['responseData']['translatedText']
        if results: 
            return results
    except:
        pass

    return 'can\'t translate this shit!'

def info(bot):
    return (("tr",), 10, main)
