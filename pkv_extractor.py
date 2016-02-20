"""parse_kvp parses given query and extracts key-value pair from it and use them to build solr query.
Arguments:
    @jsonfile: .json file which has all the category prefix, regex and postfix.
    @query: query is the query done by user.
    @pp: it is given category for which query has to parse.

Returns:
    Solr query with all pasred kvp and all possible combinations.

"""
# returning dictionary has following symentics : {'kv_pairs':'(parsed kv pairs joined with +AND+)'}
import re
import json
import itertools
def parse_kvp(jsonfile, query, pp):
    print "** parse_kvp is called**"
    regex_dict = {}
    parsed_kvp = {}
    kvp_result_list = []
    kvp_combination_list = []
    kv_pairs= ""
    #fashion_list is just for testing remove it once query is build properly.
    # fashion_list = ['shoe', 'boot', 'fashion', 'cloth', 'dress', 'shirt', 'sare']
    # print materials
    with open(jsonfile) as data_file:
        data = json.load(data_file)
        for k, v in data['kv_regex'].items():
            # Here is k is category and v is dict of all the regex of that category for kv pairs.
            if pp['category'] == k:
                for x, y in v.items():
                    # x is the key and  y is list of [perfix,regex,postfix]
                    reg_val_string = y[1].decode('string_escape')
                    value_regex = re.compile(reg_val_string, re.IGNORECASE)
                    if value_regex.search(query):
                        #code to support multiple kvp combination.
                        if len(y) == 4 and y[3] == "True":
                            #kvp_combination is creating list of all possible kvps and 
                            #constructing query with ORing the kvps
                            kvp_combination = list(itertools.product(y[0], y[2]))
                            print kvp_combination
                            for k, v in kvp_combination:
                                #Resolution query is for laptop resolution.
                                #CHECKME: Check if this query is causing any other query to break.
                                if x == 'Resolution':
                                    # kv_pairs = y[0]+ value_regex.search(query).group(2)+" X "+value_regex.search(query).group(3)+y[2]
                                    kvp_combination_list.append("\""+k+ value_regex.search(query).group(2)+" X "+value_regex.search(query).group(3)+v+"\"")
                                else:
                                    kvp_combination_list.append("\""+k+value_regex.search(query).group(1)+v+"\"")
                            kvp_result_list.append("("+"+OR+".join(kvp_combination_list)+")")
                            kvp_combination_list = []
                        else:
                            try:
                                kv_pairs =  y[0]+value_regex.search(query).group(1)+y[2]
                                if x == 'Operating System':
                                    kv_pairs = y[0]+value_regex.search(query).group(1).capitalize()+y[2]            
                                # if x == 'Resolution':
                                #     kv_pairs = y[0]+ value_regex.search(query).group(2)+" X "+value_regex.search(query).group(3)+y[2]
                            except:
                                if x == 'Hard Disk Capacity':
                                    if 'tb' in query.lower():
                                        kv_pairs = y[0]+value_regex.search(query).group(3)+y[2][1]
                                    else:
                                        kv_pairs = y[0]+value_regex.search(query).group(1)+y[2][0]            
                            kvp_result_list.append("\""+kv_pairs+"\"")
    parsed_kvp['kv_pairs'] = "("+"+AND+".join(kvp_result_list)+")"
    #If no kv pair found in query 
    if len(kvp_result_list) == 0:
        parsed_kvp= {}
    return parsed_kvp

pp ={}
pp['category'] = 'laptop'
q ="laptop with 4gb ram and 2tb harddisk windows os 64 bit version"
print parse_kvp('kv_pairs.json', q, pp)
