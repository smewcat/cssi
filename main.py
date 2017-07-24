import jinja2
import webapp2
#from google.appengine.api import users - for Gmail login
env=jinja2.Environment(loader=jinja2.FileSystemLoader(''))

# This handler will load up the Home Page of the website.  It will recieve the recipe inputs
# from the user.
class HomePage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/ingredentry.html')
        self.response.write(template.render())

# This handler will display the search results from the user's input.
class SearchResults(webapp2.RequestHandler):
    def get(self):
        # This dictionary will store the ingredients as keys and the recipies that one
        # could make as values.
        ingredients_dict = {
            "eggs" : ["cake", "hard-boiled egg", "ultimate breakfast"],
            "milk" : ["milkshake", "waffles/pancake", "cereal"],
            "lettuce" : ["salad", "taco", "burger"],
            "bread" : ["Peanut Butter & Jelly Sandwich", "Sub", "Pizza"],
            "chicken" : ["Roast Chicken", "Chicken Soup", "BBQ"],
        }
        inputted_ingredient = self.request.get("ingredient").lower()
        template = env.get_template('templates/results.html')
        ingredient_stuff = { "ingredient_stuffA" : ingredients_dict[inputted_ingredient],
                            "given_thing" : self.request.get("ingredient"),
                            "recipe1" : ingredients_dict[inputted_ingredient][0],
                            "recipe2" : ingredients_dict[inputted_ingredient][1],
                            "recipe3" : ingredients_dict[inputted_ingredient][2]}
        self.response.write(template.render(ingredient_stuff))

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

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/results', SearchResults),
    ('/recipeinput', RecipeInput)
], debug=True)
