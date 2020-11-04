import re
import jkgenome as jk
import amino as am
# input : NM_000552.4(VWF):p.Pro1266Gln 
# output : True
def check_transID_p_Type(seq):
    if check_transID_Type(seq):
        return False
    if seq.split(':')[0][0].lower() == 'p':
        return True
# input > output
# input : chr1:1234567890 >False
# input : 1:1234567890 >False
# input : NM_000552.4(VWF):c.3797C>A >True
# input : NM_000552:3797C>A >True
# input : NM_000552:3797
def check_transID_Type(seq):
    # chr1:1234567890 >False
    if seq[:3] == 'chr' :
        return False
    # 1:1234567890 >False
    if bool(re.match(r"\d",seq ) ):
        return False
    return True
# ctype to pos
# input : NM_000552.4(VWF):c.3797C>A 
# input : NM_000552:3797C>A 
# input : NM_000552:3797 
# output : 12:6022032 C>A
def get_transId2pos(seq):
    transID  =  seq.split(':')[0]

    # NM_000552.4(VWF)
    if '.' in transID :
        transID = transID[:transID.find('.')]
    transPos =  re.search(r"(?P<pos>[a-zA-Z]+[.]\d+|\d+)" , seq.split(':')[1] )
    transPos =  transPos.group('pos')

    # c.3797
    if '.' in transPos :
        transPos = transPos[transPos.find('.')+1:]
    # C>A 
    variant  =  seq.split(':')[1][len(transPos):]
    if exist_Variant(variant):
        variant = extract_variant(variant)
    else :
        variant = ''
    # output :[('chr12', 6022032, '-')]
    chrN ,pos, _ =  jk.convertTrans2Genome(transID, int(transPos) )[0]

    position = chrN+":"+str(pos)+' '+variant.upper()
    
    return position.rstrip()
# input  : NM_000552.4(VWF):p.Pro1266Gln  //only snv cases 
# 3798-2 = 3796
# output : [{'seq': '11:108236168 a>g','ref_amino':'','alt_amino':'',"amino_loc":"","amino_pos":''  }]
def get_transId_p2pos(seq='NM_000552.4(VWF):p.Pro1266Gln'):
    # NM_000552.4(VWF)
    # 'p.Pro1266Gln'
    transID  =  seq.split(':')[0]
    # NM_000552
    if '.' in transID :
        transID = transID[:transID.find('.')]    
    
    ptype    =  seq.split(':')[1]
    
    # ('Pro',1266,'Gln')
    pre_amino,amino_num,alt_amino = re.findall(r'([a-zA-Z]+)(\d+)([a-zA-Z]+)',ptype)[0]
    #  c.3796
    amino_c_first   = int(amino_num)*3 -2
    chr, amino_pos_first ,strand = jk.convertTrans2Genome(transID,amino_c_first)[0]
    pre_amino = pre_amino.lower()
    alt_amino = alt_amino.lower()

    # pro == ref_amino 
    if not check_correct_amino(chr, amino_pos_first ,strand ,pre_amino) 
        print("REf amino is not given amino")
        return -1

    amino_codon  = get_amino_codon(chr, amino_pos_first ,strand)
    amino_codon_ = amino_codon
    alt_codons   = am.amino_acid().get_codons(alt_amino)


    snv_cases =[]
    for i in range(3):
        
        for nt in ['u','c','a','g']: #ref alt nt seq

            amino_seq_[i] = nt
            if amino_seq_ in alt_codons:
                case ={}
                case['pos_in_amino'] = i
                case['alt'] = nt

            snv_cases.append(case)
            amino_codon_ = amino_codon
    common_part = { 'transID'  : transID , 
                    'ref_amino':pre_amino,
                    "alt_amino":alt_amino,
                    'ref_codon':amino_codon,
                    'first_pos':chr+':'+str(amino_pos_first)+strand }
    


    alt_amino = alt_amino.lower(chr, amino_pos_first ,strand ,pre_amino)
def get_amino_codon(chr, amino_pos_first ,strand):
    if strand == '+':
        ref_amino = jk.locus('%s:%s-%s%s' % chr, amino_pos_first-1, amino_pos_first+2,'+' )
    else :
        ref_amino = jk.locus('%s:%s-%s%s' % chr, amino_pos_first-3, amino_pos_first  ,'-' )
    ref_amino = ref_amino.twoBitFrag()
    return ref_amino

# def get_amino_change_cases(ref_amino,alt_amino, chr, amino_pos_first ,strand):
    

# input ctype first position c.1233 c.1234 c.1235 중 (pos of c.1233)
def check_correct_amino(chr, amino_pos_first ,strand ,pre_amino):
    if strand == '+':
        ref_amino = jk.locus('%s:%s-%s%s' % chr, amino_pos_first-1, amino_pos_first+2,'+' )
    else :
        ref_amino = jk.locus('%s:%s-%s%s' % chr, amino_pos_first-3, amino_pos_first  ,'-' )
    ref_amino = ref_amino.twoBitFrag()
    
    if ref_amino.lower() == pre_amino.lower():
        return True
    else:
        return False




# input : 12:6022032 C>A
# output: C>A
def extract_variant(seq):
    result = re.search(r'[a-zA-Z]+[\>\<]+[a-zA-Z]+',seq)
    if result is  None:
        return ''
    return result.group(0)
# input  : 12:6022032 C>A
# output : True
def exist_Variant(seq):
    return bool(extract_variant(seq) )


# check_transID_Type("0ca2134")