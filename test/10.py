#!/usr/bin python 
import string
import vcf


"""
The most important access method
@arg baseName: the portion of the file name shared by the plink files to be parsed
@arg binary: set to True if .bed, .bim and .fam files are being parsed, rather than .ped and .map
@arg individuals: A list specifying which individuals should be included from the file
@returns: A list of PyVCF _Record structures, one for each marker in the plink data,
	containing all the individuals specified in the @individuals argument, or all the
	individuals in the plink file if individuals is None.
"""
def doParse(baseName, binary=False, individuals=None):
	records = list();
	if binary:
		parseBinary(baseName, records, individuals);
	else:
		parseText(baseName, records, individuals);
	return records;

"""
Used by the function parseBinary to count and load individual id's into a list
@arg famFile: File object representing plink .fam file
@arg individuals: A list to store all the individuals in the file
@returns: The number of individuals in the file

@fails if: famFile is not a file
@fails if: individuals is not a list
"""
def __loadIndividuals(famFile, individuals):

	assert(type(famFile) is file);
	assert(type(individuals) is list);

	indNum = 0;

	famLine = famFile.readline();
	while famLine != "":
		# skip comments and blank lines
		if famLine[0] != '#' and famLine[0] != '\n':
			indData = string.split(famLine);
			indId = indData[0] + " " + indData[1];
			individuals.append(indId);
			
			indNum += 1;
		famLine = famFile.readline();
	
	return indNum;

"""
The first two bytes of a Plink .bed files must follow a certain format.  This function checks
to make sure that they do, raising a PlinkFormatException otherwise
There are also two possible formats for .bed files, snp-major and individual-major.
So far, this application only handles snp-major, so this function returns true if the .bed file
is in snp-major format
"""
def __checkFileFormat(bedFile):
	#The first two bytes of all correctly formatted .bed files are the same
	byte = bedFile.read(1);
	firstChar = str(bin(ord(byte)));
	byte = bedFile.read(1);
	secondChar = str(bin(ord(byte)));

	if firstChar != "0b1101100" or secondChar != "0b11011":
		raise PlinkFormatException('Binary file '+str(bedFile)+' is missing characteristic first two bits', bedFile);

	byte = bedFile.read(1);
	return str(bin(ord(byte))) == "0b1";

"""
Called by parseBinary() to converty each @byte into an easily managable string
@returns the string representation of the @byte passed to it
"""
def __binaryToString(byte):
	raw = str(bin(ord(byte)));
	processed = string.replace(raw, "0b", "");

	# invert string
	processed = processed[::-1];
	
	# append 0's to make processed string the right length
	missingDigitNum = 8 - len(processed);
	while missingDigitNum > 0:
		missingDigitNum -= 1;
		processed += "0";

	return processed;

"""
The Plink .bed file doesn't store genotypes per se.  Rather, for each marker it stores whether an individual
is homozygous for the major allele, heterozygous, homozygous for the minor allele, or missing.  The major and
minor allele are stored in the .bim file
@arg binCode: the two character code stored for this individual in the .bed file
@arg ref: the major allele as stored in the .bim file
@arg alt: the minor allele as stored in the .bim file

@returns: the string representation of the individuals genotype at this marker as the PyVCF _Record
	structure would format it
"""
def __getBinaryGenotype(binCode, ref, alt):
	if binCode == "11":
		return ref + "/" + ref;
	elif binCode == "01":
		return ref + "/" + alt;
	elif binCode == "00":
		return alt + "/" + alt;
	elif binCode == "10":
		return "./.";
	else:
		return "ERROR";

