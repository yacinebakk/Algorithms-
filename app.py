# %%
def login():
    """Ask the user for email and password with validation."""
    while True:
        email = input("Enter your email: ")
        if "@" in email:
            break
        else:
            print("Invalid email. Please include an '@' symbol.")

    while True:
        password = input("Enter your password: ")
        if (
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password)
        ):
            break
        else:
            print("Invalid password. It must contain at least one uppercase letter, one lowercase letter, and one number.")

    print("Login successful!\n")
    return email

# %%
def calculate_macros(height, weight, age, gender, exercise_intensity, goal):
    """Calculate macros based on height, weight, age, gender, exercise
intensity, and goal."""
    # Basic formula for daily caloric needs (Mifflin-St Jeor Equation)
    if gender.lower() == 'male':
        calories = (10 * weight) + (6.25 * height) - (5 * age) + 5  #

    elif gender.lower() == 'female':
        calories = (10 * weight) + (6.25 * height) - (5 * age) - 161
# -161 for female
    else:
        print("Invalid gender input. Assuming male as default.")
        calories = (10 * weight) + (6.25 * height) - (5 * age) + 5

    # Adjust calories based on exercise intensity
    if exercise_intensity.lower() == 'high':
        calories *= 1.55
    elif exercise_intensity.lower() == 'moderate':
        calories *= 1.3
    elif exercise_intensity.lower() == 'low':
        calories *= 1.2

    # Modify calories based on goal
    if goal.lower() == "cut":
        calories *= 0.8  # Reduce calories by 20% for weight loss
    elif goal.lower() == "bulk":
        calories *= 1.2  # Increase calories by 20% for bulking
    elif goal.lower() == "maintain":
        pass  # Keep calories as is for maintenance
    else:
        print("Invalid goal. Assuming maintenance.")

    # Adjust macro percentages (lower protein allocation)
    protein_percentage = 0.25  # Reduced from 0.3 to 0.25
    fat_percentage = 0.25      # Increased from 0.2 to 0.25
    carbs_percentage = 0.5     # Carbs remain the same

    # Calculate macros (grams based on percentage of total calories)
    protein = protein_percentage * calories / 4
    fat = fat_percentage * calories / 9
    carbs = carbs_percentage * calories / 4

    return round(calories), round(protein), round(fat), round(carbs)

# %%
def input_macros():
    """Allow the user to manually input macros and calculate calories."""
    protein = int(input("Enter protein (grams): "))
    fat = int(input("Enter fat (grams): "))
    carbs = int(input("Enter carbs (grams): "))
    calories = (protein * 4) + (fat * 9) + (carbs * 4)
    print(f"Calories calculated from entered macros: {calories}")
    return calories, protein, fat, carbs

# %%
# Original `calculate_macros` function
def calculate_macros(height, weight, age, gender, exercise_intensity, goal):
    """
    Automatically calculate macronutrients based on user input.
    """
    print("Calculating macros...")
    # Basal Metabolic Rate (BMR) calculation
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    elif gender == "female":
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    else:
        raise ValueError("Invalid gender. Please enter 'male' or 'female'.")

    # Adjust BMR based on exercise intensity
    exercise_multipliers = {"low": 1.2, "moderate": 1.55, "high": 1.9}
    bmr *= exercise_multipliers.get(exercise_intensity, 1.2)

    # Adjust calories based on goal
    if goal == "cut":
        calories = bmr - 500
    elif goal == "maintain":
        calories = bmr
    elif goal == "bulk":
        calories = bmr + 500
    else:
        raise ValueError("Invalid goal. Please enter 'cut', 'maintain', or 'bulk'.")

    # Macronutrient distribution
    protein = weight * 2  # 2g protein per kg of body weight
    fat = weight * 0.8    # 0.8g fat per kg of body weight
    carbs = (calories - (protein * 4 + fat * 9)) / 4

    return int(calories), int(protein), int(fat), int(carbs)

