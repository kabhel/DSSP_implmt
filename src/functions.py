from optparse import OptionParser
from subprocess import call
import datetime as dt

def argsParsing():
	"""
	Automatic creation of the help and parsing of arguments
	Options added : -i (input file), -o (output file)
	Return the input and output files
	"""
	parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
	parser.add_option("-i", "--input", dest='input', metavar="FILE",
	    help="The file name of a PDB formatted file containing the protein structure data.")
	parser.add_option("-o", "--output", dest='output', metavar="FILE",
	    help="The  file  name  of  a  DSSP  file to create.")
	(opt, args) = parser.parse_args()
	if not opt.input: parser.error('Input pdb file not given.')
	return(opt)

def hydrAddition(opt):
	"""
	Addition of hydrogens in the pdb file using a 
	shell command line to run the reduce program
	"""
	call(["./bin/reduce -NOFLIP "+opt.input+" 1>"+opt.input+".H"+" 2>"+opt.input+".H.log"],shell=True)

def lineHeader(dic):
	"""
	Access to all items of a dictionary and return a string
	of all existing items
	"""
	l = ""
	for mol_id,mol_items in dic.items():
		l += "MOL_ID: " + mol_id + "; "
		for key, item in mol_items.items():
			if (item != ""):
				l += key.upper() + ": " + item.upper() + "; "
	return(l)

def makeHeader(structure):
	"""
	Make and return the header of the dssp output using data from the pdb file
	"""
	header = "==== Secondary Structure Assignment using DSSP method ====\nDATE\t\t{}\n".format(dt.date.today())
	header += "REFERENCE\tW. KABSCH AND C.SANDER, BIOPOLYMERS 22 (1983) 2577-2637\n"
	header += "HEADER\t\t{}{:>28}\n".format(structure.header["head"].upper(),structure.header["deposition_date"])
	header += "COMPND\t\t{}\n".format(lineHeader(structure.header["compound"])) # all COMPND
	header += "SOURCE\t\t{}\n".format(lineHeader(structure.header["source"])) # all SOURCE
	header += "AUTHOR\t\t{}".format(structure.header["author"].upper())
	return(header+"\n")

def displayResults(opt,structure,dssp):
	#	print("  #  RESIDUE AA STRUCTURE BP1 BP2  ACC     N-H-->O    O-->H-N    N-H-->O    O-->H-N    TCO  KAPPA ALPHA  PHI   PSI    X-CA   Y-CA   Z-CA            CHAIN")
	header = makeHeader(structure)
	#descp = "  #  RESIDUE AA    TCO  KAPPA ALPHA  PHI   PSI    X-CA   Y-CA   Z-CA"
	descp = "  #  RESIDUE AA STRUCTURE"
	if (opt.output):
		with open(opt.output,'w') as filout:
			filout.write(header+descp+'\n')
			for i in range(0,len(dssp)):
				l = dssp[i]
				filout.write("{:>5d}{:>5d}{:>2s}{:>2s}{:>9.3f}{:>6.1f}{:>6.1f}{:>6.1f}{:>6.1f}{:>7.1f}{:>7.1f}{:>7.1f}\n"\
					.format(l['index'],l['res_nb'],l['chain'],l['aa'],l['tco'],l['kappa'],l['alpha'],l['phi'],l['psi'],l['x-ca'],l['y-ca'],l['z-ca']))
	else:
		print(header,descp,sep="")
		for i in range(0,len(dssp)):
			l = dssp[i]
			print("{:>5d}{:>5d}{:>2s}{:>2s}{:>2s}{:>3s}{:>1s}{:>1s}"\
				.format(l['index'],l['res_nb'],l['chain'],l['aa'],l['structure'],l['3-turns'],l['4-turns'],l['5-turns']))	
			#print("{:>5d}{:>5d}{:>2s}{:>2s}{:>9.3f}{:>6.1f}{:>6.1f}{:>6.1f}{:>6.1f}{:>7.1f}{:>7.1f}{:>7.1f}"\
			#	.format(l['index'],l['res_nb'],l['chain'],l['aa'],l['tco'],l['kappa'],l['alpha'],l['phi'],l['psi'],l['x-ca'],l['y-ca'],l['z-ca']))
