from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Menus(models.Model):
    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=250)
    description = fields.TextField()

    class Meta:
        table = "Menus"


class Submenus(models.Model):
    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=250)
    description = fields.TextField()
    menu = fields.ForeignKeyField(
        "models.Menus", related_name="submenu_menu",
        on_delete=fields.CASCADE
    )

    class Meta:
        table = "Submenus"


class Dishes(models.Model):
    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=250)
    description = fields.TextField()
    price = fields.FloatField()
    submenu = fields.ForeignKeyField(
        "models.Submenus", related_name="dishes_submenu",
        on_delete=fields.CASCADE
    )

    class Meta:
        table = "Dishes"


Menu_Pydantic = pydantic_model_creator(Menus)
MenuIn_Pydantic = pydantic_model_creator(Menus, exclude_readonly=True)

# Submenu_Pydantic = pydantic_model_creator(Submenus)
# SubmenuIn_Pydantic = pydantic_model_creator(Submenus, exclude_readonly=True)

# Dish_Pydantic = pydantic_model_creator(Dishes)
# DishIn_Pydantic = pydantic_model_creator(Dishes, exclude_readonly=True)
