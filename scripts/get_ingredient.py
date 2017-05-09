import json
import pprint



master_ingrd_dict = {
'spices' : ['paprika',
            'cayenne pepper',
            'chili powder',
            'curry powder',
            'vanilla extract',
            'vanilla bean',
            'kosher salt',
            'bay leaf',
            'bay leaves',
            'crushed red pepper',
            'ginger',
            'baking powder',
            'baking soda',
            'cinnamon',
            'saffron',
            'mint',
            'tarragon',
            'chives',
            'fennel',
            'parsley',
            'sage',
            'allspice',
            'dill',
            'marjoram',
            'cumin',
            'oregano',
            'thyme',
            'rosemary',
            'basil',
            'tumeric',
            'cardamom',
            'nutmeg',
            'clove',
            'star anise',
            'anise',
            'basil',
            'smoked paprika',
            'garlic powder',
            'onion powder',
            'almond extract',
            'coriander',
            'salt',
            'garlic salt',
            'celery salt',
            'black pepper',
            'peppercorns',
            'white pepper',
            'five spice',
            '5-spice',
            'five spice powder',
            '5-spice powder',
            'cilantro',
            'old bay',
            'mustard powder',
            'pepper flakes',
            'sesame seeds'      ],

'others':[  'worcestershire sauce',
            'soy sauce',
            'cocoa powder',
            'chocolate chip',
            'light soy sauce',
            'dark soy sauce',
            'hoisin sauce',
            'corn starch',
            'water',
            'capers',
            'granulated sugar',
            'sugar',
            'brown sugar',
            'molasses',
            "confectioner's sugar",
            'lemon juice',
            'lime juice',
            'lemon zest',
            'lime zest',
            'zest',
            'v-8 juice',
            'white wine',
            'red wine',
            'red wine vinegar',
            'white wine vinegar',
            'white vinegar',
            'vegetable stock',
            'beef stock',
            'chicken stock',
            'fish sauce',
            'whole grain mustard',
            'mustard',
            'ketchup',
            'dijon mustard',
            'honey',
            'agave',
            'mayonnaise',
            'beer',
            'whiskey',
            'cognac',
            'teriyaki sauce',
            'brandy',
            'vodka',
            'espresso',
            'sherry'            ],
            

'oils':[    'sunflower oil',
            'peanut oil',
            'palm oil',
            'cottonseed oil',
            'olive oil',
            'extra virgin olive oil',
            'coconut oil',
            'canola oil',
            'corn oil'
            'sesame oil',
            'soybean oil',
            'vegetable oil',
            'rapeseed oil',
            'lard',
            'vegetable shortening',
            'shortening',
            'suet',             
            'fat'               ],

'milk':[   'salted butter',
            'unsalted butter',
            'butter',
            'margarine',
            'buttermilk',
            'condensed milk'
            'custard',
            'dulce de leche',
            'evaporated milk',
            'frozen yogurt',
            'whole milk',
            'skim milk',
            'reduced fat milk',
            'whey'              ],

'cream':[   'sour cream',
            'clotted cream',
            'cream',
            'heavy cream',
            'whipped cream',
            'creme fraiche',
            'ice cream'         ],

'yogurt':[  'yogurt',
            'greek yogurt',
            'plain yogurt'      ],

'cheese':[  'cheddar cheese',
            'cream cheese',
            'goat cheese',
            'feta',
            'brie',
            'ricotta cheese',
            'jalapeno jack',
            'cream cheese',
            'cottage cheese',
            'mozzarella',
            'parmigiano-reggiano',
            'blue cheese',
            'gouda cheese',
            'american cheese',
            'camembert',
            'roquefort',
            'provolone',
            'gruyere cheese',
            'monterey jack',
            'stilton cheese',
            'gorgonzola',
            'emmental cheese',
            'ricotta',
            'swiss cheese',
            'colby cheese',
            'parmesan cheese',
            'muenster cheese',
            'pecorino',
            'manchego',
            'edam',
            'halloumi',
            'havarti',
            'pecorino romano',
            'comte cheese',
            'grana',
            'asiago cheese'
            'pepper jack cheese'
            'mascarpone',
            'limburger',
            'American Cheese',
            'processed cheese'      ],

'potatoes':['potato',
            'sweet potato',
            'taro',
            'yam'
            'idaho potato',
            'russet potato',
            'yukon gold',
            'fingerlings'       ],

'rice':[   'brown rice',
            'white rice',
            'basmati',
            'wild rice',
            'jasmine rice',
            'glutinous rice'    ],

'breads':[ 'barley',
            'millet',
            'buckwheat',
            'corn',
            'oats',
            'steel-cut oats',
            'rolled oats',
            'instant oats',
            'quinoa',
            'rye',
            'granola',
            'all-purpose flour',
            'semolina',
            'whole-wheat flour',
            'enriched flour',
            'cake flour',
            'self-rising flour',
            'sourdough',
            'white bread',
            'rye bread',
            'pita',
            'baguette',
            'focaccia',
            'naan',
            'banana bread',
            'bagel',
            'pumpernickel',
            'challah',
            'croissant',
            'english muffin',
            'raisin bread',
            'garlic bread',
            'biscuit',
            'bun',
            'hot dog bun',
            'hamburger bun'     ],

'pastas':[  'angel hair',
            'linguine',
            'fettuccine',
            'orecchiette',
            'orzo',
            'rigatoni',
            'spaghetti',
            'gnocchi',
            'fusilli',
            'farfalle',
            'penne'
            'tortellini',
            'rotelle',
            'lasagne',
            'vermicelli',
            'ramen',
            'soba',
            'udon',
            'rice vermicelli',
            'noodle'            ],

'shrooms':[ 'shittake',
            'morel',
            'enokitake',
            'oyster mushroom',
            'white mushroom',
            'white button',
            'portobello'        ],

'fruits':[  "apple",
            "pineapple",
            "grapefruit",
            "banana",
            "orange",
            'blueberry',
            "strawberry",
            "grape",
            'raisin',
            'cranberry',
            "lemon",
            "cherry",
            "pear",
            "mango",
            "avocado",
            "peach",
            "melon",
            "apricot",
            "plum",
            "kiwi",
            'watermelon',
            'blackberry',
            'papaya',
            'cantaloupe',
            'berry',
            'tangerine',
            'coconut',
            'cranberry',
            'lychee',
            'date',
            'passion fruit'
            'gooseberry',
            'persimmon',
            'lime',
            "nectarine",
            "fig",
            "pomegranate"   ],

'greens':[  'spinach',
            'kale',
            'cabbage',
            'broccoli',
            'dandelion',
            'leafy green',
            'chard',
            'lettuce',
            'rapini',
            'endive',
            'napa cabbage',
            'cauliflower',
            'tomato',
            'squash',
            'cucumber',
            'bell pepper',
            'pumpkin',
            'corn',
            'maize',
            'brussel sprout',
            'artichoke',
            'bell pepper',
            'chili pepper',
            'red pepper',
            'arugula',
            'watercress'
            'butternut squash',
            'eggplant'              
            'diced tomato',
            'crushed tomato',
            'tomato paste',
            'jalapeno',
            'radish',
            'bok choy'              ],
          


'legumes':[ 'bean',
            'soybean',
            'nut',
            'lentil',
            'pea',
            'okra',
            'green bean',
            'kidney bean',
            'navy bean',
            'pinto bean',
            'garbanzo bean',
            'wax bean',
            'mung bean',
            'snow pea',
            'lima pea'
            'alfalfa',
            'clover',
            'snap pea',
            'sugar snap pea',
            'snow pea',
            'peanut butter',
            'almond butter',
            'cashew butter',
            'peanut',
            'almond',
            'walnut',
            'cashew',
            'pecan',
            'pistachio',
            'hazelnut',
            'brazil nut',
            'pine nut',
            'macadamia',
            'chestnut'      ],


'roots':[   'carrot',
            'parsnip',
            'turnip',
            'rutabaga',
            'radish',
            'celery',
            'daikon',
            'kohirabi',
            'scalllion',
            'jicama',
            'horseradish',
            'onion',
            'shallot',
            'vidalia onion',
            'red onion',
            'pearl onion',
            'leek',
            'water chestnut',
            'spring onion',
            'yellow onion',
            'white onion',
            'asparagus',
            'chicory',
            'garlic'        ],


'eggs':[   'egg',
            'chicken egg',
            'duck egg',
            'goose egg',
            'quail egg'     ],

'lamb':[   'lamb',
            'lamb chop',
            'lamb loin chop',
            'lamb rack',
            'rack of lamb',
            'lamb rib',
            'ground lamb',
            'lamb shank',
            'lamb sirloin',
            'boneless lamb leg',
            'bone-in lamb leg'  ],

'pork':[   'pork',
            'pork shoulder',
            'pork butt',
            'pork loin',
            'pork chop',
            'loin chop',
            'sirloin chop',
            'sirloin steak',
            'baby back rib',
            'riblet',
            'rack of pork',
            'pork loin half rib',
            'pork tenderloin',
            'sirloin roast',
            'spare rib',
            'pork sausage',
            'ground pork',
            'bacon',
            'ham'               ],

'beef':[   'beef',
            't-bone steak',
            'strip steak',
            'chuck steak',
            'skirt steak',
            'brisket',
            'flank steak',
            'short loin',
            'flat iron steak',
            'short ribs',
            'rib eye steak',
            'rib steak',
            'round steak',
            'sirloin steak',
            'top sirloin',
            'bottom sirloin',
            'hanger steak',
            'beef tenderloin',
            'ground beef',
            'beef sausage'      ],

'chicken':[ 'chicken',
            'chicken breast',
            'chicken wing',
            'chicken drum',
            'chicken drumstick',
            'chicken thigh',
            'chicken leg',
            'whole chicken',
            'chicken quarter'    ]

}



