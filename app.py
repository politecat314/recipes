from flask import Flask, render_template, abort

app = Flask(__name__)

# --- Sample Recipe Data ---
# This is a simple Python dictionary. You can easily add, edit, or
# remove recipes here. For a bigger app, you'd use a database.
RECIPES = {
    'sourdough-boule':{
        'name': 'Sourdough Boule',
        'id': 'sourdough-boule',
        'description': 'A rustic round loaf with a chewy crust and open crumb, perfect for sandwiches or with butter.',
        'image_url': '/static/images/sourdough-boule.jpg',
        'image_placeholder': 'https://via.placeholder.com/800x600.png?text=Sourdough+Boule',
        'default_servings': 1,
        'ingredients': [
            {'quantity': 100, 'unit': 'g', 'name': 'Active sourdough starter'},
            {'quantity': 300, 'unit': 'g', 'name': 'Water'},
            {'quantity': 10, 'unit': 'g', 'name': 'Salt'},
            {'quantity': 450, 'unit': 'g', 'name': 'Bread flour'}
        ],
        'instructions': [
            'Mix the ingredients together and rest for 30 mins (autolyse).',
            'Stretch and fold x4 every 30 mins for 2 hours (bulk fermentation).',
            'Rest for 5 hours (25 degrees) or until bubbles form on top and jiggly.',
            'Preshape using bench scraper, rest for 30 mins uncovered.',
            'Shape into a boule, place in a banneton and rest for 30 mins in the counter, 6 hours in the fridge (cold retardation).',
            'Preheat dutch oven to 250 degrees. 25 mins bake covered. 25 mins bake uncovered at 240 degrees.'
        ]
    },
    'garlic-butter':{
        'name': 'Garlic butter',
        'id': 'garlic-butter',
        'description': 'Does it even need an introduction?',
        'image_url': '/static/images/breadsticks.jpg',
        'image_placeholder': 'https://via.placeholder.com/800x600.png?text=Breadsticks',
        'default_servings': 4,
        'ingredients': [
            {'quantity': 2, 'unit': 'tbsp', 'name': 'Butter, melted (30 g)'},
            {'quantity': 0.5, 'unit': 'tbsp', 'name': 'Minced fresh parsley (about 4 g)'},
            {'quantity': 0.5, 'unit': 'tsp', 'name': 'Garlic powder'},
            {'quantity': 0.5, 'unit': 'tsp', 'name': 'Chili flakes (optional)'},
            {'quantity': 0.5, 'unit': 'tsp', 'name': 'Parmesan cheese (optional)'}
        ],
        'instructions': [
            'Ask Annisa'
        ]
    },
    'breadsticks':{
        'name': 'Breadsticks (6 Pcs)',
        'id': 'breadsticks',
        'description': 'Soft breadsticks to be enjoyed with sausages or garlic butter',
        'image_url': '/static/images/breadsticks.jpg',
        'image_placeholder': 'https://via.placeholder.com/800x600.png?text=Breadsticks',
        'default_servings': 4,
        'ingredients': [
            {'quantity': 120, 'unit': 'ml', 'name': 'Warm water'},
            {'quantity': 1, 'unit': 'tbsp', 'name': 'Honey (21 g)'},
            {'quantity': 1.125, 'unit': 'tsp', 'name': 'Active dry yeast'},
            {'quantity': 2, 'unit': 'tbsp', 'name': 'Unsalted butter, melted and cooled (30 g)'},
            {'quantity': 0.75, 'unit': 'tsp', 'name': 'Kosher salt'},
            {'quantity': 225, 'unit': 'g', 'name': 'All-purpose flour'},
            {'quantity': 0.5, 'unit': 'tbsp', 'name': 'Olive oil, for the bowl (7 ml)'},
            {'quantity': 30, 'unit': 'g', 'name': 'Semolina flour, for dusting'}
        ],
        'instructions': [
            'Ask Annisa',
            'For garnishing, use garlic butter (follow garlic butter recipe on main page)'
        ]
    },
    'sourdough-pizza': {
        'name': 'Sourdough Pizza',
        'id': 'sourdough-pizza',
        'description': 'A delicious neapolitan style pizza made with sourdough crust.',
        'default_servings': 2,
        'image_url': '/static/images/sourdough_pizza.jpg',
        'image_placeholder': 'https://via.placeholder.com/800x600.png?text=Sourdough+Pizza',
        'ingredients': [
            {'quantity': 150, 'unit': 'g', 'name': 'Strong white bread flour'},
            {'quantity': 100, 'unit': 'g', 'name': '00 Pizza flour'},
            {'quantity': 7.5, 'unit': 'g', 'name': 'Fine sea salt'},
            {'quantity': 3, 'unit': 'g', 'name': 'Sugar'},
            {'quantity': 155, 'unit': 'g', 'name': 'Water'},
            {'quantity': 40, 'unit': 'g', 'name': 'Active sourdough starter'},
            {'quantity': 5, 'unit': 'g', 'name': 'Extra virgin olive oil'}
        ],
        'instructions': [
            'Mix the dry ingredients together.',
            'Mix water and sourdough starter in a separate bowl until dissolved.',
            'Mix dry and wet ingredients until combined. Add olive oil and knead until you get a shaggy dough.',
            'Rest for 30 mins (autolyse).',
            'Take dough onto the bench. Stretch away from you and fold inside a couple of times.',
            'Bring the dough towards you a couple of times to tighten the dough ball.',
            'Add dough ball to a bowl covered in olive oil and cover. Rest for 4 hours (bulk fermentation).',
            'Divide into dough balls. Fold invards from 4 ways, filp and tighten the dough ball.',
            'Place dough balls on a tray, cover and rest for 4 hours (final proof).',
            'Place dough balls in the fridge, rest for 12-24 hours.',
            'Take the dough balls out, let rest for 1.5-2 hours (to come to room temp.) before baking.'
        ]
    },
    'sourdough-pancakes': {
        'name': 'Sourdough Pancakes',
        'id': 'sourdough-pancakes',
        'description': 'Fluffy, tangy pancakes made with sourdough starter discard.',
        'default_servings': 2,  # This makes about 6-8 small pancakes
        'image_url': '/static/images/sourdough_pancakes.jpg',
        'image_placeholder': 'https://via.placeholder.com/800x600.png?text=Pancakes',
        'ingredients': [
            {'quantity': 120, 'unit': 'g', 'name': 'Self-Raising Flour / All Purpose Flour'},
            {'quantity': 1, 'unit': 'tsp', 'name': 'Baking Powder (if all purpose flour is used)'},
            {'quantity': 1, 'unit': 'tbsp', 'name': 'Sugar'},
            {'quantity': 0.25, 'unit': 'tsp', 'name': 'Baking Soda'},
            {'quantity': 0.4, 'unit': 'tsp', 'name': 'Salt'},
            {'quantity': 120, 'unit': 'g', 'name': 'Sourdough Starter Discard'},
            {'quantity': 0.5, 'unit': 'cups', 'name': 'Milk'},
            {'quantity': 28, 'unit': 'g', 'name': 'Melted Butter'},
            {'quantity': 1, 'unit': 'large', 'name': 'Egg'}
        ],
        'instructions': [
            'Mix the dry ingredients together.',
            'Mix wet ingredients in a separate bowl.',
            'Add wet ingredients to dry ingredients and stir until combined.',
            'Make pancakes at medium heat.'
        ]
    }
}
# --- End of Recipe Data ---


@app.route('/')
def index():
    """Homepage: Displays a list of all recipes."""
    return render_template('index.html', recipes=RECIPES)


@app.route('/recipe/<string:recipe_id>')
def recipe_detail(recipe_id):
    """Recipe Detail Page: Shows a single recipe."""
    recipe = RECIPES.get(recipe_id)
    
    if not recipe:
        abort(404)  # Not found
        
    return render_template('recipe.html', recipe=recipe)


if __name__ == '__main__':
    app.run(debug=True)