#!/usr/bin/python

import sys, re, numpy, gzip
import jkgenome
from gzip  import GzipFile


class segInfo:

	def __init__(self,seg):
		
		self.seg = seg
		self.staOffset,self.endOffset = map(int,seg[1].split('..'))
		self.span = self.endOffset - self.staOffset + 1
		self.numMatch = int(re.search('matches:([0-9]*),',seg[3]).group(1))
                self.splice = True if 'splice_' in seg[3] else False
		self.len = len(seg[0])

		rm = re.match('([+-])([^:]+):([0-9]+)\.\.([0-9]+)',seg[2])

		self.chrom = rm.group(2)
		self.strand = rm.group(1)

		if self.strand == '+':
			self.segSta = int(rm.group(3))
			self.segEnd = int(rm.group(4))
		else:
			self.segSta = int(rm.group(4))
			self.segEnd = int(rm.group(3))

		if len(seg) > 4:
			self.mapq = int(re.search('mapq:([0-9]+)', seg[4]).group(1))

		if self.span != 0:
			self.percMatch = float(self.numMatch) / self.span * 100. # deprecated
		else:
			self.percMatch = 0

		self.numMismatch = self.span - self.numMatch # deprecated

		rm = re.search('label_[12]:([^,\t]*)',seg[3])
		if rm:
			self.label = rm.group(1)
		else:
			self.label = ''

		rm = re.search('sub:([0-9]+)', seg[3])
		if rm:
			self.nSub = int(rm.group(1))
		else:
			rm = re.search('sub:[0-9]+\+[0-9]+=([0-9]+)', seg[3])
			if rm:
				self.nSub = int(rm.group(1))
			else:
				self.nSub = 0

		rm = re.search('start:([0-9]+)\.\.', seg[3])
		if rm:
			self.nClipS = int(rm.group(1))
		else:
			self.nClipS = 0

		rm = re.search('\.\.ins:([0-9]+),', seg[3])
		if rm:
			self.nIns = int(rm.group(1))
		else:
			self.nIns = 0

		rm = re.search('\.\.del:([0-9]+),', seg[3])
		if rm:
			self.nDel = int(rm.group(1))
		else:
			self.nDel = 0

		rm = re.search('\.\.(end|term):([0-9]+),', seg[3])
		if rm:
			self.nClipE = int(rm.group(2))
		else:
			self.nClipE = 0

#		rm = re.search('donor:', seg[3])
#		if rm:
#			self.donor = True
#		else:
#			self.donor = False
#
#		rm = re.search('acceptor:', seg[3])
#		if rm:
#			self.acceptor = True
#		else:
#			self.acceptor = False

	def __print__(self):
		print self.seg

	def toCIGAR_trans(self):
		strand = self.seg[2][0]
		(pos1, pos2) = re.search('([0-9]+)\.\.([0-9]+)', self.seg[1]).groups()
		rm = re.search('(start|term):([0-9]+)\.\.', self.seg[3])
		if rm:
			start = int(rm.group(2))
		else:
			start = -1
		rm = re.search('(end|term):([0-9]+),', self.seg[3])
		if rm:
			end = int(rm.group(2))
		else:
			end = -1
		match = int(pos2) - int(pos1) + 1
		if start >= 0 and end < 0: ## first half
			clip = len(self.seg[0]) - int(pos2)
			if start > 0:
				cigar = str(start) + 'S'
			else:
				cigar = ''

			if strand == '-':
				cigar = str(clip) + 'H' + str(match) + 'M' + cigar
			else:
				cigar = cigar + str(match) + 'M' + str(clip) + 'H'
			clip = -1 * clip
		elif start < 0 and end >= 0: ## second half
			cigar = str(int(pos1) - 1) + 'H'
			if strand == '-':
				cigar = str(match) + 'M' + cigar
				if end > 0:
					cigar = str(end) + 'S' + cigar
			else:
				cigar = cigar + str(match) + 'M'
				if end > 0:
					cigar = cigar + str(end) + 'S'
			clip = int(pos1) - 1
		return (cigar, clip)


	def toCIGAR(self, last=False):
		strand = self.seg[2][0]
		rm = re.search('(start|term):([0-9]+)\.\.', self.seg[3])
		if rm:
			start = int(rm.group(2))
		else:
			start = -1
		if len(self.seg) > 4 and start < 0:
			start = int(re.search('([0-9]+)\.\.[0-9]+', self.seg[1]).group(1)) - 1
		rm = re.search('del:([0-9]+),', self.seg[3])
		if rm:
			deletion = int(rm.group(1))
		else:
			deletion = 0
		rm = re.search('ins:([0-9]+),', self.seg[3])
		if rm:
			insertion = int(rm.group(1))
		else:
			insertion = 0
		rm = re.search('splice_dist_2:([0-9]+)', self.seg[3])
		if rm:
			splice_dist_2 = int(rm.group(1))
		else:
			splice_dist_2 = 0
		rm = re.search('(end|term):([0-9]+),', self.seg[3])
		if rm:
			end = int(rm.group(2))
		else:
			end = -1
		rm = re.search('([0-9]+)\.\.([0-9]+)', self.seg[1])
		if last and end < 0:
			end = len(self.seg[0]) - int(rm.group(2))
		seg_len = int(rm.group(2)) - int(rm.group(1)) + 1 + start + end
		match = seg_len - start - end
		cigar = ''
		if strand == '+':
			if start > 0:
				cigar = str(start) + 'S'
			if match > 0:
				cigar = cigar + str(match) + 'M'
			if deletion > 0:
				cigar = cigar + str(deletion) + 'D'
			if insertion > 0:
				cigar = cigar + str(insertion) + 'I'
			if splice_dist_2 > 0:
				cigar = cigar + str(splice_dist_2) + 'N'
			if end > 0:
				cigar = cigar + str(end) + 'S'
		else:
			if start > 0:
				cigar = str(start) + 'S'
			if match > 0:
				cigar = str(match) + 'M' + cigar
			if deletion > 0:
				cigar = str(deletion) + 'D' + cigar
			if insertion > 0:
				cigar = str(insertion) + 'I' + cigar
			if splice_dist_2 > 0:
				cigar = str(splice_dist_2) + 'N' + cigar
			if end > 0:
				cigar = str(end) + 'S' + cigar
		return cigar

