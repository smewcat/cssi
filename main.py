import jinja2
import webapp2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

<<<<<<< HEAD
=======

>>>>>>> 7aa7385295ce0d83f8acfd1588b1b29d24f2b483
#from google.appengine.api import users - for Gmail login
env=jinja2.Environment(loader=jinja2.FileSystemLoader(''))

# This function creates a login for the user.  It will be displayed in every page
def gmail_login(self):
    user = users.get_current_user()
    if user:
                greeting = ('<a id = "greeting" >Welcome, %s!</a>' % user.nickname()+ ' ' + '<a href="%s">(sign out)</a>' %
                      users.create_logout_url('/'))
    else:
                greeting = ('<a href="%s">Sign in with a Google account</a>' %
                    users.create_login_url('/'))
    self.response.write('<html><body>%s</body></html>' % greeting)

# This handler will load up the Home Page of the website.  It will recieve the recipe inputs
# from the user.
class HomePage(webapp2.RequestHandler):
    def get(self):
        #This is the code for the Gmail login
        gmail_login(self)
        template = env.get_template('templates/ingredentry.html')
        #This code is for recipes to display after confirmation page
        self.response.write(template.render())

# This handler will display the search results from the user's input.
# The print statements are for debugging purposes (will be removed)
# The main 'search algorithm' is located in here.
class SearchResults(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        inputted_ingredient = self.request.get("ingredient").lower().replace(" ", "")
        print inputted_ingredient
        query = Recipe.query(Recipe.Ingredients.name == inputted_ingredient)
        recipes = query.fetch()         #now a list of recipe objects
        print recipes
        template = env.get_template('templates/results.html')
        self.response.write(template.render({'recipes' : recipes }))

# This class was created to help the search algorithm understand itself better.
class RecipeIngredient(ndb.Model):
    name = ndb.StringProperty()

# This creates an object of recipe input
class Recipe(ndb.Model): #this is the recipe
    Title = ndb.StringProperty()
    Ingredients = ndb.StructuredProperty(RecipeIngredient, repeated=True)   # This is a class within a class
    Description = ndb.StringProperty()
    Date = ndb.DateProperty()
    pic = ndb.BlobProperty()

#This is the handler for the recipeinput
class RecipeInput(webapp2.RequestHandler):
    def get(self):
    #This is the code for the Gmail login
            gmail_login(self)
            template = env.get_template('templates/userinput.html')
            self.response.write(template.render())

class ConfirmationPage(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        template = env.get_template('templates/recipes.html')
        self.response.write(template.render())

    def post(self):
        gmail_login(self)
        template = env.get_template('templates/recipes.html')
        self.response.write(
            template.render({
            'Title':self.request.get('Title'),
            'Ingredients': self.request.get('Ingredients'),
            'Description':self.request.get('Description'),
            'pic':self.request.get('pic'),
            }))
        ingredients_string = self.request.get('Ingredients').replace(" ", "").split(",")
        ingredients_list = []
        for ingredient in ingredients_string:
            new_recipe = RecipeIngredient(name=ingredient)
            ingredients_list.append(new_recipe)
        recipe = Recipe( #putting parameters in recipe object
            Title=self.request.get('Title'),
            Ingredients = ingredients_list,
            Description=self.request.get('Description'),
            Date=datetime.date.today(),
            #pic=self.request.get('pic')
         )
        recipe.put() #this lets you store event into datastore

# It outputs all the recipes that have been stored in the data store.
class UserDatabase(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        template = env.get_template('templates/database.html')
        #This code is for recipes to display after confirmation page
        query = Recipe.query(Recipe.Ingredients.name == self.request.get("search"))
        recipes = query.fetch() #now a list of recipe objects
        self.response.write(template.render({'recipes' : recipes}))

# This handler will create a template for the different recipes. It displays the
# name of the recipe, the ingredients, and the procedures.

class FoodResultsPageHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/recipetemplate.html')
        page_stuff = {
        'recipe_name' : self.request.get('recipe_name'),
        'ingredients' : self.request.get('ingredients'),
        'procedure' : self.request.get('procedure') }
        self.response.write(template.render(page_stuff))
        recipe_page_template = RecipePageTemplate(
            recipe_name = self.request.get('recipe_name'),
            ingredients = self.request.get('ingredients'),
            procedure = self.request.get('procedure'),
        )
        recipe_page_template.put() # This makes it remember the date for a long time


class UserRecipePage(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        template = env.get_template('templates/recipetemplate.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/results', SearchResults),
    ('/recipeinput', RecipeInput),
    ('/confirmation', ConfirmationPage),
    ('/database', UserDatabase),
    ('/recipe', UserRecipePage),
    ('/food', FoodResultsPageHandler)
], debug=True)


#query = Recipe.query(Recipe.Ingredients == search)
