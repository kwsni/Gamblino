from ninja import Schema, ModelSchema

from inventory.models import ItemPrice, Item, Case

class PatchCasePriceSchema(ModelSchema):
    class Meta:
        model = Case
        fields = ['price']

class PatchItemPriceSchema(ModelSchema):
    class Meta:
        model = ItemPrice
        fields = ['price']

class LootSchema(Schema):
    uid: int
    username: str
    item: str
    wear: str
    stattrak: str
    rarity: str
