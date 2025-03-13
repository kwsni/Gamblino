from ninja import Schema, ModelSchema

from inventory.models import ItemWear, Item, Case

class PatchCasePriceSchema(ModelSchema):
    class Meta:
        model = Case
        fields = ['price']

class PatchItemPriceSchema(ModelSchema):
    class Meta:
        model = ItemWear
        fields = ['price']

class LootSchema(Schema):
    uid: int
    username: str
    item: str
    wear: str
    rarity: str
