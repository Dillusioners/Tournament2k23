# string input
str1, str2 = input('Enter first string: '), input('Enter second string: ')

# if the sorted version of str1 and str2 are equal, i.e. if both are anagram
# and if the reversed version of str2 and regular str1 are equal, i.e. both are palindrome
if (list(str1).sort()) == (list(str2).sort()) and (str1 == str2[::-1]):
    print('Both the strings are palindrome and anagram to each other.')
    
else:
    print('Both strings do not mee the required condition.')
