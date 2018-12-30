
# We analyze the logic of the program ran with regi = [1, 0, 0, 0, 0, 0] :
#  - it increments reg1 until 10551288
#  - if reg1 * reg4 divides 10551288, it adds reg4 to reg0
#  - if reg1 == 10551288, it increments reg4 and sets reg1 back to 1
#  - if reg4 == 10551288, halts
# This means that reg0 contains the sum of the divisors of 10551288

nb = 10551288
res = 0
for i in range(1, nb+1):
    if (nb % i) == 0:
        res += i
print('Value of reg0 when program halts = ', res)