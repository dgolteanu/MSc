#Set the working directory. I set it to my desktop
setwd("/Users/Your_Directory_Here")
# Read in the csv file with data.
# There is a header line in data, so header = TRUE
# I assigned my csv data to the name musstackSNPs
musstackSNPs <- read.csv('/Users/Your_Directory_Here/File_Name.csv', he
ader = TRUE)
# Assign the SNP state column from my musstackSNPs dataframe as a facto
r. Stored the four possible genotype results (-1 or No Call, 0 or AA, 1
or AB, 2 or BB) as levels
#SNPstate <- factor(musstackSNPs$SNP_State, levels = c("-1", "0", "1",
"2"))
#change colours of SNP state by assigning new numbers corresponding wit
h colour
SNPstate <- musstackSNPs$SNP_State
SNPstate[SNPstate = = 1] <- 5 #blue
SNPstate[SNPstate = = -1] <- 1 #black
SNPstate[SNPstate = = 0] <- 8 #grey
SNPstate[SNPstate = = 2] <- 6 #pink
# Assign the data from the Name column from my musstackSNPs dataframe a
s a factor. Stored the eight Mus species I examined as levels
musstackSNPs$Name <- factor(musstackSNPs$Name, levels = c("M. musculu
s", "M. m. castaneus 1", "M. m. castaneus 2", "M. dunni 1", "M. dunni 2
", "M. famulus 1", "M. famulus 2", "M. famulus 3", "M. fragilicauda 1",
"M. fragilicauda 2", "M. fragilicauda 3", "M. fragilicauda 4", "M. car
oli 1", "M. caroli 2", "M. caroli 3", "M. cervicolor 1", "M. cervicolor
2", "M. cookii"))
# Adjusted plot parameters. Added space to the left margin by increasin
g second value in mar vector to 7.
# Adujsted the axis label locations (mgp) (first value in vector (origi
nal 3 changed to 4)) to move them further away from the inner axis labe
l
# Set xpd = NA to allow for adding a legend outside of the plot area
par(mar =
c(5,7,4,2),mgp = c(4,1,0), xpd =
NA)
# Create a plot. X axis is genome position & y axis will be the associa
ted species names
plot(
musstackSNPs$Location,musstackSNPs$Name,
main = "Your Title Here", #title of plot. This plot displays SNPs o
n a chromosome
yaxt = 'n', #Use this option to not display the y axis ticks and la
bels
ylab = "Your species", # y axis label
xlab = "Genome Position (bp)", #x axis label
xlim = c(genomic_start_position, genomic_end_position), #sets range
for x axis. Put base-pair value of genomic start and end position of c
hromosome for species of interest
pch = 20, #sets the plot marker shape -- circle
col = SNPstate # Colour the plot points by SNP state factor
)
# Next line allows axis labels to be printed horizontally. value of 1
= horizontal always.
par(las = 1)
# add y axis in. value of 2 represents y axis. use 'at' to add labels a
t a regular sequence from 1-8 becuase I have 8 mice samples. I added a
vector of the mouse species' names as the tick labels.
#I adjusted the axis font size to be smaller using cex.axis
axis(2, at = seq(1:18),
labels = c("M. musculus", "M. m. castaneus 1", "M. m. castaneus
2", "M. dunni 1", "M. dunni 2", "M. famulus 1", "M. famulus 2", "M. fam
ulus 3", "M. fragilicauda 1", "M. fragilicauda 2", "M. fragilicauda 3",
"M. fragilicauda 4", "M. caroli 1", "M. caroli 2", "M. caroli 3", "M.
cervicolor 1", "M. cervicolor 2", "M. cookii"),
cex.axis = 0.5
)
#Add a legend.
#legend is comprised of the four possible MDGA genotype results (-1, 0,
1, 2)
legend(-2829834,20.94821,
legend = c("No Call", "AA", "AB", "BB"),
pch = 20, #Set legend symbols
ncol = 2, # split genotype symbols and corresponding colours i
n two columns
cex = 0.75, # reduced size of legend
col = c(1, 8, 5, 6) #added colours of genotype values
)
