#! /usr/bin/python
import sys
import argparse

'''

Find corresponding pathways to list of KOs from BlastKOALA results

Usage:
ko_pathway_mapper.py -k <BlastKOALA results> -d <KEGG database file> (-o <output file>)

KEGG database file from https://www.genome.jp/kegg-bin/get_htext?ko00001.keg 
Click "Download htext"

'''
def database(db):
	
	keg={}
	
	A=""
	B=""
	C=""
	D=""
	
	for line in db:
		lsplit=line.strip().split(" ")
		if line.startswith("#") or line.startswith("!") or line.startswith("+"):
			pass
		elif line.startswith("A"):
			A=line[1:].strip()
		elif line.startswith("B") and len(lsplit)>1:
			B=line[2:].strip()
		elif line.startswith("C"):
			C=line[4:].strip()
		elif line.startswith("D") and lsplit[6] in keg.keys():
			keg[lsplit[6]].append([C,B,A])
		elif line.startswith("D"):
			keg[lsplit[6]]=[[C,B,A]]

	return keg
	
def main(argv):
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-k','--ko', required=True, help='BlastKOALA file')
	parser.add_argument('-d','--database_keg', required=True, help='KEGG database')
	parser.add_argument('-o', '--output', default="def", help='Output file')
	args = parser.parse_args()

	blastkoala=open(args.ko)
    
	if args.output=="def":
		out=open(args.ko.replace(".txt","")+"_pathways.txt","w")
	else:
		out=open(args.output,"w")
		
	db=open(args.database_keg)
	
	keg=database(db)
	
	for line in blastkoala:
		lsplit=line.strip().split("\t")
		if len(lsplit)>2 and lsplit[1]!="":
			out.write(lsplit[0]+"\t"+lsplit[1]+"\t"+lsplit[2]+"\t")
			for item in keg[lsplit[1]]:
				out.write(" - ".join(item)+" // ")
			out.write("\n")
		elif len(lsplit)>1 and lsplit[1]!="":
			out.write(lsplit[0]+"\t"+lsplit[1]+"\t"+lsplit[2]+"\t")
			for item in keg[lsplit[1]]:
				out.write(" - ".join(item)+" // ")
			out.write("\n")
		elif len(lsplit)>2:
			out.write("\t".join(lsplit[:3])+"\n")
		else:
			out.write(line)
		
	
     
if __name__ == '__main__':   
    main(sys.argv)
