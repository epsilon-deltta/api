class variant:
    def __init__(self,chrN=None,pos=None,ref=None,alt=None):
        pass
    def set_var_str(self,seq=''): #"11:1234567 a>g"
        pass
    def set_var_pos(self,):        # 11,1234567,a,g
        pass
    def set_var_ptype(self,transID,loc)      :
        pass
    def set_var_ctype(self,transID,ref_amino,alt_amino,pos):
        pass
amino = {}
print("===")
amino['a'] = {'codons':['gcu','gcc','gca','ggg'],'name':'alanine'      ,'3-letter':'ala','desc':''}
amino['c'] = {'codons':['ugu','ugc']            ,'name':'cysteine'     ,'3-letter':'cys','desc':''}
amino['d'] = {'codons':['gau','gac']            ,'name':'aspatic_acid' ,'3-letter':'asp','desc':''}
amino['e'] = {'codons':['gcu','gcc','gca','ggg'],'name':'glutamic_acid','3-letter':'glu','desc':''}
amino['f'] = {'codons':['uuu','uuc']            ,'name':'phenylalanine','3-letter':'phe','desc':''}
amino['g'] = {'codons':['gcu','gcc','gca','ggg'],'name':'glycine'      ,'3-letter':'gly'}
amino['h'] = {'codons':['gcu','gcc','gca','ggg'],'name':'histidine'    ,'3-letter':'his'}
amino['i'] = {'codons':['auu','auc','aua']      ,'name':'isoleucine'   ,'3-letter':'ile'}
amino['k'] = {'codons':['gcu','gcc','gca','ggg'],'name':'lysine'       ,'3-letter':'lys'}
amino['l'] = {'codons':['uua','uug','cuu','cuc','cua','cug'],'name':'leucine','3-letter':'leu','desc':''}

amino['m'] = {'codons':['aug'],                  'name':'methionine'     ,'3-letter':'met','desc':'start' }
amino['n'] = {'codons':['aau','aac']            ,'name':'asparagine'     ,'3-letter':'asn','desc':''}
amino['p'] = {'codons':['ccu','ccc','cca','ccg'],'name':'proline'        ,'3-letter':'pro','desc':''}
amino['q'] = {'codons':['caa','cag']            ,'name':'glutamine'      ,'3-letter':'gln','desc':''}
amino['r'] = {'codons':['aga','agg']            ,'name':'argineine'      ,'3-letter':'arg','desc':''}
amino['s'] = {'codons':['ucu','ucc','uca','ucg'],'name':'serine'         ,'3-letter':'ser','desc':''}
amino['t'] = {'codons':['acu','acc','aca','acg'],'name':'threonine'      ,'3-letter':'thr','desc':''}
amino['v'] = {'codons':['guu','guc','gua','gug'],'name':'valine'         ,'3-letter':'val','desc':''}
amino['w'] = {'codons':['ugg']                  ,'name':'tryptophan'     ,'3-letter':'trp','desc':''}
amino['y'] = {'codons':['uau','uac']            ,'name':'tyrosine'       ,'3-letter':'tyr','desc':''}
amino['stop' ] = {'codons':['uaa','uag','uga']}
amino['start'] = {'codons':['aug']}

class amino_acid:
    amino = {}

    amino['a'] = {'codons':['gcu','gcc','gca','ggg'],'name':'alanine'      ,'3-letter':'ala','desc':''}
    amino['c'] = {'codons':['ugu','ugc']            ,'name':'cysteine'     ,'3-letter':'cys','desc':''}
    amino['d'] = {'codons':['gau','gac']            ,'name':'aspatic_acid' ,'3-letter':'asp','desc':''}
    amino['e'] = {'codons':['gcu','gcc','gca','ggg'],'name':'glutamic_acid','3-letter':'glu','desc':''}
    amino['f'] = {'codons':['uuu','uuc']            ,'name':'phenylalanine','3-letter':'phe','desc':''}
    amino['g'] = {'codons':['gcu','gcc','gca','ggg'],'name':'glycine'      ,'3-letter':'gly'}
    amino['h'] = {'codons':['gcu','gcc','gca','ggg'],'name':'histidine'    ,'3-letter':'his'}
    amino['i'] = {'codons':['auu','auc','aua']      ,'name':'isoleucine'   ,'3-letter':'ile'}
    amino['k'] = {'codons':['gcu','gcc','gca','ggg'],'name':'lysine'       ,'3-letter':'lys'}
    amino['l'] = {'codons':['uua','uug','cuu','cuc','cua','cug'],'name':'leucine','3-letter':'leu','desc':''}

    amino['m'] = {'codons':['aug'],                  'name':'methionine'     ,'3-letter':'met','desc':'start' }
    amino['n'] = {'codons':['aau','aac']            ,'name':'asparagine'     ,'3-letter':'asn','desc':''}
    amino['p'] = {'codons':['ccu','ccc','cca','ccg'],'name':'proline'        ,'3-letter':'pro','desc':''}
    amino['q'] = {'codons':['caa','cag']            ,'name':'glutamine'      ,'3-letter':'gln','desc':''}
    amino['r'] = {'codons':['aga','agg']            ,'name':'argineine'      ,'3-letter':'arg','desc':''}
    amino['s'] = {'codons':['ucu','ucc','uca','ucg'],'name':'serine'         ,'3-letter':'ser','desc':''}
    amino['t'] = {'codons':['acu','acc','aca','acg'],'name':'threonine'      ,'3-letter':'thr','desc':''}
    amino['v'] = {'codons':['guu','guc','gua','gug'],'name':'valine'         ,'3-letter':'val','desc':''}
    amino['w'] = {'codons':['ugg']                  ,'name':'tryptophan'     ,'3-letter':'trp','desc':''}
    amino['y'] = {'codons':['uau','uac']            ,'name':'tyrosine'       ,'3-letter':'tyr','desc':''}
    amino['stop' ] = {'codons':['uaa','uag','uga']}
    amino['start'] = {'codons':['aug']}
    def getAmino(amin):
        return amino[amin]
    # def get_cases_amino_change(ref_amino,alt_amino,n):
    #     return [variant0,variant1,...]
    # def convert_to_gene():
    #     return pos,chr
    # def convert_to_trans():
    #     return gene,trns_id,loc
    # def validate_amino():
    #     count = 0
    #     for ami in amino.keys():
    #         for codon in amino[ami]['codons']:
    #             print(codon)
    #             count += 1
    #     print(count)
    # def test():
    #     print(a)

