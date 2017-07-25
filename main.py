import jinja2
import webapp2
import time
from google.appengine.ext import ndb
from google.appengine.api import users

INGREDIENT_TO_RECIPES = {
    "eggs" : ["cake", "hard-boiled egg", "ultimate breakfast", "sunny-side up", "deviled eggs"],
    "milk" : ["milkshake", "waffles/pancake", "cereal", "cheese"],
    "lettuce" : ["salad", "taco", "burger"],
    "bread" : ["peanut butter & jelly sandwich", "sub", "pizza", "bagels", "sandwiches"],
    "chicken" : ["Roast Chicken", "Chicken Soup", "BBQ"],
}

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
        self.response.write(template.render())

# This handler will display the search results from the user's input.
class SearchResults(webapp2.RequestHandler):
    def get(self):
        inputted_ingredient = self.request.get("ingredient").lower()
        template = env.get_template('templates/results.html')
        results_params= { "recipes" : INGREDIENT_TO_RECIPES[inputted_ingredient]}
        gmail_login(self)
        self.response.write(template.render(results_params))

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
        localtime = time.localtime(time.time())
        template = env.get_template('templates/recipes.html')
        self.response.write(
            template.render({
            'Title':self.request.get('Title'),
            'Ingredients': self.request.get('Ingredients'),
            'Description':self.request.get('Description'),
            'Time':self.request.get('localtime')
            }))
        recipe = Recipe( #putting parameters in recipe object
            Title=self.request.get('Title'),
            Ingredients=self.request.get('Ingredients'),
            Description=self.request.get('Description'),
            Time=self.request.get('localtime')
         )
        recipe.put() #this lets you store event into datastore

# This is creates an object of recipe input
class Recipe(ndb.Model): #this is the recipe
    Title = ndb.StringProperty()
    Ingredients = ndb.StringProperty()
    Description = ndb.StringProperty()
    Time = ndb.StringProperty()

# It outputs all the recipes that have been stored in the data store.
class UserDatabase(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        #This code is for recipes to display after confirmation page
        query = Recipe.query()
        query = query.order(Recipe.Title)
        recipes = query.fetch() #now a list of recipe objects
        template = env.get_template('templates/database.html')
        self.response.write(
        template.render({'recipes' : recipes}))

class TacoPageHandler(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        template = env.get_template('templates/taco.html')
        self.response.write(template.render())

class CakePageHandler(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        template = env.get_template('templates/cake.html')
        self.response.write(template.render())

# This handler will create a template for the different recipes. It displays the
# name of the recipe, the ingredients, and the procedures.
class FoodResultsPageHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/recipetemplate.html')   #Need to change the name for the HTML file
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

# This handler will store the comments and recipes inputted by the users in the datastore
class RecipePageTemplate(ndb.Model):
    # NEED TO ADD A WAY TO ACCESS PICTURES FROM THE DATASTORE
    recipe_name = ndb.StringProperty()
    ingredients = ndb.StringProperty()
    procedure = ndb.StringProperty()


app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/results', SearchResults),
    ('/recipeinput', RecipeInput),
    ('/confirmation', ConfirmationPage),
    ('/database', UserDatabase),
    ('/taco', TacoPageHandler),
    ('/cake', CakePageHandler),
    ('/recipe', UserRecipePage),
    ('/food', FoodResultsPageHandler)
], debug=True)


# This handler will store the comments inputted by the users
#class InputAndCommentStore(ndb.Model):
    # THESE ARE EXAMPLES OF RETRIVING DATA FROM THE DATASTORE
    # day = ndb.DateProperty()
    # time = ndb.StringProperty()
    # venue = ndb.StringProperty()
    # occasion = ndb.StringProperty()
    # num_of_people = ndb.StringProperty()
