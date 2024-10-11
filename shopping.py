shopping_list = ["Apples", "Bananas", "Carrots", "Dairy", "Eggs"]
print("Shopping List before removing an item:")
print(shopping_list)
item_to_remove = "Carrots"
if item_to_remove in shopping_list:
    shopping_list.remove(item_to_remove)
else:
    print(f"{item_to_remove} is not in the shopping list.")
print("\nShopping List after removing the item:")
print(shopping_list)