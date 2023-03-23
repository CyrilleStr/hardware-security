from smartcard.System import readers

from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString

from smartcard.CardConnectionObserver import ConsoleCardConnectionObserver
from smartcard.CardMonitoring import CardMonitor, CardObserver

__author__ = "Marina Shchavleva"
__maintainer__ = "Marina Shchavleva"
__email__ = "shchamar@fit.cvut.cz"
__status__ = "garbage"

def get_readers():
    return readers()


class Reader:
    """Creates connection to reader, sends and receives messages"""
#     def __init__(self, reader_id):
#         found_readers = readers()
#         self.connection = found_readers[reader_id].createConnection()
#         self.connection.connect()

    def __init__(self):

        cardrequest = CardRequest( timeout=1, cardType=AnyCardType() )
        self.cardservice = cardrequest.waitforcard()
        self.cardservice.connection.connect()

    def send(self, apdu: list):
        return self.cardservice.connection.transmit(apdu)

    def send_encrypt(self, data: list):
        encryption_prefix = [ 0x80, 0x60, 0x00, 0x00 ]
        apdu = encryption_prefix + [len(data)] + data + [len(data)]
        received, sw1, sw2 = self.send(apdu)
        return received


class Card:
    def __init__(self, card_obj, observer):
        self.card = card_obj
        self.card.connection = self.card.createConnection()
        self.card.connection.connect()
        self.card.connection.addObserver(observer)

    def send(self, apdu: list):
        return self.card.connection.transmit(apdu)

    def send_encrypt(self, data: list):
        encryption_prefix = [ 0x80, 0x60, 0x00, 0x00 ]
        apdu = encryption_prefix + [len(data)] + data + [len(data)]
        received, sw1, sw2 = self.send(apdu)
        return received


class Observer(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def __init__(self, callback):
        self.observer = ConsoleCardConnectionObserver()
        self.on_insert_callback = callback

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            print("Vložení karty...")
            self.on_insert_callback(Card(card, self.observer))

        for card in removedcards:
            print("Karta odstraněná.")

