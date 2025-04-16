def reverse_sentence(sentence, start, end):
  i = end
  j = start
  while j < i:
    sentence[j], sentence[i] = sentence[i], sentence[j]
    j += 1
    i -= 1

def do_reverse(sent):
  sentence = list(sent)
  reverse_sentence(sentence, 0, len(sentence) -1)
  j = 0
  while j < len(sentence):
    # First get to word start
    while j < len(sentence) and sentence[j] == ' ':
      j += 1
    if j == len(sentence):
      break
    word_start = j
    # Go till word end
    while j < len(sentence) and sentence[j] != ' ': 
      j += 1
    word_end = j - 1
    reverse_sentence(sentence, word_start, word_end)
  return ''.join(sentence)


sentence = 'the    quick brown fox      jumped over the lazy dog'
print(sentence)
new_sent = do_reverse(sentence)
print(new_sent)

