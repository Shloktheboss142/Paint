a = 2
b = 2
# for x in range(2):
#     for y in range(x):
#         print(y)
#         print(a + y,b + y)

for x in range(1,3):
    print(a+x - 1,b+x - 1)
    print(a,b+x)
    print(a+x,b)
    print(a,b-x)
    print(a-x,b)
    print(a-x + 1,b-x + 1)
    print("x: " + str(x))

# 2 2 m 
# 2 3 m
# 3 2 m 
# 2 1 m 
# 1 2 m 
# 1 1 m
# x: 1
# 3 3 m 
# 2 4 m 
# 4 2 m 
# 2 0 m
# 0 2 m
# 0 0
# x: 2

# 3,1
# 1,3