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
    #all_duplicates = list(map(list, set(map(tuple, [[duplicate, prime] for duplicate in single_duplicates for prime in p_factors if duplicate == prime]))))
    all_duplicates = []
    duplicate_bunch = []
    i = 0
    for duplicate in single_duplicates:
      duplicate_bunch = []
      a = list(filter(lambda x: x == duplicate, p_factors))
      b = len(a) - radical[2]
      c = list(remove_n_dupes(a, duplicate, b))
      all_duplicates.append(c)
    #like_factors = list(filter(lambda x: len(x) == radical[2], all_duplicates))
    like_factors = all_duplicates
    flattened_like_factors = [item for sublist in like_factors for item  in sublist]
    new_radicand = 0
    if(len(like_factors) == 1):
      if(flattened_like_factors == p_factors):
        new_radicand = flattened_like_factors[0]
      else:  
        if(not flattened_like_factors in p_factors):
          new_radicand = p_factors[0]
        #new_radicand = [y for x in flattened_like_factors for y in p_factors if x != y]
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
        b = list(remove_n_dupes(p_factors, i, len(like_factors)))
        arr.append(b)
        j += 1
      diff = []
      k = 0
      for i in arr:
        a = list(filter(lambda x: x == list(set(flattened_like_factors))[k], i))
        diff.append(a)
        k += 1
      flattened_diff = [item for sublist in diff for item  in sublist]
      if(set(p_factors).issubset(flattened_like_factors) and flattened_diff):
        new_radicand = reduce(lambda x, y: x * y, flattened_diff)
      else:
        factors_diff = list(set(flattened_like_factors).symmetric_difference(set(p_factors)))
        if(not factors_diff):
          new_radicand = reduce(lambda x, y: x * y, prime_radical_factors)
        else:
          new_radicand = reduce(lambda x, y: x * y, factors_diff)
        #new_radicand = list(set(flattened_like_factors).symmetric_difference(set(p_factors)))
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
    simplified_temp_radical = []
    if(is_integer(temp_radical[1])):
      simplified_temp_radical = simplify_radical_numeral_part(temp_radical)
    else:
      simplified_temp_radical = temp_radical
    if(len(simplified_temp_radical) == 1):
      return simplified_temp_radical
    if(simplified_temp_radical[1]):
      simplified_radicand = radical[1][-1]
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
  return list(set([radical[2] for radical in radicals]))

#returns a dictionary of int to list of lists, where the int is the index and the list of lists are the radicals with that index
def get_radicals_with_index(radicals, index):
  return {index : list(filter(lambda radical: radical[2] == index, radicals))}

#returns a list of lists of all the like radicals
def get_like_radicals(radicals_same_index):
  i = 0
  j = 1
  duplicates = []
  final_dups = []
  for radical1 in radicals_same_index:
    for radical2 in radicals_same_index:
      if(j >= len(radicals_same_index)):
        break
      if(radicals_same_index[i][1] == radicals_same_index[j][1]):
        if(radicals_same_index[i] not in duplicates and radicals_same_index[j] not in duplicates):
          duplicates.append(radicals_same_index[i])
          duplicates.append(radicals_same_index[j])
          break
        elif(radicals_same_index[i][1] == radicals_same_index[j][1]): 
          duplicates.append(radicals_same_index[j])
          break
        j += 1    
      if(j >= len(radicals_same_index)):
        break
    i = i + 1
    j = i + 1
  return duplicates

#returns a list of the prime radicands
def get_prime_radicands(like_radicals):
  #return list(filter(lambda x, y: (x == y), like_radicals))
  return list(set([like_radical[1] for like_radical in like_radicals]))

def combine_like_radicals(grouped_like_radicals, prime_radicands):
  radicals_same_radicand = []
  combined_like_radicals = []
  new_radical_factor = 0
  new_radical = []
  for prime_radicand in prime_radicands:
    radicals_same_radicand = []
    for like_radical in grouped_like_radicals:
      if(prime_radicand == like_radical[1]):
        #print('RADICAL FACTOR: ', like_radical[0])
        new_radical_factor += like_radical[0]
        #radicals_same_radicand.append(like_radical)
    #ret.append(radicals_same_radicand)
    new_radical = [new_radical_factor, prime_radicand, like_radical[2]]
    new_radical_factor = 0
    combined_like_radicals.append(new_radical)
  
  #new_radical_factor = 0
  #for i in ret:
  #  for j in i:
  #    print(j)
  #    print(j[0])

  return combined_like_radicals

def get_unlike_radicals(radicals, like_radicals):
  unlike_radicals = []
  for radical in radicals:
    if(radical not in like_radicals and like_radicals): 
      unlike_radicals.append(radical)
  return unlike_radicals

