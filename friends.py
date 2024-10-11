friends_list1 = ["Alice", "Bob", "Charlie", "David"]
friends_list2 = ["Charlie", "Eve", "Frank", "Alice"]
merged_list = friends_list1 + friends_list2
unique_friends = list(set(merged_list))
print("Merged list of friends (without duplicates):")
print(unique_friends)