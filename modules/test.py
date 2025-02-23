import jkgenome as jk
import os
import time
import tensorflow as tf
#cd /home/ypil/api-test/modules python test.py
print("=====start")
def spliceAI_run_str_test(seq='11:108236168 A>C'):
    result = jk.spliceAI_run_str(seq)
    return result
# result = jk.spliceAI('11:108241292-108241292') #output 01
# output ex) [{'chrN': '11', 'pos': 108236168, 'ref': 'A', 'alt': 'C', 'geneName': 'ATM', 'score': {'AG': 0.0, 'AL': 0.0, 'DG': 0.02, 'DL': 0.01}, 'relPos': {'AG': 5, 'AL': 2, 'DG': 4, 'DL': -48}} ...
# input chr12:51391349-51391349 //it doesn't work
def spliceai_test(locus_str='chr11:108236168-108236168'):    
    result = jk.spliceAI(locus_str) #output 01
    for x in result:
        print(x)

# input  : 12,51391349,'T','G'
# output :
# {'count': 2, 
#       0:{'transName': 'GALNT6',
#             'strand': '-', 
#            'hexamer': {'5p_exon': -0.9433427732811785, '3p_exon': -3.3507853061596906, '5p_intron': -0.7609967287046513, '3p_intron': -0.29408536662619955}, 
# 	      'type': 'snv', 
#                'mes': {'donor': {'delta': [0.0, 0.0, 0.0, 0.2999999999999998, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final': [0.0, 0.0, 0.0, 7.75, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}, 'acceptor': {'delta': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.09999999999999964, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}}}, 
# 1: {'transName': 'SLC4A8', 'strand': '+', 'hexamer': {'5p_exon': 0.26357736584766656, '3p_exon': -1.519055738781958, '5p_intron': -0.016999846994960266, '3p_intron': -1.7098262852115953}, 'type': 'snv', 'mes': {'donor': {'delta': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}, 'acceptor': {'delta': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'final': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}}}}
def variant_bi2_test():
    result = jk.variant_bi2(12,51391349,'T','G')
    
    return result
def variant_bi2_test_indel():
    result = jk.variant_bi2(11,108236165, 'TTCAG','T')
    # result = jk.variant_bi2(11,108236168 A>AT)
    return result
# output :[( {'transName', 'transID', 'chrom', 'chrNum', 'strand', 'txnSta', 'txnEnd', 'txnLen', 'cdsSta', 'cdsEnd', 'exnList', 'exnLenList', 'exnLen', 'cdsList', 'utr5', 'utr3', 'utr5Len', 'utr3Len', 'cdsLen', 'intron'}
#            ,3796  # position
#            ,'cds' #?    ]
# output [(,,) ,(,,) ...] // each transcription
# (,,) = (dict , pos, 'cds' ?? )
def convertGenome2Trans_test(chrNum='12',gPos=6022032): # genomic pos base1, transcript pos base0
    return jk.convertGenome2Trans(jk.loadBlatOutputByChr(),chrNum,gPos)
# output  : [('chr12', 6022032, '-')]
def convertTrans2Genome_test(transID="NM_000552",transPos=3797):
    result = jk.convertTrans2Genome(jk.loadBlatOutputByID(),transID,transPos)
    return result
# /HDD8/ypil/djg-api-test/modules/data/tools/tabix-0.2.6/tabix /HDD8/ypil/djg-api-test/modules/data/BigFiles/SpliceAI/spliceai_scores.raw.indel.hg38.vcf.gz 11:108236168-10823616
if __name__ == '__main__':
    print("spliceAI_run_str result is ",spliceAI_run_str_test() )
    # print(convertGenome2Trans_test )
    # print(variant_bi2_test_indel())
    # print(jk.convertTrans2Genome(jk.loadBlatOutputByID(),"NM_000552",3797) )
    # spliceai_test('chr12:51391349-51391349')
    # spliceai_test('chr11:108236168-108236168')
    # print(jk.locus("chr11:108236168-108236169+").twoBitFrag())
    # print(jk.locus("12:51391349-51391349+").twoBitFrag())