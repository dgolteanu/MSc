
# create code to ask user to input location of files, store in variable & pass var to setwd function
# ask user for any patterns to be removed from filename to match feature labels
setwd('/Users/dolteanu/local_documents/Coding/MSc/FinalProject/Data/letter calls/')
files<- list.files(path='./', pattern='.txt')
colname<-vector()
genotyping<-vector()
files[1]
name <- files[1]
name2 <-files[2]
samples <-read.table(name,sep = "\t",header=T)
samples2 <- read.table(name,header = T,sep = "\t")

write.table(samples[,2], file = "../../Output/calls.csv",row.names=samples[,1], col.names=name,sep=",")

write.table(c("\n",name,samples2[,2]),file = "../../Output/calls.csv", append=T, col.names=F,sep=",")


##once the second write.table works add it into the for loop 
# for (i in files) {
#   name<- toString(i)
#   sample <- read.csv(i)
# }
# write.
# c(" ",name)
