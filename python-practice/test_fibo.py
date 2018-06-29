from fibo import fibo_memo, fibo_iter, fibo_tail, fibo_recur

correct_fibonacci_seq = [0, 1, 1, 2, 3, 5, 8, 13]
for i, correct in enumerate(correct_fibonacci_seq):
	assert fibo_memo(i) == correct
	assert fibo_iter(i) == correct
	assert fibo_tail(i) == correct
	assert fibo_recur(i) == correct

#print(fibo_recur(6)) 
#print(fibo_memo(6))
#print(fibo_iter(6))
#print(fibo_tail(6))
