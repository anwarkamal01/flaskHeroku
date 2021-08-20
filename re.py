import re

userinput="abc"

pattern=re.compile("^[a-zA-Z0-9]{8,}$")

#create regex with a pattern

if(pattern.match(userinput)):#match will return None if there is no match
    print ("Input is correct!")
else:
    print ("Input does not match pattern!")

    

userinput="abc12345678"

if(pattern.match(userinput)):
    print("Input is correct!")
else:
    print("Input does not match pattern!")
