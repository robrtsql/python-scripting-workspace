import os.path
import requests
import time
import shutil

CARD_PIC_DIR = "/home/rob/.cache/forge/pics/cards"

def get_cards():
    cards = []
    with open("deck.txt") as deck_txt:
        lines = deck_txt.readlines()
        for line in lines:
            cards.append(" ".join(line.split(" ")[1:]).rstrip())
    missing_cards = []
    for card in cards:
        if card:
            if not os.path.isfile(f"{CARD_PIC_DIR}/{card}.fullborder.jpg"):
                missing_cards.append(card)
    # missing_cards = [missing_cards[0]]
    for missing_card in missing_cards:
        time.sleep(1)
        card_name = missing_card.replace(" ", "+")
        r = requests.get(f"https://api.scryfall.com/cards/named?exact={card_name}")
        r.raise_for_status()
        try:
            image_url = r.json()["image_uris"]["normal"]
            r = requests.get(image_url, stream=True)
            r.raise_for_status()
            with open(f"{CARD_PIC_DIR}/{missing_card}.fullborder.jpg", 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            print(f"Downloaded to {CARD_PIC_DIR}/{missing_card}.fullborder.jpg")
        except KeyError:
            print(f"Something went wrong with {missing_card}")


if __name__ == "__main__":
    get_cards()