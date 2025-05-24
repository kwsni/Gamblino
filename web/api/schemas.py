from inventory.models import Case, ItemPrice
from ninja import ModelSchema, Schema


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
    stattrak: bool
    rarity: str
