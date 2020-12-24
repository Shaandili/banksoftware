# banksoftware
#the program reads from the Recommendations.txt file, so it needs to be in the same folder
#there are a few bugs in the program:
#1.when one tries to withdraw money from a CD account, it leads to a "pickle.UnpicklingError: unpickling stack underflow" 
#2.when one tries to display or modify loan details, the details don't display and instead of modifying the old data after applying interest, the program prints the modified #object in the file (seperately)
#3. while executing the "pay back loan" option, the program is unable to read through the "accounts.dat" file properly and is unable to find the appropriate account to deduct #money from. it also prints an error message in this instance.

 
