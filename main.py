import jinja2
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import ndb

INGREDIENT_TO_RECIPES = {
    "eggs" : ["cake", "hard-boiled egg", "ultimate breakfast"],
    "milk" : ["milkshake", "waffles/pancake", "cereal"],
    "lettuce" : ["salad", "taco", "burger"],
    "bread" : ["Peanut Butter & Jelly Sandwich", "Sub", "Pizza"],
    "chicken" : ["Roast Chicken", "Chicken Soup", "BBQ"],
}

#from google.appengine.api import users - for Gmail login
env=jinja2.Environment(loader=jinja2.FileSystemLoader(''))

# This handler will load up the Home Page of the website.  It will recieve the recipe inputs
# from the user.
class HomePage(webapp2.RequestHandler):
    def get(self):
        #This is the code for the Gmail login
        user = users.get_current_user()
        if user:
                    greeting = ('<a id = "greeting" >Welcome, %s!</a>' % user.nickname()+ ' ' + '<a href="%s">(sign out)</a>' %
                          users.create_logout_url('/'))
        else:
                    greeting = ('<a href="%s">Sign in with a Google account</a>' %
                        users.create_login_url('/'))
        self.response.write('<html><body>%s</body></html>' % greeting)
        template = env.get_template('templates/ingredentry.html')
        self.response.write(template.render())

# This handler will display the search results from the user's input.
class SearchResults(webapp2.RequestHandler):
    def get(self):
        inputted_ingredient = self.request.get("ingredient").lower()
        template = env.get_template('templates/results.html')
        recipe_display_dict = { "ingredient_stuffA" : INGREDIENT_TO_RECIPES[inputted_ingredient],
                            "recipe1" : INGREDIENT_TO_RECIPES[inputted_ingredient][0],
                            "recipe2" : INGREDIENT_TO_RECIPES[inputted_ingredient][1],
                            "recipe3" : INGREDIENT_TO_RECIPES[inputted_ingredient][2]}
        user = users.get_current_user()
        if user:
                    greeting = ('<a id = "greeting" >Welcome, %s!</a>' % user.nickname()+ ' ' + '<a href="%s">(sign out)</a>' %
                          users.create_logout_url('/'))
        else:
                    greeting = ('<a href="%s">Sign in with a Google account</a>' %
                        users.create_login_url('/'))
        self.response.write('<html><body>%s</body></html>' % greeting)
        self.response.write(template.render(recipe_display_dict))

#This is the handler for the recipeinput
class RecipeInput(webapp2.RequestHandler):
    def get(self):
    #This is the code for the Gmail login
            user = users.get_current_user()
            if user:
                greeting = ('<a id = "greeting" >Welcome, %s!</a>' % user.nickname()+ ' ' + '<a href="%s">(sign out)</a>' %
                      users.create_logout_url('/'))
            else:
                greeting = ('<a href="%s">Sign in with a Google account</a>' %
                    users.create_login_url('/'))
            self.response.write('<html><body>%s</body></html>' % greeting)
            template = env.get_template('templates/userinput.html')
            self.response.write(template.render())

# This handler will store the comments and recipes inputted by the users
#class InputAndCommentStore(ndb.Model):
    # THESE ARE EXAMPLES OF RETRIVING DATA FROM THE DATASTORE
    # day = ndb.DateProperty()
    # time = ndb.StringProperty()
    # venue = ndb.StringProperty()
    # occasion = ndb.StringProperty()
    # num_of_people = ndb.StringProperty()

class RecipePage(webapp2.RequestHandler):
    def post(self):
        template = env.get_template('templates/recipes.html')
        self.response.write(
            template.render({
            'Title':self.request.get('Title'),
            'Link': self.request.get('Link'),
            'Description':self.request.get('Description'),
            }))
        recipe = Recipe( #putting parameters in recipe object
            Title=self.request.get('Title'),
            Link=self.request.get('Link'),
            Description=self.request.get('Description')
         )
        recipe.put() #this lets you store event into datastore

class Recipe(ndb.Model): #this is the recipe
    Title = ndb.StringProperty()
    Link = ndb.StringProperty()
    Description = ndb.StringProperty()

class TacoPageHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/taco.html')
        self.response.write(template.render())

class CakePageHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/cake.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/results', SearchResults),
    ('/recipeinput', RecipeInput),
    ('/confirmation', RecipePage)
], debug=True)