def edit_distance(str1, str2):
    
    mat = [ [0 for i in range(len(str2) + 1)] for i in range(len(str1) + 1) ]

    for i in range(1, len(str1)+1):
        mat[i][0] = i

    for j in range(1, len(str2)+1):
        mat[0][j] = j

    sub_cost = 0
    for j in range(1, len(str2)+1):
        for i in range(1, len(str1)+1):
            if str1[i-1] == str2[j-1] :
                sub_cost = 0
            else:
                sub_cost = 1
            
            mat[i][j] = min(mat[i-1][j] + 1, mat[i][j-1] + 1, mat[i-1][j-1] + sub_cost)
    #print mat
    return mat[-1][-1]

def word_compare(ingrd_list_rec, ingrd_list_real, match_diff=2):

    list_match = list()
    for word_real in ingrd_list_real:
        for word_rec in ingrd_list_rec:
            if edit_distance(word_rec, word_real) < match_diff:
                list_match.append(word_real)
    """
    for word_real in ingrd_list_real:
        for word_rec in ingrd_list_rec:
            dist = edit_distance(word_rec, word_real)
            list_match.append((word_real, dist))
    
    print list_match
    for word_match in list_match:
        if word_match[1] > 3:
            list_match = list()
            break
    """
    if len(list_match) > 0:
        #print ingrd_list_real
        #print ingrd_list_rec
        #print list_match
        #print
        return list_match
        
    return None
                
