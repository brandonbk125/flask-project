from flask import Flask, render_template, request
import json
import requests
import os


# Cocktail Class
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


# Takes a dict of drink attributes and returns a cocktail object
def get_cocktail(drink: dict):
    # instantiate a cocktail object
    cocktail = Cocktail()
    cocktail.set_img_url(drink.get("strDrinkThumb"))
    cocktail.set_name(drink.get("strDrink"))
    # filtering out empty values from dictionary
    drink_filtered = {k: v for k, v in drink.items() if v is not None and not ''}
    # making dictionaries for ingredients and ingredient amounts for the drink
    ingredients = {k: v for k, v in drink_filtered.items() if "Ingredient" in k}
    ingredient_amounts = {k: v for k, v in drink_filtered.items() if "Measure" in k}
    # adding the ingredients and amounts to the object
    for i in range(len(ingredients.keys())):
        cocktail.add_ingredient(list(ingredients.items())[i][1])
        cocktail.add_ingredient_amount("")
    for i in range(len(ingredient_amounts.keys())):
        cocktail.set_ingredient_amount(list(ingredient_amounts.items())[i][1], i)
    # return the cocktail object
    return cocktail


# Homepage of the website
@app.route("/")
def home():
    # renders the homepage of the website
    return render_template("home.html")


@app.route("/ingredient/")
def ingredient():
    pass


# Displays a random cocktail from the API
@app.route("/random")
def random_cocktail():
    # API call to return a random cocktail from their database
    url = "http://www.thecocktaildb.com/api/json/v1/1/random.php"
    r = requests.get(url)
    # import data into a dictionary
    data = r.json()
    drink = data["drinks"][0]
    # extract cocktail data into an object
    r_cocktail = get_cocktail(drink)
    # render the cocktail info
    return render_template("random.html", thumburl=r_cocktail.get_img_url(), name=r_cocktail.get_name(),
                           ingredients=r_cocktail.get_ingredients(),
                           ingredient_amounts=r_cocktail.get_ingredient_amounts())


# Displays a list of cocktails beginning with a given letter
@app.route('/browse/<string:letter>')
def list_cocktails(letter: str):
    # API call for the list of cocktails starting with the given letter
    url = "http://www.thecocktaildb.com/api/json/v1/1/search.php?f=" + letter
    r = requests.get(url)
    # import data into a dictionary
    cocktail_dict = r.json()
    drinks_dict = cocktail_dict["drinks"]
    # if dictionary is empty render no_cocktail_found.html
    if drinks_dict is None:
        return render_template("no_cocktail_found.html")
    # else render cocktail list
    else:
        drinks = []
        for drink in drinks_dict:
            drinks.append([drink.get("strDrink"), drink.get("strDrinkThumb")])
        return render_template("cocktail_list.html", drinks=drinks)


# Displays a cocktail based on user search (or tells them that nothing can be found)
@app.route('/search', methods=["GET", "POST"])
def search():
    # get the user search from the form
    searched = str(request.form.get("searched"))
    # make the API call using the users search term
    url = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + searched
    r = requests.get(url)
    # import the data into a dictionary
    cocktail_dict = r.json()
    # if the API call returns an empty dict then render no_cocktail_found.html
    if cocktail_dict["drinks"] is None:
        return render_template("no_cocktail_found.html")
    # else render the cocktail info
    else:
        drinks_dict = cocktail_dict["drinks"][0]
        search_cocktail = get_cocktail(drinks_dict)
        return render_template("cocktail.html", thumburl=search_cocktail.get_img_url(), name=search_cocktail.get_name(),
                               ingredients=search_cocktail.get_ingredients(),
                               ingredient_amounts=search_cocktail.get_ingredient_amounts())


# Display a specific cocktail
@app.route('/drink/<string:drink>')
def cocktail(drink: str):
    # API call for a specific cocktail
    url = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s=" + drink
    r = requests.get(url)
    # import the data into a dictionary
    cocktail_dict = r.json()
    drinks_dict = cocktail_dict["drinks"][0]
    # extract cocktail data into an object
    s_cocktail = get_cocktail(drinks_dict)
    # render the cocktail info
    return render_template("cocktail.html", thumburl=s_cocktail.get_img_url(), name=s_cocktail.get_name(),
                           ingredients=s_cocktail.get_ingredients(),
                           ingredient_amounts=s_cocktail.get_ingredient_amounts())


if __name__ == '__main__':
    app.run(debug=True)