# Fridge Scanner Functionality
def scan_fridge(image_path, model_name="facebook/detr-resnet-50"):
    """
    Scan the fridge using an image recognition model to identify items and quantities.
    Args:
        image_path (str): Path to the image of the fridge.
        model_name (str): Hugging Face model to use for object detection.
    Returns:
        dict: Detected items and their approximate quantities.
    """
    if not os.path.exists(image_path):
        print("Image file does not exist.")
        return {}

    # Load the object detection pipeline
    print("Loading model...")
    detector = pipeline("object-detection", model=model_name)

    print("Processing image...")
    results = detector(image_path)

    # Process the results into a dictionary
    fridge_items = {}
    for result in results:
        item_name = result['label']
        fridge_items[item_name] = fridge_items.get(item_name, 0) + 1  # Increment count

    print(f"Detected items: {fridge_items}")
    return fridge_items

# Recipe Matching
def match_recipes(fridge, macros):
    """Find recipes based on closest macro, calories, and ingredient fit."""
    # Example recipes dictionary
    recipes = {
        "Grilled Chicken Salad": {
            "ingredients": {"chicken_breast": 150, "lettuce": 100, "cherry_tomatoes": 50},
            "macros": {"protein": 35, "fat": 10, "carbs": 5},
            "calories": 300,
        },
        "Spaghetti Bolognese": {
            "ingredients": {"spaghetti": 100, "ground_beef": 150, "tomato_sauce": 100},
            "macros": {"protein": 30, "fat": 15, "carbs": 50},
            "calories": 450,
        },
    }

    scored_recipes = []
    for recipe_name, recipe in recipes.items():
        # Calculate missing ingredients
        missing = {
            item: max(0, qty - fridge.get(item, 0))
            for item, qty in recipe["ingredients"].items()
        }
        total_missing = sum(missing.values())

        # Calculate macro difference
        macro_diff = sum(
            abs(macros[key] - recipe["macros"].get(key, 0))
            for key in macros
            if key in recipe["macros"]
        )

        # Calculate calorie difference
        calorie_diff = abs(macros["calories"] - recipe["calories"])

        # Combine scores
        score = macro_diff + total_missing * 10 + calorie_diff * 5
        scored_recipes.append((recipe_name, recipe, macro_diff, total_missing, calorie_diff, score))

    # Sort recipes by score
    return sorted(scored_recipes, key=lambda x: x[-1])

# Main Function
def main():
    """Main function to run the app."""
    email = login()
    mode = input("Do you want to input macros automatically or manually? (auto/manual): ").strip().lower()
    macros = {}

    if mode == 'auto':
        height = float(input("Enter your height (cm): "))
        weight = float(input("Enter your weight (kg): "))
        age = int(input("Enter your age (years): "))
        gender = input("Enter your gender (male/female): ").strip().lower()
        exercise_intensity = input("Enter your exercise intensity (low/moderate/high): ").strip().lower()
        goal = input("Enter your exercise diet goal (cut/maintain/bulk): ").strip().lower()
        macros['calories'], macros['protein'], macros['fat'], macros['carbs'] = calculate_macros(
            height, weight, age, gender, exercise_intensity, goal
        )
    elif mode == 'manual':
        macros['calories'], macros['protein'], macros['fat'], macros['carbs'] = input_macros()
    else:
        print("Invalid choice. Exiting.")
        return

    print("\nYour selected macros:")
    print(f"Calories: {macros['calories']} kcal")
    print(f"Protein: {macros['protein']} g")
    print(f"Fat: {macros['fat']} g")
    print(f"Carbs: {macros['carbs']} g\n")

    # Option to scan fridge
    scan_option = input("Do you want to scan your fridge? (yes/no): ").strip().lower()
    if scan_option == 'yes':
        image_path = input("Enter the path to your fridge image: ").strip()
        fridge = scan_fridge(image_path)
    else:
        print("No fridge scanning selected.")
        return

    # Match recipes
    ranked_recipes = match_recipes(fridge, macros)

    if ranked_recipes:
        print("\nMatching recipes found:")
        for i, (recipe_name, recipe, macro_diff, total_missing, calorie_diff, score) in enumerate(ranked_recipes, 1):
            print(f"{i}. {recipe_name} (Score: {score})")
    else:
        print("No matching recipes found.")


# %%
def add_fridge_items():
    """Input items available in the fridge (item names only, no quantities)."""
    fridge = set() 
    while True:
        item = input("Enter item (or 'done' to finish): ").strip().lower()
        if item == 'done':
            break
        fridge.add(item)
    if fridge:
        print(f"Current fridge items: {fridge}")
    else:
        print("Fridge is currently empty.")
    return fridge


