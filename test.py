print("x y z w")
for x in range(0,2):
    for y in range(0,2):
        for z in range(0,2):
            for w in range(0,2):
                result1 = bool((w or not (y)) <= (z == x))
                result2 = bool((w or not (y)) == (x <= z))
                if not ((result1 == True) and (result2 == True)):
                    print(x,y,z,w,int(result1),int(result2))