"""
The function that parses binary plink files (.bed, .bim, .fam) to PyVCF _Record structures
@arg baseName: the part of the filename shared by all three files
@arg records: A list in which the _Record structures will be stored, must already be instantiated
@arg selectIndividuals: A list of individual ID's that is a subset of those individuals in the file
	individuals in @selectIndividuals but not in the file will have all their genotypes set to missing

@raises PlinkFormatException: if .bed file is not in SNP-major mode (any .bed file generated by the plink
	--make-bed command will be in SNP-major mode; it would have been modified manually to be in non-SNP-major mode)

@fails if: records is not a list
@fails if: one of the files does not exist, <baseName>.bed, <baseName>.bim or <baseName>.fam
"""
def parseBinary(baseName, records, selectIndividuals):

	assert(type(records) is list);
	
	bedFile = open(baseName + ".bed", "rb");
	bimFile = open(baseName + ".bim", "rb");
	famFile = open(baseName + ".fam", "rb");

	allIndividuals = list();
	indNum = __loadIndividuals(famFile, allIndividuals);

	includedIndividuals = [];
	if selectIndividuals != None:
		includedIndividuals = selectIndividuals;
	else:
		includedIndividuals = allIndividuals;

	# individualCols is the column number associated with an individual ID
	# an individual will have the same column number accross all markers in the file
	individualCols = {};
	colNum = 0;
	for ind in includedIndividuals:
		individualCols[ind] = colNum;
		colNum += 1;

	if not __checkFileFormat(bedFile):
		raise PlinkFormatException('Binary file is not in requisite SNP major mode', bedFile);

	bimLine = bimFile.readline();
	while bimLine != "":
		# ignore comments and blank lines (these shouldn't be present in file generated using --make-bed)
		if bimLine[0] == '#' or bimLine[0] == '\n':
			bimLine = bimFile.readline();
			continue;
		markerData = string.split(bimLine);
		chr = markerData[0];
		id = markerData[1];
		pos = int(markerData[3]);
		alt = markerData[4];
		ref = markerData[5];

		# the default missing characer for plink is '0'
		# for vcf files it is '.'
		if alt == '0':
			alt = '.';
		if ref == '0':
			ref = '.';

		qual = None;
		filter = None;
		info = None;
		format = "GT";

		# the .bed file stores four individuals per byte
		# the last byte may contain less than four, 
		# preceded by senseless 0's
		bytesToReadFromBedFile = indNum / 4;
		if indNum % 4 != 0:
			bytesToReadFromBedFile += 1;
		textRead = "";
		bytesRead = 0;
		while bytesRead < bytesToReadFromBedFile:
			textRead += __binaryToString(bedFile.read(1));
			bytesRead += 1;

		genotypes = {};
		startSlice = 0;
		endSlice = 2;
		for ind in allIndividuals:
			# textRead is a string of one's and zero's, each two characters
			# correspoding to the genotype of an individual
			indString = textRead[startSlice:endSlice];
			genotypes[ind] = indString;
			startSlice += 2;
			endSlice += 2;

		samples = [];
		for ind in includedIndividuals:
			if ind in genotypes:
				samples.append(__getBinaryGenotype(genotypes[ind], ref, alt));
			else:
				samples.append('./.');

		#individualCols is a dictionary of unique ID's : column number
		# The unique ID represents an individual; the column number is the index of the list 'samples'
		# that holds the genotype for the individual
		newRecord = vcf.model._Record(chr, pos, id, ref, alt, qual, filter, info, format, individualCols, samples);
		records.append(newRecord);	

		bimLine = bimFile.readline();

	bedFile.close();
	bimFile.close();
	famFile.close();
"""
@arg genotypeData: An ordered list of all the alleles for one individual (i.e. a list of the columns in one line of
	the .ped file, minus the first six columns)
@returns: An ordered list of all the genotypes for one individual
@raises PlinkFormatException: if the .ped file from which genotypeData came doesn't have an even number of columns
"""
def __parseTextGenotypeData(genotypeData):
	genotypes = [];
	dataCount = len(genotypeData);
	if dataCount % 2 != 0:
		raise PlinkFormatException("A line in the .ped file doesn't have the correct number of columns");

	parsedData = 0;
	while parsedData < dataCount:
		allele1 = genotypeData[parsedData];
		parsedData += 1;
		allele2 = genotypeData[parsedData];
		parsedData += 1;

		# in plink format, 0 is the default missing genotype character
		# in VCF format, it is a period
		if allele1 == '0':
			allele1 = '.';
		if allele2 == '0':
			allele2 = '.';

		genotypes.append(allele1 + "/" + allele2);


	return genotypes;

