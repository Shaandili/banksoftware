# banksoftware
#the program reads from the Recommendations.txt file, so it needs to be in the same folder
#there are a few bugs in the program:
#1.when one tries to withdraw money from a CD account, it leads to a "pickle.UnpicklingError: unpickling stack underflow" 
#2.when one tries to view account details without any accounts being created in the bank, it gives a traceback as the file does not exist. This is due to the file being opened in "rb+" mode in the show() function, which fails if the file does not exist

 
