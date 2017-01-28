

#read from filtered file
final = ""
with open("filtered_HLA_B.txt") as f:
    content = f.readlines()
    for i in xrange(1, len(content)+1):
        if i % 2 == 0: 
        	x = content[i-2].strip() + content[i-1].strip()
        	print x
        	final = final + '\n'+ x
        	#generate string by joining every two lines, ie "allele group" + "sequence"

#convert bases to integers
final = final.replace('A', '0')
final = final.replace('T', '1')
final = final.replace('C', '2')
final = final.replace('G', '3')
final = final.replace('-', '4')

#write to output file
f = open('filtered_HLA_B_final.txt', 'w')
f.write(final)
f.close()