def main():
  #a radical is represented by a list of 3 elements, the first element is the radical factor, the second element is the radicand, and the third element is the index
  #radicals = [[4, 3, 2], [1, 75, 2], [1, 'x', 2], [1, '9x', 2], [1, 18, 2], [-1, 28, 2], 
  #            [-1, 63, 2], [4, 7, 2], [3, '10000a', 2], [3, '1000000a', 2], [3, '100000000a', 2], [1, 252, 2], 
   #           [1, 200, 2]]
  #radicals = [[4, 3, 2], [1, 75, 2], [1, 'x', 2], [1, '9x', 2], [1, 18, 2], [-1, 28, 3], [-1, 63, 3], [4, 7, 3], [3, '100a', 2], [1, 252, 4], [3, '1000000a', 4], [7, 3, 2], [4, 'x', 2], [7, 'x', 2], [2, 'y', 2], [1, 'y', 2]]
  #radicals = [[3, '100a', 2]]
  #radicals = [[1, 252, 2]]
  #radicals = [[4, 7, 2], [-1, 28, 2], [-1, 63, 2]]
  #radicals = [[1, '75y', 2], [4, '3y', 2]]
  #radicals = [[6, 'b', 2], [-1, 'b', 2], [1, '25a', 2], [-2, 'a', 2]]
  #radicals = [[1, 75, 2], [4, 3, 2], [1, 18, 2]]
  #radicals = [[1, 8, 2], [-2, 8, 2], [7, 8, 2]]
  radicals = [[2, '9y', 2], [-3, 'y', 2], [-1, '4x', 2], [7, 'x', 2]]
  print('radicals are: ', radicals)
  #print('prime radicals are: ', get_prime_radicals(radicals))
  #print('numeral radicals are: ', get_numeral_radicals(radicals))
  #print('literal radicals are: ', get_literal_radicals(radicals))
  #print('numeral and literal radicals are: ', get_numeral_literal_radicals(radicals))
  #radicals = [[4, 3, 2], [1, 75, 2], [1, 'x', 2], [1, '9x', 2], [1, 18, 2], [-1, 28, 2], [-1, 63, 2], [4, 7, 2], [3, '100a', 2]]
  simplified_radicals = list(map(simplify_radical, radicals))
  print('simplified radicals are: ', simplified_radicals)
  #print('all indexes: ', get_all_indexes(simplified_radicals))
  #print(get_radicals_with_index(simplified_radicals, 2))
  #print(get_radicals_with_index(simplified_radicals, 3))
  #print(get_radicals_with_index(simplified_radicals, 4))
  radicals_same_index = list(get_radicals_with_index(simplified_radicals, 2).values())[0]
  radicals_numerals = get_numeral_radicals(radicals_same_index)
  radicals_literals = get_literal_radicals(radicals_same_index)
  radicals_numerals_literals = get_numeral_literal_radicals(radicals_same_index)
  #print(radicals_same_index)
  #print('NUMERALS ONLY', radicals_numerals)
  #print('LITERALS ONLY', radicals_literals)
  grouped_like_radicals_numerals = get_like_radicals(radicals_numerals)
  grouped_like_radicals_literals = get_like_radicals(radicals_literals)
  grouped_like_radicals_numerals_literals = get_like_radicals(radicals_numerals_literals)
  #print('radicals with like numerals: ', get_like_radicals(radicals_numerals))
  #print('radicals with like literals: ', get_like_radicals(radicals_literals))
  #print('radicals with like numerals and literals: ', get_like_radicals(radicals_numerals_literals))
  unlike_radicals_numerals = get_unlike_radicals(simplified_radicals, grouped_like_radicals_numerals)
  unlike_radicals_literals = get_unlike_radicals(simplified_radicals, grouped_like_radicals_literals)
  unlike_radicals_numerals_literals = get_unlike_radicals(simplified_radicals, grouped_like_radicals_numerals_literals)
  #print('UNLIKE NUMERAL RADICALS ARE: ', unlike_radicals_numerals) 
  #print('UNLIKE LITERAL RADICALS ARE: ', unlike_radicals_literals) 
  #print('UNLIKE NUMERAL AND LITERAL RADICALS ARE: ', unlike_radicals_numerals_literals) 
  prime_radicands_literals = get_prime_radicands(grouped_like_radicals_literals)
  prime_radicands_numerals = get_prime_radicands(grouped_like_radicals_numerals)
  prime_radicands_numerals_literals = get_prime_radicands(grouped_like_radicals_numerals_literals)
  #print('prime numeral radicands are: ', get_prime_radicands(grouped_like_radicals_numerals))
  #print('prime literal radicands are: ', get_prime_radicands(grouped_like_radicals_literals))
  #print('prime numeral and literal radicands are: ', get_prime_radicands(grouped_like_radicals_numerals_literals))
  print('simplified and combined numeral radicals: ', combine_like_radicals(grouped_like_radicals_numerals, prime_radicands_numerals) + unlike_radicals_numerals)
  print('simplified and combined literal radicals: ', combine_like_radicals(grouped_like_radicals_literals, prime_radicands_literals) + unlike_radicals_literals)
  print('simplified and combined combined numeral and literal radicals: ', combine_like_radicals(grouped_like_radicals_numerals_literals, prime_radicands_numerals_literals) + unlike_radicals_numerals_literals)
  

if __name__ == '__main__':
  main()