# %%
def quicksort_recipes(recipes):
    """Sort recipes by score using Quicksort."""
    if len(recipes) <= 1:
        return recipes  # Base case: a single item or empty list is already sorted.

    pivot = recipes[0]  # Choose the first recipe as the pivot.
    pivot_score = pivot[5]  # Score is at index 5 of the tuple.

    # Partition recipes into left (lower scores) and right (higher scores).
    left = [recipe for recipe in recipes[1:] if recipe[5] <= pivot_score]
    right = [recipe for recipe in recipes[1:] if recipe[5] > pivot_score]

    # Recursively sort left and right partitions, then combine them.
    return quicksort_recipes(left) + [pivot] + quicksort_recipes(right)


# %%
def match_recipes(fridge, macros):
    """Find recipes based on closest macro, calories, and ingredient fit, sorted using Quicksort."""
    scored_recipes = []
    for recipe_name, recipe in recipes.items():
        # Calculate missing ingredients
        missing = {item: qty for item, qty in recipe["ingredients"].items() if item not in fridge}
        total_missing = sum(missing.values())

        # Calculate macro difference
        macro_diff = round(sum(abs((macros[key])*4/9 - recipe["macros"].get(key, 0)) for key in macros if key in recipe["macros"]))

        # Calculate calorie difference
        calorie_diff = round(abs((macros['calories'])*4/9 - recipe['calories']))

        # Combine scores with adjusted weighting
        score = (calorie_diff * 2) + (macro_diff * 5) + (total_missing * 10)
        scored_recipes.append((recipe_name, recipe, macro_diff, total_missing, calorie_diff, score))

    # Sort recipes using Quicksort
    return quicksort_recipes(scored_recipes)


# %%
def missing_ingredients(recipe_name, recipe, fridge):
    """Identify missing ingredients."""
    # Calculate missing ingredients
    missing = {
        item: qty for item, qty in recipe["ingredients"].items() if item not in fridge
    }

    # Display only item names when listing missing ingredients
    if missing:
        print(f"\nMissing ingredients for {recipe_name}: {', '.join(missing.keys())}")
    else:
        print(f"\nYou have all the ingredients for {recipe_name}!")

    return missing


