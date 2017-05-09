import json
from pprint import pprint


unit_to_gram = {

        "dash"          : 0.0625,
        "dashes"        : 0.0625,
        "pinch"         : 0.125,
        "pinches"       : 0.125,
        "teaspoon"      : 5,
        "teaspoons"     : 5,
        "tsp"           : 5,
        "tablespoon"    : 15,
        "tablespoons"   : 15,
        "tbsp"          : 15,
        "fluid ounce"   : 29.5735296875,
        "fluid ounces"  : 29.5735296875,
        "fl oz"         : 29.5735296875,
        "cup"           : 236.5882375,
        "cups"          : 236.5882375,
        "pint"          : 473.176475,
        "pints"         : 473.176475,
        "quart"         : 946.35295,
        "quarts"        : 946.35295,
        "gallon"        : 3785.4118,
        "gallons"       : 3785.4118,
        "milliliter"    : 1,
        "milliliters"   : 1,
        "millilitre"    : 1,
        "millilitres"   : 1,
        "deciliter"     : 100,
        "deciliters"    : 100,
        "decilitre"     : 100,
        "decilitres"    : 100,
        "liter"         : 1000,
        "liters"        : 1000,
        "litre"         : 1000,
        "litres"        : 1000,
        "pound"         : 453.59237,
        "pounds"        : 453.59237,
        "lb"            : 453.59237,
        "lbs"           : 453.59237,
        "ounce"         : 28.349523125,
        "ounces"        : 28.349523125,
        "oz"            : 28.349523125,
        "oz."           : 28.349523125,
        "milligram"     : 0.001,
        "milligrams"    : 0.001,
        "gram"          : 1,
        "grams"         : 1,
        "g"             : 1,
        "kilogram"      : 1000,
        "kg"            : 1000
}

eng_to_num = {
        "one"           : 1,
        "two"           : 2,
        "three"         : 3,
        "four"          : 4,
        "five"          : 5,
        "six"           : 6,
        "seven"         : 7,
        "eight"         : 8,
        "nine"          : 9,
        "ten"           : 10,
        "eleven"        : 11,
        "twelve"        : 12,
        "thirteen"      : 13,
        "fourteen"      : 14,
        "fifteen"       : 15,
        "sixteen"       : 16,
        "seventeen"     : 17,
        "eighteen"      : 18,
        "nineteen"      : 19,
        "twenty"        : 20,
        "twenty four"   : 24,
        "twenty-four"   : 24,
        "half"          : 0.5,
        "third"         : 0.33,
        "quarter"       : 0.25,
        "few"           : 3

}

