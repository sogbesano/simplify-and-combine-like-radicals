import collections
from functools import reduce

#returns True if n is a prime numeral number, False otherwise
def is_prime_numeral(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

#returns True if n is a prime literal number, False otherwise
def is_prime_literal(n):
  return len(n) == 1 and n.isalpha()

#returns True if n is a prime numeral and literal number, False otherwise
def is_prime_numeral_literal(n):
  str_len = len(n)
  is_prime_numeral_literal = False
  if str_len >= 2:
    numeral_str = n[:-1]
    numeral_int = int(numeral_str, 10)
    if(is_prime_numeral(numeral_int)):
      is_prime_numeral_literal = True
  literal_str = n[-1]
  if not literal_str.isalpha():
    is_prime_numeral_literal = False
  return is_prime_numeral_literal

#returns True if n is an integer, False otherwise
def is_integer(n):
  return isinstance(n, int)

#returns True if n is a character, False otherwise
def is_char(n):
  return isinstance(n, str) and len(n) == 1

#returns True if n is a str, False otherwise
def is_str(n):
  return isinstance(n, str) and len(n) >= 2

#returns a list of lists of the radicals whose radicands are prime numerals, an example radicand would be 3
def get_prime_numerals(radicals):
  numeral_radicals = [radical for radical in radicals if is_integer(radical[1])]
  return [radical for radical in numeral_radicals if is_prime_numeral(radical[1])]

#returns a list of lists of the radicals whose radicands are prime literals, an example radicand would be 'x'
def get_prime_literals(radicals):
  literal_radicals = [radical for radical in radicals if is_char(radical[1])]
  return [radical for radical in literal_radicals if is_prime_literal(radical[1])]

#returns a list of lists of the radicals whose radicands are prime numerals and literals, an example radicand would be '3x'
def get_prime_numerals_literals(radicals):
  numeral_literal_radicals = [radical for radical in radicals if is_str(radical[1])]
  return [radical for radical in numeral_literal_radicals if is_prime_numeral_literal(radical[1])]
  
#returns a dictionary of strings to list of lists of radicals whose radicands are prime numbers
def get_prime_radicals(radicals):
  return {'prime_numerals' : get_prime_numerals(radicals),
          'prime_literals' : get_prime_literals(radicals),
          'prime_numerals_and_literals' : get_prime_numerals_literals(radicals)
         }

#returns a list of lists of all radicals with numeral radicands
def get_numeral_radicals(radicals): 
  return [radical for radical in radicals if is_integer(radical[1])]

#returns a list of lists of all radicals with literal radicands
def get_literal_radicals(radicals):
  return [radical for radical in radicals if is_char(radical[1])]

#returns a list of lists of all radicals with numeral and literal radicands
def get_numeral_literal_radicals(radicals):
  return [radical for radical in radicals if is_str(radical[1])]

#returns a list of primes from 2 to n
def get_primes(n):
  return [num for num in range(2, n) if is_prime_numeral(num)]

#returns a list of the prime factors of n
def prime_factors(n):
  i = 2
  factors = []
  while i <= n:
    if (n % i) == 0:
      factors.append(i)
      n = n / i
    else:
      i = i + 1
  return factors

#returns the simplified radical where the radicand is a numeral
def simplify_radical_numeral_part(radical):
  if(is_prime_numeral(radical[1])):
    return radical
  else:
    p_factors = prime_factors(radical[1])
    single_duplicates = [item for item, count in collections.Counter(p_factors).items() if count > 1]
    all_duplicates = list(map(list, set(map(tuple, [[duplicate, prime] for duplicate in single_duplicates for prime in p_factors if duplicate == prime]))))
    like_factors = list(filter(lambda x: len(x) == radical[2], all_duplicates))
    flattened_like_factors = [item for sublist in like_factors for item  in sublist]
    new_radicand = 0
    if(len(like_factors) == 1):
      if(flattened_like_factors == p_factors):
        new_radicand = flattened_like_factors[0]
      else:  
        new_radicand = [y for x in flattened_like_factors for y in p_factors if x != y][0]
    else:
      difference_factors = []
      removed_dupes = []
      i = 0
      for like_factor in like_factors:
        removed_dupes = list(remove_n_dupes(p_factors, like_factor[i], len(like_factors)))
        difference_factors.append(removed_dupes)
        i += 1
      diff = []
      k = 0
      for i in difference_factors:
        a = list(filter(lambda x: x == list(set(flattened_like_factors))[k], i))
        diff.append(a)
        k += 1
      flattened_diff = [item for sublist in diff for item  in sublist]
      prime_radical_factors = list(set(flattened_like_factors))
        
      j = 0
      arr = []
      for i in prime_radical_factors:
        b = list(remove_n_dupes(p_factors, i, len(diff[j]) / len(like_factors)))
        arr.append(b)
        j += 1
      diff = []
      k = 0
      for i in arr:
        a = list(filter(lambda x: x == list(set(flattened_like_factors))[k], i))
        diff.append(a)
        k += 1
      flattened_diff = [item for sublist in diff for item  in sublist]
      if(flattened_like_factors not in p_factors):
        new_radicand = reduce(lambda x, y: x * y, flattened_diff)
      else:
        new_radicand = list(set(flattened_like_factors).symmetric_difference(set(p_factors)))
    prime_radical_factors = list(set(flattened_like_factors))
    product_prime_radical_factors = reduce(lambda x, y: x * y, prime_radical_factors)
    new_radical_factor = radical[0] * product_prime_radical_factors
    if(isinstance(new_radicand, list) and new_radicand):
      return [new_radical_factor, new_radicand[0], radical[2]]
    else: 
      return [new_radical_factor, new_radicand, radical[2]]

#returns a simplified radical, i.e. in its prime form
def simplify_radical(radical):
  if(is_integer(radical[1])):
    if(is_prime_numeral(radical[1])):
      return radical
    else:
      return simplify_radical_numeral_part(radical)
  elif(is_char(radical[1])):
    return radical
  else:
    numeral_part_str = radical[1][:-1]
    numeral_part_int = int(numeral_part_str, 10)
    temp_radical = [radical[0], numeral_part_int, radical[2]]
    simplified_temp_radical = simplify_radical_numeral_part(temp_radical)
    if(simplified_temp_radical[1]):
      simplified_radicand = str(simplified_temp_radical[1]) + radical[1][-1]
    else:
      simplified_radicand = radical[1][-1]
    simplified_temp_radical[1] = simplified_radicand
    return simplified_temp_radical

#yields generator after removing 'how_many' duplicates of 'what' from 'remove_from' 
def remove_n_dupes(remove_from, what, how_many):
    count = 0
    for item in remove_from:
        if item == what and count < how_many:
            count += 1
        else:
            yield item

#returns a list of all indexes of the radicals
def get_all_indexes(radicals):
  return True

def main():
  #a radical is represented by a list of 3 elements, the first element is the radical factor, the second element is the radicand, and the third element is the index
  #radicals = [[1, 75, 2], [4, 3, 2], [1, 18, 2]]
  #radicals = [[4, 3, 2], [7, 'x', 2], [2, '9y', 2], [1, 75, 2], [3, '100a', 2], 
  #            [5, '3b', 2], [1, 2, 2], [3, 'a', 2]]
  radicals = [[4, 3, 2], [1, 75, 2], [1, 'x', 2], [1, '9x', 2], [1, 18, 2], [-1, 28, 2], [-1, 63, 2], [4, 7, 2], [3, '10000a', 2], [3, '1000000a', 2], [3, '100000000a', 2]]
  #radicals = [[3, '1_000_000a', 2]]
  print('radicals are: ', radicals)
  print('prime radicals are: ', get_prime_radicals(radicals))
  print('numeral radicals are: ', get_numeral_radicals(radicals))
  print('literal radicals are: ', get_literal_radicals(radicals))
  print('numeral and literal radicals are: ', get_numeral_literal_radicals(radicals))
  #radicals = [[4, 3, 2], [1, 75, 2], [1, 'x', 2], [1, '9x', 2], [1, 18, 2], [-1, 28, 2], [-1, 63, 2], [4, 7, 2], [3, '100a', 2]]
  simplified_radicals = list(map(simplify_radical, radicals))
  print(simplified_radicals)

if __name__ == '__main__':
  main()