# %%
def calculate_dist(coord1, coord2):
    """Calculate the distance between two coordinates using the Haversine formula."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  
    return c * r

# %%
def get_coordinates(address, api_key):
    """Convert a real address into latitude and longitude using OpenCage API."""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={'c072a2f26783452c8dd070dc676f0517'}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']
            return location['lat'], location['lng']
        else:
            print("No results found for the given address.")
            return None
    else:
        print("Error:", response.status_code)
        return None

# %%
def find_nearest_supermarkets(user_coordinates, supermarkets, limit=5):
    """
    Find and sort supermarkets by distance from the user's location.
    Return only the top `limit` closest supermarkets.
    """
    distances = []
    for name, details in supermarkets.items():
        distance = calculate_dist(user_coordinates, details["coordinates"])
        distances.append((name, details["address"], distance))
    
    # Sort by distance
    distances.sort(key=lambda x: x[2])
    
    # Return only the closest `limit` supermarkets
    return distances[:limit]


# %%
def main():
    """Main function to run the app."""
    # User login
    email = login()
    
    # Choose macro input method
    mode = input("Do you want to input macros automatically or manually? (auto/manual): ").strip().lower()
    macros = {}

    if mode == 'auto':
        # Automatic macro calculation
        height = float(input("Enter your height (cm): "))
        weight = float(input("Enter your weight (kg): "))
        age = int(input("Enter your age (years): "))
        gender = input("Enter your gender (male/female): ").strip().lower()
        exercise_intensity = input("Enter your exercise intensity (low/moderate/high): ").strip().lower()
        goal = input("Enter your exercise diet goal (cut/maintain/bulk): ").strip().lower()
        macros['calories'], macros['protein'], macros['fat'], macros['carbs'] = calculate_macros(
            height, weight, age, gender, exercise_intensity, goal
        )
    elif mode == 'manual':
        # Manual macro input
        macros['calories'], macros['protein'], macros['fat'], macros['carbs'] = input_macros()
    else:
        print("Invalid choice. Exiting.")
        return

    # Display selected macros
    print("\nYour selected macros:")
    print(f"Calories: {macros['calories']} kcal")
    print(f"Protein: {macros['protein']} g")
    print(f"Fat: {macros['fat']} g")
    print(f"Carbs: {macros['carbs']} g\n")

    # Option to scan fridge or add manually
    scan_option = input("Do you want to scan your fridge or add items manually? (scan/add): ").strip().lower()
    if scan_option == 'scan':
        # Prompt user for file path to fridge image
        image_path = input("Enter the path to your fridge image: ").strip()
        fridge = scan_fridge(image_path)
    elif scan_option == 'add':
        # Add fridge items manually
        fridge = add_fridge_items()
    else:
        print("Invalid choice. Exiting.")
        return

    # Match recipes based on fridge contents and macros
    ranked_recipes = match_recipes(fridge, macros)

    if ranked_recipes:
        print("\nChoose a recipe to proceed:")
        for i, (recipe_name, recipe, macro_diff, total_missing, calorie_diff, score) in enumerate(ranked_recipes, start=1):
            print(f"{i}: {recipe_name} (Score: {score})")

        while True:
            try:
                choice = int(input("Enter the number of the recipe: ")) - 1
                if 0 <= choice < len(ranked_recipes):
                    chosen_recipe_name = ranked_recipes[choice][0]
                    chosen_recipe = ranked_recipes[choice][1]
                    break
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(ranked_recipes)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        missing = missing_ingredients(chosen_recipe_name, chosen_recipe, fridge)
        if missing:
            print(f"\nYou need to buy: {missing}")
        print(f"\nInstructions for {chosen_recipe_name}:")
        print(f"\nIngredients:")
        print(chosen_recipe.get("ingredients"))
        print(chosen_recipe.get("instructions", "No instructions provided."))
    else:
        print("No recipes matched your ingredients and macros.")

    # Find nearest supermarkets based on user address
    api_key = "c072a2f26783452c8dd070dc676f0517"  # OpenCage API key
    user_address = input("Enter your address: ")
    user_coordinates = get_coordinates(user_address, api_key)
    
    if user_coordinates:
        nearest_supermarkets = find_nearest_supermarkets(user_coordinates, supermarkets)
        print(f"\nNearest supermarkets to {user_address}:")
        for name, address, distance in nearest_supermarkets:
            print(f"{name}: {address} ({distance:.2f} km)")
    else:
        print("Unable to fetch coordinates for the provided address.")


# %%
import requests
import math
from transformers import pipeline
import os

recipes = {
    "Grilled Chicken Salad": {
        "ingredients": {"chicken": 150, "lettuce": 100, "tomatoe": 50, "olive oil": 10},
        "macros": {"protein": 35, "fat": 10, "carbs": 5},
        "calories": 300,
        "instructions": (
            "1. Preheat the grill to medium-high heat. \n"
            "2. Season the chicken breast with salt and pepper on both sides. \n"
            "3. Grill the chicken for 5-6 minutes on each side or until the internal temperature reaches 75°C (165°F). \n"
            "4. While the chicken cooks, wash and chop the lettuce and halve the cherry tomatoes. \n"
            "5. Let the grilled chicken rest for 5 minutes, then slice it into strips. \n"
            "6. Arrange the lettuce on a plate, add the cherry tomatoes, and top with the grilled chicken. \n"
            "7. Drizzle olive oil over the salad and serve immediately."
        )
    },
    "Spaghetti Bolognese": {
        "ingredients": {"spaghetti": 100, "ground beef": 150, "tomato sauce": 100},
        "macros": {"protein": 30, "fat": 15, "carbs": 50},
        "calories": 450,
        "instructions": (
            "1. Boil a pot of salted water and cook the spaghetti according to package instructions, then drain. \n"
            "2. Heat a skillet over medium heat and add the ground beef. \n"
            "3. Break up the beef with a spoon and cook until browned, about 7-10 minutes. \n"
            "4. Pour in the tomato sauce and stir well. Let the sauce simmer for 5-7 minutes. \n"
            "5. Season the sauce with salt, pepper, and optional Italian herbs like oregano or basil. \n"
            "6. Combine the cooked spaghetti with the sauce and toss to coat evenly. \n"
            "7. Serve hot, garnished with grated Parmesan cheese, if desired. \n"
        )
    },
    "Berry Smoothie": {
        "ingredients": {"blueberries": 100, "strawberries": 100, "yogurt": 150, "banana": 100},
        "macros": {"protein": 8, "fat": 5, "carbs": 30},
        "calories": 200,
        "instructions": (
            "1. Rinse the blueberries and strawberries thoroughly under running water. \n"
            "2. Hull the strawberries to remove the green tops. \n"
            "3. Add the blueberries, strawberries, and yogurt to a blender. \n"
            "4. Blend the ingredients on high speed for 1-2 minutes until smooth. \n"
            "5. If the smoothie is too thick, add a splash of milk or water and blend again. \n"
            "6. Pour the smoothie into a glass and serve immediately. \n"
            "7. Optional: Garnish with a few whole berries or a mint leaf on top. \n"
        )
    },
    "Avocado Toast": {
        "ingredients": {"bread": 50, "avocado": 100},
        "macros": {"protein": 5, "fat": 15, "carbs": 20},
        "calories": 250,
        "instructions": (
            "1. Toast the bread slices in a toaster or on a heated skillet until golden and crisp. \n"
            "2. Cut the avocado in half, remove the pit, and scoop the flesh into a bowl. \n"
            "3. Mash the avocado with a fork until smooth, or leave it chunky if preferred. \n"
            "4. Season the mashed avocado with salt, pepper, and optional lemon juice for extra flavor. \n"
            "5. Spread the avocado mixture evenly on the toasted bread. \n"
            "6. Serve as-is, or top with additional toppings like sliced tomatoes, boiled eggs, or chili flakes. \n"
        )
    },
    "Chicken Stir-Fry": {
        "ingredients": {"chicken": 150, "peppers": 100, "soy sauce": 10},
        "macros": {"protein": 30, "fat": 5, "carbs": 10},
        "calories": 250,
        "instructions": (
            "1. Slice the chicken breast into thin strips. \n"
            "2. Chop the bell peppers into bite-sized pieces. \n"
            "3. Heat a wok or large skillet over high heat and add a tablespoon of oil. \n"
            "4. Add the chicken to the pan and stir-fry for 5-6 minutes until fully cooked. Remove and set aside. \n"
            "5. In the same pan, stir-fry the bell peppers for 3-4 minutes until slightly softened. \n"
            "6. Return the chicken to the pan and add the soy sauce. Toss everything together for 1-2 minutes. \n"
            "7. Serve hot, optionally over steamed rice or noodles. \n"
        )
    },
    "Vegetable Soup": {
        "ingredients": {"carrot": 100, "celery": 50, "potato": 150, "stock": 500},
        "macros": {"protein": 5, "fat": 3, "carbs": 30},
        "calories": 150,
        "instructions": (
            "1. Peel and chop the carrots and potatoes into small cubes. Chop the celery into small pieces. \n"
            "2. Heat a pot over medium heat and add a teaspoon of oil or butter. \n"
            "3. Sauté the carrots and celery for 3-4 minutes until softened. \n"
            "4. Add the potatoes and pour in the vegetable stock. Bring to a boil. \n"
            "5. Reduce the heat and let the soup simmer for 15-20 minutes until the vegetables are tender. \n"
            "6. Season with salt, pepper, and optional herbs like thyme or parsley. \n"
            "7. Serve hot with a side of bread or crackers. \n"
        )
    },
    "Mexican Tacos": {
        "ingredients": {"ground beef": 150, "taco shells": 50, "lettuce": 30, "cheese": 20},
        "macros": {"protein": 25, "fat": 15, "carbs": 20},
        "calories": 400,
        "instructions": (
            "1. Heat a skillet over medium heat and add the ground beef. \n"
            "2. Break up the beef with a spatula and cook until browned and fully cooked, about 8-10 minutes. \n"
            "3. Season the beef with salt, pepper, and optional taco seasoning. Stir to combine. \n"
            "4. Warm the taco shells in a skillet or oven according to package instructions. \n"
            "5. Fill each taco shell with a layer of ground beef. \n"
            "6. Top with shredded lettuce and grated cheddar cheese. \n"
            "7. Serve immediately, with salsa or guacamole on the side if desired. \n"
        )
    },
    "Chicken Curry": {
    "ingredients": {"chicken": 300, "onion": 100, "tomato": 100, "curry": 15, "coconut milk": 200},
    "macros": {"protein": 40, "fat": 25, "carbs": 15},
    "calories": 450,
    "instructions": (
        "1. Heat oil in a pan over medium heat. \n"
        "2. Add chopped onions and sauté until golden brown. \n"
        "3. Add minced garlic and ginger, and cook for 1 minute. \n"
        "4. Stir in curry powder and cook for 30 seconds to release the aroma. \n"
        "5. Add chopped tomatoes and cook until soft, about 5 minutes. \n"
        "6. Add chicken pieces and cook until lightly browned. \n"
        "7. Pour in coconut milk and simmer for 15-20 minutes, until the chicken is cooked through. \n"
        "8. Season with salt to taste. \n"
        "9. Serve hot with steamed rice or naan bread. \n"
    )
}

}

supermarkets = {
    "Mercadona - Serrano 61": {
        "address": "C. de Serrano, 61, Salamanca, 28006 Madrid, Spain",
        "coordinates": (40.430460, -3.686260)
    },
    "Mercadona - General Martínez Campos": {
        "address": "P.º del Gral. Martínez Campos, Chamberí, 28010 Madrid, Spain",
        "coordinates": (40.438330, -3.693180)
    },
    "Mercadona - Fuencarral 77": {
        "address": "Calle de Fuencarral, 77, Centro, 28004 Madrid, Spain",
        "coordinates": (40.427610, -3.701950)
    },
    "Mercadona - Ayala 89": {
        "address": "Cl. de Ayala, 89, Salamanca, 28006 Madrid, Spain",
        "coordinates": (40.429940, -3.675410)
    },
    "Mercadona - Paseo de La Habana 10": {
        "address": "P.º de La Habana, 10, Chamartín, 28036 Madrid, Spain",
        "coordinates": (40.451500, -3.687650)
    },
    "Mercadona - Pintor Juan Gris 3": {
        "address": "C. del Pintor Juan Gris, 3, Tetuán, 28020 Madrid, Spain",
        "coordinates": (40.459100, -3.698360)
    },
    "Carrefour Express - Hermosilla 28": {
        "address": "C. de Hermosilla, 28, Salamanca, 28001 Madrid, Spain",
        "coordinates": (40.425220, -3.685710)
    },
    "Carrefour Express - Villanueva 24": {
        "address": "C. de Villanueva, 24, Salamanca, 28001 Madrid, Spain",
        "coordinates": (40.426780, -3.688130)
    },
    "Carrefour Express - Zurbano 11": {
        "address": "Calle de Zurbano, 11, Chamberí, 28010 Madrid, Spain",
        "coordinates": (40.428250, -3.690870)
    },
    "Carrefour Express - Castelló 36": {
        "address": "Calle de Castelló, 36, Salamanca, 28001 Madrid, Spain",
        "coordinates": (40.426120, -3.678580)
    },
    "Carrefour Market - Conde de Peñalver 15": {
        "address": "C. del Conde de Peñalver, 15, Salamanca, 28006 Madrid, Spain",
        "coordinates": (40.428650, -3.675250)
    },
    "Mi Alcampo - Lagasca 51": {
        "address": "Calle de Lagasca, 51, Salamanca, 28001 Madrid, Spain",
        "coordinates": (40.426770, -3.683020)
    },
    "Mi Alcampo - Rodrigo Rebolledo 31": {
        "address": "C. de Rodrigo Rebolledo, 31, Salamanca, 28001 Madrid, Spain",
        "coordinates": (40.424930, -3.678750)
    },
    "Mi Alcampo - Alcalá 137": {
        "address": "C. de Alcalá, 137, Salamanca, 28001 Madrid, Spain",
        "coordinates": (40.425710, -3.671530)
    },
    "Mi Alcampo - Dr. Castelo 28": {
        "address": "Calle del Dr. Castelo, 28, Retiro, 28009 Madrid, Spain",
        "coordinates": (40.423410, -3.673220)
    }
}


if __name__ == "__main__":
    main()