def calculate_with_unit(str_list):

    unit_idx = 0
    unit = 0.0
    amt_by_unit = 0.0
    for i in range(len(str_list)):
        #Want to strip away end parens
        if (')' in str_list[i][-1]) or ('.' in str_list[i][-1]):
            str_list[i] = str_list[i][: len(str_list[i]) - 1]
        #Sometimes recipes calls units of fixed amounts, like 2 6-ounce cans
        #Since this is a special case, we calculate the amount here, and
        #continue to the next ingredient
        if ("-" in str_list[i]) and (len(str_list[i]) > 1):
            #print str_list[i]
            fixed_unit = str_list[i].split('-')
            #print fixed_unit
            if (str(fixed_unit[1]) in unit_to_gram):
                unit = float(unit_to_gram[fixed_unit[1]])
                if (str(fixed_unit[0]).isdigit()):
                    amt_by_unit = float(fixed_unit[0])
                elif '.' in fixed_unit[0]:
                    float_amt = fixed_unit[0].split('.')
                    if str(float_amt[0]).isdigit() and str(float_amt[1]).isdigit():
                        unit = float(unit_to_gram[fixed_unit[1]])
                elif '/' in fixed_unit[0]:
                    frac_mul = fixed_unit[0].split('/')
                    #print frac_mul
                    if str(frac_mul[0]).isdigit() and str(frac_mul[1]).isdigit():
                        amt_by_unit *= float(frac_mul[0]) / float(frac_mul[1])
                else:
                    pass
                if i >= 1:
                    multiplier = str_list[i - 1]
                    #print multiplier
                    if (multiplier in eng_to_num) and str(multiplier).isdigit():
                        amt_by_unit *= float(multiplier)
                    elif '/' in multiplier:
                        frac_mul = multiplier.split('/')
                        #print frac_mul
                        if str(frac_mul[0]).isdigit() and str(frac_mul[1]).isdigit():
                            amt_by_unit *= float(frac_mul[0]) / float(frac_mul[1])
                    else:
                        pass

                    amount = amt_by_unit * unit
                    return amount, unit_idx


        if str_list[i] in unit_to_gram:
            unit = unit_to_gram[str_list[i]]
            unit_idx = i
            break

    if (unit_idx - 1) >= 0:
        #print str_list[unit_idx - 1]
        if (str(str_list[unit_idx - 1]) in eng_to_num):
            amt_by_unit = eng_to_num[str_list[unit_idx - 1]]

        #elif the string before the unit is a fraction
        elif ("/" in str_list[unit_idx - 1]):
            frac_str = str_list[unit_idx - 1].split('/')
            #Check if the previous string is actually a fraction
            if str(frac_str[0]).isdigit() and str(frac_str[1]).isdigit():
                amt_by_unit += float(frac_str[0]) / float(frac_str[1])
                #Checking if there is a whole number before the fraction. If so, 
                #it's a whole number by fraction notation
                if (unit_idx - 2) >= 0:
                    if (str(str_list[unit_idx - 2]).isdigit()):
                        amt_by_unit += float(str_list[unit_idx - 2])
            # Occasionally, recipe gives amount equivalent amounts in two different 
            #units, split by a single slash
            elif str(frac_str[1].isdigit()):
                amt_by_unit = float(frac_str[1])

            #If previous string not a fraction, then the string is bogus and we skip
            else:
                pass
        
        #elif the string before the unit is a range x-y, where x, y are positive integers
        elif ("-" in str_list[unit_idx - 1]):
            range_str = str_list[unit_idx - 1].split('-')
            if str(range_str[0]).isdigit() and str(range_str[1]).isdigit():
                amt_by_unit = (float(range_str[0]) + float(range_str[1])) / 2.0

        elif (str(str_list[unit_idx - 1]).isdigit()):
            amt_by_unit = float(str_list[unit_idx - 1])

        else:   #Then we don't know what to do
            pass

    amount = amt_by_unit * unit
    #return amount, unit_idx
    return amount # number of grams
"""

units = unit_to_gram.keys()
#print units

ingrd = dict()

with open('recipes.json', 'rb') as jfile:
    j = json.load(jfile)

for key, val in j.iteritems():
    ingrd[key] = val['ingredients']

for key, val in ingrd.iteritems():
    for ingr in val:

        # We want to decipher how much of an ingredient is needed in the recipe
        amount = 0
        # We also want to know the ingredient
        ingredient = ""

        # Units of measurement are sometimes in parentheses. If so, the rest
        # of the string only needs to be checked for the ingredient
        paren_split = ingr.split('(')
        if len(paren_split) > 1:
            paren_str = paren_split[1].split()
            #pprint(paren_str)

            #amount, unit_idx = calculate_with_unit(paren_str)
            amount = calculate_with_unit(paren_str)

            if amount == 0.0:
                #amount, unit_idx = calculate_with_unit(paren_split[0].split())
                amount = calculate_with_unit(paren_str)

            #pprint(ingr)
            #pprint(paren_str)
            #pprint(amount)

        else: #The string may have a comma, which includes extraneous info
            #Get the string with ingredient and amount info (left of comma)
            #and break up string into words
            single_str = paren_split[0].split(',')[0].split()
            pprint(single_str)
            #amount, unit_idx = calculate_with_unit(single_str)
            amount = calculate_with_unit(single_str)

        if amount == 0:
            amount = unit_to_gram['cup']

        #print ingr
        print amount

    #pprint(ingrd)
"""