def best_match(ingrd_rec, ingr_category):
    
    
    ingrd_list_rec = ingrd_rec.split('(')[0].split(',')[0].split()

    best_match_ingrds = list()
    best_match_list = list()
    best_match_diff = 10000
    match_list = list()

    for ingrd_real in ingr_category:
        ingrd_list_real = ingrd_real.split()

        match_list = word_compare(ingrd_list_rec, ingrd_list_real)

        if match_list != None:
            #print ingrd_rec
            #print ingrd_list_real
            #print match_list
            #print
            match_goodness = abs(len(match_list) - len(ingrd_list_rec))     # Measures how many words match
            if match_goodness < best_match_diff:
                best_match_diff = match_goodness
                best_match_ingrds = [ingrd_real]
                best_match_list = [ingrd_list_real]
            elif (match_goodness == best_match_diff) and (match_goodness < 10000):
                best_match_ingrds.append(ingrd_real)
                best_match_list.append(ingrd_list_real)
            else:
                pass
    
    """
    filtered_match_ingrds = list()
    filtered_match_list = list()
    if (len(best_match_ingrds) > 1):
        print best_match_list
        for i in range(len(best_match_list)):
            accessory_words = list()
            print best_match_list[i]
            for word in best_match_list[i]:
                print match_list
                if word in match_list:
                    continue
                else:
                    accessory_words.append(word)
            
            acc_match_list = word_compare(ingrd_list_rec, accessory_words, 3)
            if acc_match_list != None:
                filtered_match_ingrds.append(best_match_ingrds[i])
                filtered_match_list.append(best_match_list[i])
    """

    #print ingrd_rec
    #print best_match_ingrds
    #print best_match_list
    #print best_match_diff
    #print
    #return best_match_ingrd

    if best_match_ingrds == []:
        return None, None, None
    else:
        return best_match_ingrds, best_match_list, best_match_diff




