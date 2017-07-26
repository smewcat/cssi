import jinja2
import webapp2
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users

INGREDIENT_TO_RECIPES = {
    "eggs" : ["The perfect poach", "Omelet", "Mediterranean Egg Salad"],
    "flour" : ["Flour Tortilla Tacos", "Pancakes", "cake"],
    "chicken" : ["Caprese Chicken", "Parmesan Garlic Chicken", "Chicken Soup"],
}

#from google.appengine.api import users - for Gmail login
env=jinja2.Environment(loader=jinja2.FileSystemLoader(''))

# This function creates a login for the user.  It will be displayed on every page
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
        template = env.get_template('templates/recipes.html')
        self.response.write(
            template.render({
            'Title':self.request.get('Title'),
            'Ingredients': self.request.get('Ingredients'),
            'Description':self.request.get('Description'),
            }))
        recipe = Recipe( #putting parameters in recipe object
            Title=self.request.get('Title'),
            Ingredients=self.request.get('Ingredients'),
            Description=self.request.get('Description'),
            Date=datetime.date.today(),
            pic=str(self.request.get('pic'))
         )
        recipe.put() #this lets you store event into datastore

# This is creates an object of recipe input
class Recipe(ndb.Model): #this is the recipe
    Title = ndb.StringProperty()
    Ingredients = ndb.StringProperty()
    Description = ndb.StringProperty()
    Date = ndb.DateProperty()
    pic = ndb.BlobProperty()