"""
The function that parses text plink files (.ped and .map) to PyVCF _Record structures
@arg baseName: the part of the filename shared by both files
@arg records: A list in which the _Record structures will be stored, must already be instantiated
@arg selectIndividuals: A list of individual ID's that is a subset of those individuals in the file
	individuals in @selectIndividuals but not in the file will have all their genotypes set to missing

@fails if: records is not a list
@fails if: one of the files does not exist, <baseName>.ped, <baseName>.map
"""
def parseText(baseName, records, selectIndividuals):	

	assert(type(records) is list);

	pedFile = open(baseName + ".ped");
	mapFile = open(baseName + ".map");

	allIndividuals = [];
	individualGenotypes = {};
	pedLine = pedFile.readline();
	while pedLine != "":
		# ignore comments and blank lines
		if pedLine[0] == '\n' or pedLine[0] == '#':
			pedLine = pedFile.readline();
			continue;

		pedData = string.split(pedLine);
		
		individual = pedData[0] + " " + pedData[1];

		# the first six columns are data about the individual
		# the remaining columns are alleles
		genotypeData = pedData[6:];
		genotypes = __parseTextGenotypeData(genotypeData);

		individualGenotypes[individual] = genotypes;
		allIndividuals.append(individual);

		pedLine = pedFile.readline();

	includedIndividuals = [];
	if selectIndividuals != None:
		includedIndividuals = selectIndividuals;
	else:
		includedIndividuals = allIndividuals;

	individualCols = {};
	colNum = 0;
	for ind in includedIndividuals:
		individualCols[ind] = colNum;
		colNum += 1;

	markerNum = 0;
	mapLine = mapFile.readline();
	while mapLine != "":
		# ignore comments and blank lines
		if mapLine[0] == "\n" or mapLine[0] == "#":
			mapLine = mapFile.readline();
			continue;

		mapData = string.split(mapLine);
		chr = mapData[0];
		id = mapData[1];
		pos = int(mapData[3]);

		qual = None;
		filter = None;
		info = None;
		format = "GT";

		samples = [];
		for individual in includedIndividuals:
			if individual in individualGenotypes:
				samples.append(individualGenotypes[individual][markerNum]);
			else:
				# individuals specified in @selectIndividuals, but not in the file
				# will be given a missing genotype
				samples.append('./.');

		# variants will be used to determine the major and minor allele for each marker
		variants = {};
		for individual in allIndividuals:
			genotype = individualGenotypes[individual][markerNum];

			alleles = string.split(genotype, "/");
			for allele in alleles:
				if allele in variants:
					count = variants[allele];
					count += 1;
					variants[allele] = count;
		
				else:
					variants[allele] = 1;
		
		refFreq = -1;
		ref = ".";
		alt = ".";
		for variant in variants.iterkeys():
			frequency = variants[variant];
			if frequency > refFreq:
				alt = ref;
				ref = variant;
				refFreq = frequency;
			else:
				alt = variant;

		newRecord = vcf.model._Record(chr, pos, id, ref, alt, qual, filter, info, format, individualCols, samples);
		records.append(newRecord);

		markerNum += 1;
		mapLine = mapFile.readline();


"""
This method is called if plinkToVCFParse is called alone.

USAGE: python plinkToVCFParse.py [-b] <file_base_name>

where -b specifieds that the file is binary and
<file_base_name> is shared by the files to be parsed (i.e.
'python plinkToVCFParse.py data' will attempt to parse
data.ped and data.map, whereas
'python plinkToVCFParse.py -b data' will attempt to parse
data.bed, data.bim and data.fam

This option does not allow the user to specify of subset of
individuals in the PLINK formatted file, but will parse all
of the individuals instead.
"""
def main():
	import sys;
	result = None;
	if len(sys.argv) == 2:
		try:
			result = doParse(sys.argv[1]);
		except IOError:
			print("One of the files specified doesn't exist");
	elif len(sys.argv) == 3:
		try:
			result = doParse(sys.argv[2], True);
		except IOError:
			print("One of the files specified doesn't exist");
	else:
		print("USAGE: python ParsePlinkFileIntoVcfFormat [-b] <file_base_name>"); 
		sys.exit(1);

	if result != None:
		for record in result:
			print(str(record));
			for sample in record.samples:
				print("\t" + str(sample));

if __name__ == "__main__":
	main();

class PlinkFormatError(Exception):
	def __init__(self, value):
		self.value = value;
	def __str__(self):
		return repr(self.value);
