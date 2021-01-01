import urllib.request,json


def getquote():
    getquote_url ='https://parallelum.com.br/fipe/api/v1/carros/marcas/59/modelos/5940/anos/2014-3'

    with urllib.request.urlopen(getquote_url) as url:
        get_quote_data = url.read()
        get_quote_response = json.loads(get_quote_data)

    return get_quote_response