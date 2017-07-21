import jinja2
import webapp2

env=jinja2.Environment(loader=jinja2.FileSystemLoader(''))

class HomePage(webapp2.RequestHandler):
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

class SearchResults(webapp2.RequestHandler):
 def get(self):


class Food(webapp2.RequestHandler):
 def get(self):

     
    #make sure you have the correct html file name here
    template = env.get_template(' ')
    self.response.write(template.render(ingredients_dict))

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/results', SearchResults),
    ('/food', Food)
], debug=True)
