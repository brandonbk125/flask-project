from flask import Flask, render_template
import json
import requests
import os


class Cocktail:
    def __init__(self):
        self._name = ""
        self._img_url = ""
        self._ingredients = []
        self._ingredient_amounts = []

    def set_name(self, name: str):
        self._name = name

    def get_name(self):
        return self._name

    def set_img_url(self, img_url: str):
        self._img_url = img_url

    def get_img_url(self):
        return self._img_url

    def add_ingredient(self, ingredient: str):
        self._ingredients.append(ingredient)

    def get_ingredients(self):
        return self._ingredients

    def add_ingredient_amount(self, amount: str):
        self._ingredient_amounts.append(amount)

    def set_ingredient_amount(self, amount: str, index: int):
        if index > len(self._ingredient_amounts)-1:
            self._ingredient_amounts.append(amount)
        else:
            self._ingredient_amounts[index] = amount

    def get_ingredient_amounts(self):
        return self._ingredient_amounts


app = Flask(__name__)


@app.route("/")
def home():
    url = "http://www.thecocktaildb.com/api/json/v1/1/random.php"

    r = requests.get(url)
    data = r.json()
    drink = data["drinks"][0]

    cocktail = Cocktail()

    thumburl = drink.get("strDrinkThumb")
    name = drink.get("strDrink")
    print(drink)

    drink_filtered = {k: v for k, v in drink.items() if v is not None and not ''}
    print("------------------filter----------------")
    print(drink_filtered.keys())
    # key: value for k, value in drink.items() if Ingredient in key
    ingredients = {k: v for k, v in drink_filtered.items() if "Ingredient" in k}
    ingredient_amounts = {k: v for k, v in drink_filtered.items() if "Measure" in k}

    for i in range(len(ingredients.keys())):
        cocktail.add_ingredient(list(ingredients.items())[i][1])
        cocktail.add_ingredient_amount("")

    for i in range(len(ingredient_amounts.keys())):
        cocktail.set_ingredient_amount(list(ingredient_amounts.items())[i][1], i)

    print("INGREDIENTS:")
    print(cocktail.get_ingredients())
    print("AMOUNTS: ")
    print(cocktail.get_ingredient_amounts())

    return render_template("home.html", thumburl=thumburl, name=name, ingredients=cocktail.get_ingredients(),
                           ingredient_amounts=cocktail.get_ingredient_amounts())


@app.route("/ingredient/")
def ingredient():
    pass


@app.route('/search/<string:letter>')
def list_cocktails(letter: str):
    pass


if __name__ == '__main__':
    app.run(debug=True)
