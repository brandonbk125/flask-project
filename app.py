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


# takes a dict of drink attributes and returns a cocktail object
def get_ingredients(drink: dict):
    cocktail = Cocktail()
    cocktail.set_img_url(drink.get("strDrinkThumb"))
    cocktail.set_name(drink.get("strDrink"))
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

    return cocktail




@app.route("/")
def home():
    url = "http://www.thecocktaildb.com/api/json/v1/1/random.php"

    r = requests.get(url)
    data = r.json()
    drink = data["drinks"][0]
    cocktail = get_ingredients(drink)

    print("INGREDIENTS:")
    print(cocktail.get_ingredients())
    print("AMOUNTS: ")
    print(cocktail.get_ingredient_amounts())

    return render_template("home.html", thumburl=cocktail.get_img_url(), name=cocktail.get_name(),
                           ingredients=cocktail.get_ingredients(), ingredient_amounts=cocktail.get_ingredient_amounts())


@app.route("/ingredient/")
def ingredient():
    pass


@app.route('/browse/<string:letter>')
def list_cocktails(letter: str):
    url = "http://www.thecocktaildb.com/api/json/v1/1/search.php?f=" + letter
    r = requests.get(url)
    cocktail_dict = r.json()
    print(cocktail_dict.keys())
    drinks_dict = cocktail_dict["drinks"]
    print(drinks_dict[0])
    drinks = []
    for drink in drinks_dict:
        print(drink.get("strDrink"))
        print(drink.get("strDrinkThumb"))
        drinks.append([drink.get("strDrink"), drink.get("strDrinkThumb")])

    print(drinks)
    return render_template("cocktail_list.html", drinks=drinks)


@app.route('/drink/<string:drink>')
def cocktail(drink: str):
    url = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + drink
    r = requests.get(url)
    cocktail_dict = r.json()
    print(cocktail_dict.keys())
    drinks_dict = cocktail_dict["drinks"][0]
    print(drinks_dict)
    cocktail = get_ingredients(drinks_dict)

    return render_template("cocktail.html", thumburl=cocktail.get_img_url(), name=cocktail.get_name(),
                           ingredients=cocktail.get_ingredients(), ingredient_amounts=cocktail.get_ingredient_amounts())


if __name__ == '__main__':
    app.run(debug=True)
