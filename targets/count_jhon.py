def count_jhon(statement):
  count = 0
  for i in range(len(statement)-1):
    if statement[i:i+4] == 'Emma':
        count += 1
    # Cannot handle the
    # count += statement[i:i+4] == 'Emma'
  return count

print(count_jhon("Emma is good developer. Emma is aslo a writer"))
