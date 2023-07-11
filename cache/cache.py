class CPF:
    cache = {}

    def __init__(self, cpf):
        self.cpf = cpf
        self.offers = {}

        CPF.cache[cpf] = self

    def check_offers(self):
        if self.offers:
            return self.offers
        else:
            return False

    def add_offers(self, offers):
        self.offers = offers