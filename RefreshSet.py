#Script to refresh a specific set

#Make the variable SETCODE = your desired set to populate the database
#Then save the script file
#finally run the script until completion

from mtgDB import mtgDB

setcode = 'RNA'

#Populate with SetCode from above
mtgDB.UpdateSet(setcode)