class seqMatch:

	def __init__(self,segL): # take newline- and tab-delimited list
		'''
		__init__
		'''

		self.segL = segL
		self.locusL = [jkgenome.locus(s[2]) for s in segL]

		self.segObjL = self.getSegInfo()

	def getSegInfo(self):

		return [segInfo(seg) for seg in self.segL]

#	def mergedLocusL(self,gap=10):
#
#		return jkgenome.mergeLoci(self.locusL, gap)

	def pairInfo(self):

		insertLen, pairType = None, None

		if len(self.segL[0]) >= 6:

			infoL = self.segL[0][5].split(',')

			insertLen = int(infoL[1].split(':')[1])

			if len(infoL) >= 3:
				pairType = infoL[2].split(':')[1]

		return insertLen, pairType

	def score(self):

		return int(re.search('align_score:([0-9]*)',self.segL[0][4]).group(1))

	def isSpliced(self):

		return True in [seg.splice for seg in self.segObjL]

	def spliceJuncL(self,wrtIntron=False):

		juncL = []

		for i in range(len(self.segL)-1):

#                        # for debugging: neither sense? nor antisense? no ambiguous strand in GSNAP
#                        if re.search('splice_',self.segL[i][3]):
#                            mo = re.search('dir:([^,]+)',self.segL[i][3])
#                            if not mo or mo.group(1) not in ('sense','antisense'):
#                                print self.segL[i][3]
#                                raise Exception

			if not (re.search('\.\.donor:',self.segL[i][3]) or re.search('\.\.acceptor:',self.segL[i][3])):
				continue

			direction = re.search('dir:([^,\t]*)', self.segL[i][3]).group(1)

			bp1 = re.match('([+-])([^:]+):[0-9]+..([0-9]+)',self.segL[i][2])
			bp2 = re.match('([+-])([^:]+):([0-9]+)..[0-9]+',self.segL[i+1][2])

			bp1 = [bp1.group(1),bp1.group(2),int(bp1.group(3))]
			bp2 = [bp2.group(1),bp2.group(2),int(bp2.group(3))]

			if wrtIntron:
				bp1[2] += 1 if bp1[0]=='+' else -1
				bp2[2] += -1 if bp2[0]=='+' else 1
	
			if (bp1[0],direction) in (('+','sense'),('-','antisense')):
				trans_strand1 = '+'
			elif (bp1[0],direction) in (('+','antisense'),('-','sense')):
				trans_strand1 = '-'
			else:
				raise Exception

			if (bp2[0],direction) in (('+','sense'),('-','antisense')):
				trans_strand2 = '+'
			elif (bp2[0],direction) in (('+','antisense'),('-','sense')):
				trans_strand2 = '-'
			else:
				raise Exception

			if direction=='sense':
				key = [trans_strand1,]+bp1[1:]+[trans_strand2,]+bp2[1:]
			elif direction=='antisense':
				key = [trans_strand2,]+bp2[1:]+[trans_strand1,]+bp1[1:]
			else:
				raise Exception
	
			juncL.append(tuple(key))

		return juncL


	def numMatch(self,seq_read):

		return sum(self.posProfile(seq_read)) - len(self.segL) + 1
		#return sum([int(re.search('matches:([0-9]*)',seg[3]).group(1)) for seg in self.segL])

	def getPenalties(self):

		nSub = sum([s.nSub for s in self.segObjL])
		nIns = sum([s.nIns for s in self.segObjL[:-1]])
		nDel = sum([s.nDel for s in self.segObjL[:-1]])
		nClipS = self.segObjL[0].nClipS
		nClipE = self.segObjL[-1].nClipE

		return {'nSub':nSub, 'nIns':nIns, 'nDel':nDel, 'nClipS':nClipS, 'nClipE':nClipE}

	def posProfile(self,seq_read):

		seqLen = len(seq_read)

		profile = [0,]*seqLen
		
		for seg in self.segL:

			seq_match = seg[0]

			for p in range(min(seqLen,len(seq_match))):

				if seq_match[p] == '-':
					continue

				profile[p] = int(seq_match[p].isupper() and seq_read[p]!='N')

		return profile
	
	def toCIGAR(self):
		segInfoL = self.getSegInfo()
		(strand, rname, pos1, pos2) = re.search('([\+\-])(.*):([0-9]+)\.\.([0-9]+)', segInfoL[0].seg[2]).groups()
		pos = min(pos1, pos2)
		if len(segInfoL) == 1:
			cigar = segInfoL[0].toCIGAR(True)
		else:
			cigar = segInfoL[0].toCIGAR()
		prev_cigar = cigar
		index = 0
		for segInfo in segInfoL[1:]:
			index = index + 1
			if index == (len(segInfoL) - 1):
				final = True
			else:
				final = False
			rm = re.search('([\+\-])(.*):([0-9]+)\.\.([0-9]+)', segInfo.seg[2]).groups()
			if pos == 0 or pos > min(rm[2], rm[3]):
				pos = min(rm[2], rm[3])
			if strand == '-':
				dist = int(pos2) - int(rm[2]) - 1
			else:
				dist = int(rm[2]) - int(pos2) - 1
			pos1 = rm[2]
			pos2 = rm[3]
			cur_cigar = segInfo.toCIGAR(final)
			if strand == '-':
				if dist > 0 and 'D' not in prev_cigar and 'I' not in prev_cigar and 'N' not in prev_cigar:
					cigar = cur_cigar + str(dist) + 'N' + cigar
				else:
					cigar = cur_cigar + cigar
			else:
				if dist > 0 and 'D' not in prev_cigar and 'I' not in prev_cigar and 'N' not in prev_cigar:
					cigar = cigar + str(dist) + 'N' + cur_cigar
				else:
					cigar = cigar + cur_cigar
		return cigar