# It outputs all the recipes that have been stored in the data store.
class UserDatabase(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        #This code is for recipes to display after confirmation page
        query = Recipe.query()
        recipes = query.fetch() #now a list of recipe objects
        template = env.get_template('templates/database.html')
        self.response.write(
        template.render({'recipes' : recipes}))

class Poach(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        name = "The Perfect Poach"

        ingredients = [{'ing': '1 cup distilled white vinegar'},
        {'ing':'2 large eggs'},
        {'ing':'Coarse sea salt (such as Maldon)'},
        {'ing':'freshly ground black pepper'}]

        images = [{'img': 'resources/poach1.jpg'},
        {'img': 'resources/poach2.jpg'},
        {'img': 'resources/poach3.jpg'}]

        recipes = [{'recipe_step': 'Pour 1/2 cup vinegar into each of 2 small bowls.'},
        {'recipe_step': 'Crack 1 egg into each bowl, taking care not to break yolk; let stand for 5 minutes.'},
        {'recipe_step':'bring a medium saucepan of water to a boil over medium-high heat.'},
        {'recipe_step':'Using a whisk, vigorously swirl water until a vortex forms in the center.'},
        {'recipe_step': 'Slip 1 egg with vinegar into vortex and continue to swirl water with whisk around edges of pan until it returns to a boil. The egg white should wrap tightly around the yolk, forming an oval shape.'},
        {'recipe_step': 'As soon as water returns to a boil, reduce heat to medium and gently simmer egg, frequently swirling water, for 2 minutes.'},
        {'recipe_step': 'Using a slotted spoon, lift egg from water and use kitchen shears to trim any stray pieces of egg white.'},
        {'recipe_step': 'Place egg on paper towels and gently blot; transfer egg to a bowl or plate. Repeat with remaining egg.'},
        {'recipe_step':'Season with salt and pepper.'}]

        link = "http://www.bonappetit.com/recipe/the-perfect-poach"
        linkName = "Bon Appetit"
        template = env.get_template('templates/recipe.html')
        variables = {'name': name, 'ingredients':ingredients, 'recipes': recipes, 'link':link, 'images':images, 'linkName': linkName}
        self.response.write(template.render(variables))

class Omelet(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        name = "Omelet with Bacon, Mushrooms, and Ricotta"

        ingredients = [{'ing': '3 slices thick-cut bacon'},
        {'ing':'4 ounces button mushrooms'},
        {'ing':'Kosher salt, freshly ground pepper'},
        {'ing':'4 ounces fresh ricotta or cream cheese (about 1/2 cup)'},
        {'ing':'1/4 ounce Parmesan, finely grated (about 1/4 cup)'},
        {'ing':'6 large eggs'}]

        images = [{'img': 'resources/omelet1.jpg'},
        {'img': 'resources/omelet2.jpg'},
        {'img': 'resources/omelet3.jpg'}]

        recipes = [{'recipe_step': 'Cut bacon crosswise into 1/2 inch-wide pieces.'},
        {'recipe_step':'Cook in a large nonstick skillet over medium, stirring and turning occasionally, until starting to brown and crisp but not all of the fat is rendered, 6 to 8 minutes.'},
        {'recipe_step':'Transfer to a small plate or bowl with a slotted spoon.'},
        {'recipe_step':'While the bacon is cooking, finely chop the mushrooms.'},
        {'recipe_step': 'Add mushrooms to skillet with bacon drippings, season with salt and pepper, and increase heat to medium-high.'},
        {'recipe_step': 'Cook, tossing often, until browned and any liquid from mushrooms has cooked off, about 5 minutes.'},
        {'recipe_step': 'Use a slotted spoon to transfer to a small bowl; let skillet cool slightly.'},
        {'recipe_step': 'Add ricotta and Parmesan to mushrooms and stir well to combine; season with salt and pepper.'},
        {'recipe_step':'Whisk eggs in a medium bowl until very smooth and a little frothy, about 1 minute; season with salt and pepper.'},
        {'recipe_step':'Cook eggs in reserved skillet over medium, stirring constantly and making sure to scrape up eggs from bottom and around edge of pan, until large folded curds form.'},
        {'recipe_step':'Shake pan to distribute uncooked eggs over surface and spoon mushroom mixture slightly off center.'},
        {'recipe_step':'Top with bacon and cook until bottom of omelet takes on a light golden-brown color but surface is still slightly wet.'},
        {'recipe_step': 'Fold one side of omelet over filling (like a taco); slide omelet onto a cutting board or large plate.'}]

        link = "http://www.bonappetit.com/recipe/omelet-with-bacon-mushrooms-and-ricotta"
        linkName = "Bon Appetit"
        template = env.get_template('templates/recipe.html')
        variables = {'name': name, 'ingredients':ingredients, 'recipes': recipes, 'link':link, 'images':images, 'linkName': linkName}
        self.response.write(template.render(variables))

class EggSalad(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        name = "Mediterranean Egg Salad"

        ingredients = [{'ing': '1/4 cup olive oil'},
        {'ing':'1 tablespoon za\'atar'},
        {'ing':'2 teaspoons fresh lemon juice'},
        {'ing':'4 hard-boiled large eggs, chopped'},
        {'ing':'1/2 cup chopped green olives'},
        {'ing':'2 tablespoons fresh cilantro leaves'},
        {'ing': '2 tablespoons chopped red onion'},
        {'ing': '2 tablespoons toasted pine nuts'},
        {'ing':'Kosher salt and freshly ground black pepper'},
        {'ing': 'Toast'}]

        images = [{'img': 'resources/eggsalad1.jpg'},
        {'img': 'resources/eggsalad2.jpg'},
        {'img': 'resources/eggsalad3.jpg'}]

        recipes = [{'recipe_step': 'Whisk together oil, za\'atar, and lemon juice.'},
        {'recipe_step': 'Toss with eggs, olives, cilantro, onion, and pine nuts.'},
        {'recipe_step':'season with salt and pepper.'},
        {'recipe_step':' Serve on toast.'}]

        link = "http://www.bonappetit.com/recipe/mediterranean-egg-salad"
        linkName = "Bon Appetit"
        template = env.get_template('templates/recipe.html')
        variables = {'name': name, 'ingredients':ingredients, 'recipes': recipes, 'link':link, 'images':images, 'linkName': linkName}
        self.response.write(template.render(variables))


class Taco(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        name = "Tacos"

        ingredients = [{'ing': '3/4 cup peanut oil'},
        {'ing':'12 (6-inch) yellow corn tortillas'},
        {'ing':'Kosher, for seasoning, plus 1 teaspoon for beef'},
        {'ing':'1 medium onion, chopped'},
        {'ing': '16 ounces ground sirloin'},
        {'ing': '2 cloves garlic, minced'},
        {'ing': '2/3 cup low-sodium beef broth'},
        {'ing': '6 ounces panela cheese, crumbled'},
        {'ing': '12 pickled jalapeno slices'},
        {'ing': '1 cup shredded iceberg lettuce (optional)'},
        {'ing': '1 large tomato, seeded and chopped (optional)'},
        {'ing': '1/2 cup fresh cilantro leaves (optional)'}]

        images = [{'img': 'resources/taco.jpg'},
        {'img': 'resources/taco2.jpg'},
        {'img': 'resources/taco3.jpg'}]

        recipes = [{'recipe_step': 'Heat the oven to 250 degrees F.'},
        {'recipe_step': 'Heat peanut oil until it reaches 350 degrees (about 5 minutes), and maintain the temperature.'},
        {'recipe_step':'Create a taco-shaped holder using aluminium foil, and shape 1 tortilla around it to form a taco shape. Put the bottom of the tortilla into the hot oil and fry for 20 seconds.'},
        {'recipe_step':'Lay 1 side of the tortilla down in the hot oil and fry for 30 seconds.'},
        {'recipe_step': 'Flip the tortilla over and fry for an additional 30 seconds. Remove the taco and cool for 30 seconds before removing the mold.'},
        {'recipe_step': 'Sprinkle the hot tortillas with kosher salt. Repeat frying procedure with the remaining tortillas.'},
        {'recipe_step': 'Drain all but 2 tablespoons of peanut oil from the skillet and return to medium heat. Once the oil shimmers, add the onion and cook until softened and lightly browned around the edges, (about 3 to 4 minutes). Add the ground meat, 1 teaspoon salt, and garlic. Cook until browned (about 3 to 4 minutes), stirring occasionally to break up the meat. Add beef broth. Bring to a simmer and cook, uncovered, until sauce is slightly thickened, (2 to 3 minutes).'},
        {'recipe_step': 'Assemble each taco with meat mixture, panela, jalapeno slices, lettuce, tomatoes, and cilantro.'}]

        link = "http://www.foodnetwork.com/recipes/alton-brown/all-american-beef-taco-recipe-2014469"
        linkName = "Food Network"
        template = env.get_template('templates/recipe.html')
        variables = {'name': name, 'ingredients':ingredients, 'recipes': recipes, 'link':link, 'images':images, 'linkName':linkName}
        self.response.write(template.render(variables))

class Pancakes(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        name = "Pancakes"

        ingredients = [{'ing': '1 1/2 cups all-purpose flour'},
        {'ing':'3 1/2 tsps baking powder'},
        {'ing':'1/2 tsp salt'},
        {'ing':'1/4 cup sugar'},
        {'ing': '1 cup sugar '},
        {'ing': '1 1/4 cups whole milk'},
        {'ing': '1 egg'},
        {'ing': '3 tbsp butter melted'}]

        images = [{'img': 'resources/pancakes1.jpg'},
        {'img': 'resources/pancakes2.jpg'},
        {'img': 'resources/pancakes3.jpg'}]

        recipes = [{'recipe_step': 'Melt the butter in microwave for 30 seconds, set aside.'},
        {'recipe_step': 'In a medium bowl, mix together flour, sugar, salt, and baking powder.'},
        {'recipe_step': 'Stir milk and egg together.'},
        {'recipe_step': 'Create a well in the center of the flour mixture.'},
        {'recipe_step': 'Pour the butter and milk mixture into the well.'},
        {'recipe_step': 'Use a wire whisk to stir everything together until just combined. It will be slightly thick and lumpy, but should be well incorporated.'},
        {'recipe_step': 'Allow the batter to rest while heating a lightly oiled skillet or griddle to medium high heat.'},
        {'recipe_step': 'Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake.'},
        {'recipe_step': 'Cook each side for 3-6 minutes, until lightly golden brown.'}]

        link = 'https://www.graceandgoodeats.com/best-ever-pancake-recipe/'
        linkName = "Grace and Good Eats"
        template = env.get_template('templates/recipe.html')
        variables = {'name': name, 'ingredients':ingredients, 'recipes': recipes, 'link':link, 'images': images, 'linkName':linkName}
        self.response.write(template.render(variables))

class Cake(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        name = "Cake"

        ingredients = [{'ing': '1.5 cups sifted cake flour'},
        {'ing':'1.5 tsp. baking powder'},
        {'ing':'1/4 tsp. salt'},
        {'ing':'1/2 cup unsalted butter'},
        {'ing': '1 cup sugar '},
        {'ing': '2 large eggs'},
        {'ing': '1/2 tsp. vanilla extract'},
        {'ing': '1/2 cup whole milk '}]

        images = [{'img': 'resources/cake.jpg'},
        {'img': 'resources/cake2.jpg'},
        {'img': 'resources/cake3.jpg'}]

        recipes = [{'recipe_step': 'Heat the oven to 400 degrees F.'},
        {'recipe_step': 'Lightly coat an 8-inch cake pan with butter and dust with all-purpose flour.'},
        {'recipe_step': 'Sift the cake flour, baking powder, and salt into a large mixing bowl.'},
        {'recipe_step': 'Beat in the butter one heaping 1/4 teaspoonful at a time, using an electric mixer set on low speed, until the mixture resembles coarse sand.'},
        {'recipe_step': 'Beat in the sugar a tablespoon at a time, until the mixture resembles fine damp sand. Beat in the eggs one at a time. Add the vanilla and milk, and beat on medium-high, just until blended. Do not overbeat.'},
        {'recipe_step': 'Pour into the prepared pan and bake until a wooden skewer inserted in the center comes out clean (30 to 35 minutes). Cool cake in the pan on a wire rack for 5 minutes.'},
        {'recipe_step': 'Un-mold and cool completely and ice.'}]

        link = 'http://www.countryliving.com/food-drinks/recipes/a871/basic-vanilla-cake-69/'
        linkName = "Country Living"
        template = env.get_template('templates/recipe.html')
        variables = {'name': name, 'ingredients':ingredients, 'recipes': recipes, 'link':link, 'images': images, 'linkName':linkName}
        self.response.write(template.render(variables))

class Chicken(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        name = "Caprese Chicken"

        ingredients = [{'ing': '1 tbsp. extra-virgin olive oil'},
        {'ing':'1 lb. boneless skinless chicken breasts'},
        {'ing':'kosher salt'},
        {'ing':'Freshly ground black pepper'},
        {'ing': '1/4 c. balsamic vinegar'},
        {'ing': '2 cloves garlic, minced'},
        {'ing': '1 pt. grape tomatoes, halved'},
        {'ing': '2 tbsp. shredded fresh basil'},
        {'ing': '4 slices mozzarella'}]

        images = [{'img': 'resources/chicken1.jpg'},
        {'img': 'resources/chicken2.jpg'},
        {'img': 'resources/chicken3.jpg'}]

        recipes = [{'recipe_step': 'Heat the oven to 400 degrees F.'},
        {'recipe_step': 'Lightly coat an 8-inch cake pan with butter and dust with all-purpose flour.'},
        {'recipe_step': 'Sift the cake flour, baking powder, and salt into a large mixing bowl.'},
        {'recipe_step': 'Beat in the butter one heaping 1/4 teaspoonful at a time, using an electric mixer set on low speed, until the mixture resembles coarse sand.'},
        {'recipe_step': 'Beat in the sugar a tablespoon at a time, until the mixture resembles fine damp sand. Beat in the eggs one at a time. Add the vanilla and milk, and beat on medium-high, just until blended. Do not overbeat.'},
        {'recipe_step': 'Pour into the prepared pan and bake until a wooden skewer inserted in the center comes out clean (30 to 35 minutes). Cool cake in the pan on a wire rack for 5 minutes.'},
        {'recipe_step': 'Un-mold and cool completely and ice.'}]

        link = 'http://www.delish.com/cooking/recipe-ideas/recipes/a47169/caprese-chicken-recipe/'
        linkName = "Delish"
        template = env.get_template('templates/recipe.html')
        variables = {'name': name, 'ingredients':ingredients, 'recipes': recipes, 'link':link, 'images': images, 'linkName':linkName}
        self.response.write(template.render(variables))

class GarlicChicken(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        name = "Parmesan Garlic Chicken"

        ingredients = [{'ing': '2 tablespoons olive oil'},
        {'ing':'1 clove garlic, minced'},
        {'ing':'1 cup dry bread crumbs'},
        {'ing':'2/3 cup grated Parmesan cheese'},
        {'ing': '1 teaspoon dried basil leaves'},
        {'ing': '1/4 teaspoon ground black pepper'},
        {'ing': '6 skinless, boneless chicken breast halves'}]

        images = [{'img': 'resources/pchicken1.jpg'},
        {'img': 'resources/pchicken2.jpg'},
        {'img': 'resources/pchicken3.jpg'}]

        recipes = [{'recipe_step': 'Preheat oven to 350 degrees F (175 degrees C). Lightly grease a 9x13 inch baking dish.'},
        {'recipe_step': 'In a bowl, blend the olive oil and garlic. '},
        {'recipe_step': 'In a separate bowl, mix the bread crumbs, Parmesan cheese, basil, and pepper'},
        {'recipe_step': 'Dip each chicken breast in the oil mixture, then in the bread crumb mixture.'},
        {'recipe_step': 'Arrange the coated chicken breasts in the prepared baking dish, and top with any remaining bread crumb mixture.'},
        {'recipe_step': 'Bake 30 minutes in the preheated oven, or until chicken is no longer pink and juices run clear.'}]

        link = 'http://allrecipes.com/recipe/55860/baked-garlic-parmesan-chicken/'
        linkName = "All Recipes"
        template = env.get_template('templates/recipe.html')
        variables = {'name': name, 'ingredients':ingredients, 'recipes': recipes, 'link':link, 'images': images, 'linkName':linkName}
        self.response.write(template.render(variables))

class Soup(webapp2.RequestHandler):
    def get(self):
        gmail_login(self)
        name = "Chicken Soup"

        ingredients = [{'ing': '1 (3 pound) whole chicken'},
        {'ing':'4 carrots, halved'},
        {'ing':'4 stalks celery, halved'},
        {'ing':'1 large onion, halved'},
        {'ing': 'water to cover'},
        {'ing': 'salt and pepper to taste'},
        {'ing': '1 teaspoon chicken bouillon granules (optional)'}]

        images = [{'img': 'resources/cs1.jpg'},
        {'img': 'resources/cs2.jpg'},
        {'img': 'resources/cs3.jpg'}]

        recipes = [{'recipe_step': 'Put the chicken, carrots, celery and onion in a large soup pot and cover with cold water.'},
        {'recipe_step': 'Heat and simmer, uncovered, until the chicken meat falls off of the bones (skim off foam every so often).'},
        {'recipe_step': 'Take everything out of the pot.'},
        {'recipe_step': 'Strain the broth.'},
        {'recipe_step': 'Pick the meat off of the bones and chop the carrots, celery and onion.'},
        {'recipe_step': 'Season the broth with salt, pepper and chicken bouillon to taste, if desired.'},
        {'recipe_step': 'Return the chicken, carrots, celery and onion to the pot, stir together, and serve.'}]

        link = 'http://allrecipes.com/recipe/8814/homemade-chicken-soup/'
        linkName = "All Recipes"
        template = env.get_template('templates/recipe.html')
        variables = {'name': name, 'ingredients':ingredients, 'recipes': recipes, 'link':link, 'images': images, 'linkName':linkName}
        self.response.write(template.render(variables))

app = webapp2.WSGIApplication([
    ('/', HomePage),
    ('/results', SearchResults),
    ('/recipeinput', RecipeInput),
    ('/confirmation', ConfirmationPage),
    ('/database', UserDatabase),
    ('/The perfect poach', Poach), #DONE
    ('/Omelet', Omelet), #DONE
    ('/Mediterranean Egg Salad', EggSalad), #DONE
    ('/Flour Tortilla Tacos', Taco), #DONE
    ('/Pancakes', Pancakes), #DONE
    ('/cake', Cake), #DONE
    ('/Caprese Chicken', Chicken),
    ('/Parmesan Garlic Chicken', GarlicChicken),
    ('/Chicken Soup', Soup)
], debug=True)
