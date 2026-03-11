from enum import StrEnum

class ProductTypeEnum(StrEnum):
    lesa = "lesa"
    monolit = "monolit"
    taxta_opalubka = "taxta_opalubka"
    metal_opalubka = "metal_opalubka"


class ProductSizeEnum(StrEnum):
    katta = "katta"
    orta = "orta"
    kichik = "kichik"
    four_meters = "four_meters"
    three_meters = "three_meters"
    two_meters = "two_meters"
    one_meter = "one_meter"


class RentStatusEnum(StrEnum):
    active = "Ижарада"
    returned = "Қайтарилган"


class PaymentStatusEnum(StrEnum):
    full_paid = "Тўлиқ ✅"
    part_paid = "Қисман ⚠️"
    not_paid = "Тўланмаган ❌"