class seqRead:
	
	def __init__(self,l): # take newline- and tab-delimited list

		self.raw = l
		self.nLoci = int(l[0][1].split(' ')[0])

		if ' ' in l[0][1]:
			self.pairRel = l[0][1][l[0][1].find(' ')+1:]
		else:
			self.pairRel = ''

	def seq(self):
		return self.raw[0][0][1:]

	def rawText(self):
		return '\t'.join(self.raw[0][:2])+'\n' + '\n'.join(['\t'.join(t) for t in self.raw[1:]])+'\n'

	def matchL(self):
		return [seqMatch([l.split('\t') for l in m.lstrip().split('\n,')]) for m in '\n'.join(['\t'.join(t) for t in self.raw[1:]]).split('\n ')]

	def pairInfo(self):
		return self.matchL()[0].pairInfo()

	def qual(self):
		return self.raw[0][2]
	
	def rid(self):
		return self.raw[0][3]
	
class gsnapFile(file):

	def __init__(self, fileName, paired=True):

		self.paired = paired
		if fileName[-3:] == '.gz':
			self.gzip = True
			self.gzfile = gzip.open(fileName)
		else:
			self.gzip = False

		return super(gsnapFile,self).__init__(fileName)
	
	def next(self):

		l1 = []

		while 1:

			if self.gzip:
				line = self.gzfile.next()
			else:
				line = file.next(self)

			if line=='\n':
				break

			l1.append(line[:-1].split('\t'))
				
		if self.paired:

			l2 = []

			while 1:

				if self.gzip:
					line = self.gzfile.next()
				else:
					line = file.next(self)

				if line=='\n':
					break

				l2.append(line[:-1].split('\t'))
					
			return seqRead(l1), seqRead(l2)

		else:

			return seqRead(l1)
