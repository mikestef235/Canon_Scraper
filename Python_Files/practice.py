word = 'apple'
words = [word,'hih']
palindromes=[]

for word in words:
    if word == word[::-1]:
        palindromes.append(word)

print(max(palindromes, key=len))