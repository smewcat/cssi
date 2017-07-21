import jinja2
import webapp2

env=jinja2.Environment(loader=jinja2.FileSystemLoader(''))

# This handler will load up the Home Page of the website.  It will recieve the inputs
# from the user.
class HomePage(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('templates/ingredentry.html')
        self.response.write(template.render())

# This handler will display the search results from the user's input.
class SearchResults(webapp2.RequestHandler):
    def get(self):
        # This dictionary will store the ingredients as keys and the receipies that one
        # could make as values.
        ingredients_dict = {
            "eggs" : ["cake", "hard-boiled egg", "ultimate breakfast"],
            "milk" : ["milkshake", "waffles/pancake", "cereal"],
            "lettuce" : ["salad", "taco", "burger"],
            "bread" : ["Peanut Butter & Jelly Sandwich", "Sub", "Pizza"],
            "chicken" : ["Roast Chicken", "Chicken Soup", "BBQ"],
        }

# This handler will display the different ingredients required for the certain
# recipe loaded.
#class Food(webapp2.RequestHandler):
 #def get(self):
    # #make sure you have the correct html file name here
    # template = env.get_template(' ')
    # self.response.write(template.render(ingredients_dict))

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/results', SearchResults),
    #('/food', Food)
], debug=True)
