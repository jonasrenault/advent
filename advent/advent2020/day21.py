from advent.utils.utils import Advent

advent = Advent(21, 2020)


def main():
    lines = advent.get_input_lines()
    foods, ingredients, allergens = read_input(lines)

    non_allergenic = set(ingredients)
    for allergen in allergens:
        non_allergenic -= get_ingredients_for_allergen(foods, allergen)

    c = 0
    for ings, _ in foods:
        c += len(non_allergenic & set(ings))
    advent.submit(1, c)

    options = dict()
    for allergen in allergens:
        options[allergen] = get_ingredients_for_allergen(foods, allergen)

    dangerous_ingredients = dict()
    while len(dangerous_ingredients) != len(options):
        for allergen, ingredients in options.items():
            ingredients = ingredients - set(dangerous_ingredients.values())
            if len(ingredients) == 1:
                dangerous_ingredients[allergen] = ingredients.pop()

    advent.submit(
        2, ",".join([dangerous_ingredients[k] for k in sorted(dangerous_ingredients)])
    )


def get_ingredients_for_allergen(
    foods: list[tuple[list[str], list[str]]], allergen: str
) -> set[str]:
    """
    Find possible ingredients for a given allergen.

    Args:
        foods (list[tuple[list[str], list[str]]]): list of foods
        allergen (str): an allergen

    Returns:
        set[str]: set of possible ingredients
    """
    ingredients: set[str] = set()
    for ings, alls in foods:
        if allergen in alls:
            if not ingredients:
                ingredients = set(ings)
            else:
                ingredients &= set(ings)

    return ingredients


def read_input(
    lines: list[str],
) -> tuple[list[tuple[list[str], list[str]]], set[str], set[str]]:
    """
    Read lines to get list of foods, set of ingredients and set of allergens.

    Args:
        lines (list[str]): input lines

    Returns:
        tuple[list[tuple[list[str], list[str]]], set[str], set[str]]: list of
        foods, set of ingredients and set of allergens
    """
    foods = []
    ingredients = set()
    allergens = set()
    for line in lines:
        ings = line[: line.index("contains") - 2].split()
        alls = line[line.index("contains") + len("contains") + 1 : -1].split(", ")
        ingredients.update(ings)
        allergens.update(alls)
        foods.append((ings, alls))
    return foods, ingredients, allergens


if __name__ == "__main__":
    main()
