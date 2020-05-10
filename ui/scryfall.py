from browser import ajax


def get_images_url(card: str, on_result):
    def parse(response):
        start = response.text.index('small')
        start += len('small') + 3
        end = response.text.index(',', start)
        end -= 1
        image_url = response.text[start:end]
        on_result(image_url)

    request = ajax.Ajax()
    request.bind('complete', parse)
    request.open(
        'GET',
        'https://api.scryfall.com/cards/named?exact=' + card.replace(' ', '+')
    )
    request.send()