pp = pprint.PrettyPrinter(indent=4)

with open("recipes.json", "rb") as jfile:
    j = json.load(jfile)

ingrd_dict = dict()
for key, val in j.iteritems():
    ingrd_dict[key] = val['ingredients']



cleaned_recipe = dict()

size = len(ingrd_dict.keys())
i = 0
for key, val in ingrd_dict.iteritems():
    
    print "%d out of %d\n" % (i, size)
    ingredients_match = dict()
    for ingrd in val:

        
        match_ingrds = list()
        match_list = list
        match_goodness = 10000
        category = list()

        cat_best_match_ingrds, cat_best_match_list, cat_best_match_goodness = best_match(ingrd, master_ingrd_dict['spices'])
        #print ingrd
        #print cat_best_match_ingrds, cat_best_match_list, cat_best_match_goodness
        
        for cat, cat_list in master_ingrd_dict.iteritems():        
        # check spices
            cat_best_match_ingrds, cat_best_match_list, cat_best_match_goodness = best_match(ingrd, cat_list)

            if cat_best_match_ingrds != None:
                if cat_best_match_goodness < match_goodness:
                    match_ingrd = [cat_best_match_ingrds]
                    match_list = cat_best_match_list
                    match_goodness = cat_best_match_goodness
                    category = [cat]
                elif (cat_best_match_goodness == match_goodness) and (cat_best_match_goodness < 10000):
                    match_ingrd.append(cat_best_match_ingrds)
                    match_list.append(cat_best_match_list)
                    category.append(cat)
                else:
                    pass

        #print ingrd
        #print match_ingrds
        #print match_list
        #print category
       
        ingredients_match[ingrd] = {    'ingrd_real': match_ingrd,
                                        'category'  : category      }

    cleaned_recipe[key] = ingredients_match

    i+=1

try:
    with open('ingrdients_extract.json', 'wb') as jwrite:
        json.dump(cleaned_recipe, jwrite, sort_keys=True, indent=4) 
except:
    pp.pprint(cleaned_recipe)
        #check poultry
        #for s in spices:
        #    s_list = s.split()
        #    word_compare(ingrd_split, s_list)


            





#pp.pprint(ingrd_dict)


