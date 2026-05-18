from flask import Flask, render_template, abort

app = Flask(__name__)

# --- Sample Recipe Data ---
# This is a simple Python dictionary. You can easily add, edit, or
# remove recipes here. For a bigger app, you'd use a database.
RECIPES = {
    'burger-buns': {
        'name': 'Burger Buns',
        'id': 'burger-buns',
        'description': 'Soft, bakery-quality burger buns perfect for any burger.',
        'image_url': '/static/images/burger_bun.jpg',
        'image_placeholder': 'https://via.placeholder.com/800x600.png?text=Burger+Buns',
        'default_servings': 6,
        'ingredients': [
            {'quantity': 300, 'unit': 'g', 'name': 'Bread flour'},
            {'quantity': 160, 'unit': 'ml', 'name': 'Warm water or milk. If using milk powder, 20g milk + 140g water'},
            {'quantity': 5, 'unit': 'g', 'name': 'Instant Yeast'},
            {'quantity': 20, 'unit': 'g', 'name': 'Sugar'},
            {'quantity': 6, 'unit': 'g', 'name': 'Salt'},
            {'quantity': 30, 'unit': 'g', 'name': 'Unsalted butter (softened)'},
            {'quantity': 1, 'unit': 'large', 'name': 'Egg'},
            {'quantity': 1, 'unit': 'tbsp', 'name': 'Sesame seeds (optional)'}
        ],
        'instructions': [
            'Mix and Activate the Yeast: Whisk the egg, add half to a large bowl and save the rest in the fridge for the egg wash. Add warm milk, yeast, and sugar.',
            'Knead the Dough: Add flour and salt to the wet mixture and stir until a shaggy dough forms. Add softened butter and knead for 8-10 minutes until smooth, elastic, and slightly tacky.',
            'First Rise: Shape into a smooth ball, place in a lightly oiled bowl, cover, and let rise for 1 to 1.5 hours until doubled in size.',
            'Shape the Buns: Deflate dough and divide into 6 equal pieces (85g-90g each). Shape into tight balls, place on a lined baking sheet, and press down slightly to flatten.',
            'Second Rise: Cover loosely and let rise for 45 to 60 minutes until puffy. Preheat oven to 190°C (375°F) during the last 15 minutes of this rise.',
            'Bake: Mix the reserved egg with 1 tsp water and gently brush the tops of the buns. Sprinkle with sesame seeds if desired.',
            'Bake for 15 to 18 minutes until golden brown. Cool on a wire rack. (Tip: Brush with melted butter immediately after baking for a glossy, soft crust).'
        ]
    },
    'italian-bread':{
        'name': 'Italian Bread',
        'id': 'italian-bread',
        'description': 'A classic Italian bread with a crispy crust and soft interior.',
        'image_url': '/static/images/italian-bread.png',
        'image_placeholder': 'https://via.placeholder.com/800x600.png?text=Italian+Bread',
        'default_servings': 1,
        'ingredients': [
            {'quantity': 320, 'unit': 'g', 'name': 'Water'},
            {'quantity': 8, 'unit': 'g', 'name': 'Salt'},
            {'quantity': 2, 'unit': 'tsp', 'name': 'Instant yeast'},
            {'quantity': 420, 'unit': 'g', 'name': 'All-purpose flour'},
        ],
        'instructions': [
            'Mix the ingredients together and rest for 30 mins (autolyse).',
            'Stretch and fold x4 every 30 mins for 2 hours (bulk fermentation).',
            'Rest for 30 mins and bake. No need for shaping, dust the dutch oven with semolina flour and place the dough in the dutch oven.',
            'Bake at 250 degrees for 25 mins covered. 10 mins bake uncovered at 240 degrees.'
        ]
    },
    'sourdough-cacio-e-pepe-boule':{
        'name': 'Sourdough Cacio e Pepe Boule',
        'id': 'sourdough-cacio-e-pepe-boule',
        'description': 'A rustic round loaf with roasted black pepper and parmesan, perfect with butter.',
        'image_url': '/static/images/sourdough-boule.png',
        'image_placeholder': 'https://via.placeholder.com/800x600.png?text=Sourdough+Boule',
        'default_servings': 1,
        'ingredients': [
            {'quantity': 100, 'unit': 'g', 'name': 'Active sourdough starter'},
            {'quantity': 300, 'unit': 'g', 'name': 'Water'},
            {'quantity': 7, 'unit': 'g', 'name': 'Salt'},
            {'quantity': 450, 'unit': 'g', 'name': 'Bread flour'},
            {'quantity': 90, 'unit': 'g', 'name': 'Parmesan cheese (1/4 inch cubes)'},
            {'quantity': 0.5, 'unit': 'tsp', 'name': 'Roasted black pepper (freshly cracked)'}
        ],
        'instructions': [
            'Mix the ingredients together and rest for 30 mins (autolyse).',
            'Stretch and fold x4 every 30 mins for 2 hours (bulk fermentation).',
            'Mix half of the inclusions (black pepper and parmesan) into the dough during 2nd stretch and fold. Mix the rest of the inclusions during 3rd stretch and fold.',
            'Rest for 5 hours (25 degrees) or until bubbles form on top and jiggly.',
            'Preshape using bench scraper, rest for 30 mins uncovered.',
            'Shape into a boule, place in a banneton and rest for 30 mins in the counter, 6 hours in the fridge (cold retardation).',
            'Preheat dutch oven to 250 degrees. 25 mins bake covered. 25 mins bake uncovered at 240 degrees.'
        ]
    },
    'submarine-sauce':{
        'name': 'Submarine Sauce',
        'id': 'submarine-sauce',
        'description': 'A tangy and spicy sauce perfect for submarine sandwiches.',
        'image_url': '/static/images/submarine.jpg',
        'image_placeholder': 'https://via.placeholder.com/800x600.png?text=Submarine+Sauce',
        'default_servings': 1,
        'ingredients': [
            {'quantity': 150, 'unit': 'g', 'name': 'Sunflower oil'},
            {'quantity': 1, 'unit': 'amount', 'name': 'Egg'},
            {'quantity': 1, 'unit': 'amount', 'name': 'Garlic clove'},
            {'quantity': 0.5, 'unit': 'amount', 'name': 'Lemon juice'},
            {'quantity': 0.5, 'unit': 'tsp', 'name': 'Black pepper'},
            {'quantity': 0.5, 'unit': 'tsp', 'name': 'Mustard'},
            {'quantity': 0.5, 'unit': 'tsp', 'name': 'Chilli flakes'},
            {'quantity': 0.25, 'unit': 'tsp', 'name': 'Salt'},
        ],
        'instructions': [
            'Mix using hand blender.'
        ]
    },
    'sourdough-boule':{
        'name': 'Sourdough Boule',
        'id': 'sourdough-boule',
        'description': 'A rustic round loaf with a chewy crust and open crumb, perfect for sandwiches or with butter.',
        'image_url': '/static/images/sourdough-boule.png',
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