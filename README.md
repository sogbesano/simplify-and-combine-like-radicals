# simplify-and-combine-like-radicals
Python program that simplifies and combine like radicals.
Program uses Prime Factorization to simplify radicals.

# Usage
A radical is represented by a list of 3 elements, the first element is the radical factor, the second element is the radicand, and the third element is the index.
For example, the radical 4 * sqrt(3) would be represented by the list [4, 3, 2],
notice that the index is 2 because we take the sqrt in the example.

Program currently simplifies radicals, the three cases it works on currently are,
where the radicand is a numeral, i.e. 100, or the radicand is a literal, i.e. 'x',
or the radicand is a numeral and literal combination, i.e. '9x'.

Program can simplifiy a bunch of radicals at the same time, this is done by storing all
the radicals you wish to simplify in a list of lists, for example:
radicals = [[4, 3, 2], [1, 75, 2], [1, 'x', 2]]

To simplify a radical, use the function 'simplify_radical' which takes one argument, the radical to be simplified. To simplify a more than one radical at a time, create a list
of lists of radicals and use the map function with the simplify_radical function as the function parameter, i.e. the first parameter,
 and the radicals as the iterable parameter, i.e. the second parameter, then parse the result from that into a list for example:

simplfied_radicals = list(map(simplify_radical, radicals))

you can then print the list like so:
print(simplified_radicals)

To combine radicals with like terms, first get the radicals with like terms, to do this first determine whether you want to do it for radicals with radicands that are numerals, literals, or numeral and literal combinations. If you are working with numerals, then use the function get_numeral_radicals which takes as an argument radicals with the same index, such as [1, '75y', 2] and [4, '3y', 2], note that they both have the index 2, pass them as a list of lists for example, [[1, '75y', 2], [4, '3y', 2]]. 
If you're working with literal radicals then use the get_literal_radicals function which works the same way, pass it to radicals with the same index. 
And if you're working with radicals that have numeral and literal radicands then use the function get_numeral_literal_radicals which also takes the same argument. 

Next get the like radicals by using the function get_like_radicals which takes, numeral radicals, literal radicals, or numeral and literal radicals as it's argument, i.e. what you get from using the functions in the last paragraph

The second to last step is to get the prime radicands, to do this use the get_prime_radicands function which takes as an argument like radicals, obtained using the get_like_radicals function. 

The last step is to combine the like radicals, this is done by using the combine_like_radicals function which takes 2 arguments, the first one is the like radicals obtained by using the get_like_radicals function and the second argument is the prime radicands, obtained by using the get_prime_radicands function.

# Installation
Clone the repo and run python3 main.py 
