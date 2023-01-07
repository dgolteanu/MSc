library(affxparser)
# create code to ask user to input location of files, store in variable & pass var to setwd function
# ask user for any patterns to be removed from filename to match feature labels
setwd('/Users/dolteanu/local_documents/Coding/MSc/FinalProject/Output')
files<- list.files(path='./', pattern='.txt')
colname<-vector()
genotyping<-vector()
 for (i in files) {
  name<-gsub("*_SNP.chp","",toString(i))
  lists<-assign(name,readChp(i))
  genotype<-cbind(lists$Genotype$Call)
  colname<-append(colname,name)
  genotyping<- cbind(genotyping,genotype)}
colnames(genotyping)=colname
row.names(genotyping)=lists$Genotype$ProbeNames
write.csv(genotyping,file="calls.csv", row.names=T)
 #should add function to check if variables are empty
