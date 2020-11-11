from slr import SLR

def main():
    s = SLR()
    s.GOTO()
    s.reduction()


    print ("\n--------------------GRAMMAR--------------------")
    for index, rule in s.rule_dict.items():
        print (index, rule)
    print ("\n--------------------AUGMENTED RULES--------------------")
    for item in s.new_grammar:
        print(item.replace(".",""))
    print("\nTerminals:",s.terminals)
    print("\nNonTerminals:",s.non_terminals)

    print ("\n--------------------STATES--------------------")
    for index, itemsets in s.Items.items():
        print("I[",index,"]=",itemsets)
    print ("\n--------------------GOTO OPERATIONS--------------------")
    for i,value,j in s.shift_list:
        print ("GOTO(I[",i,"],",value,")=I[",j,"]")
    print ("\n--------------------REDUCTION--------------------")
    for i,value,j in s.reduction_list:
        print ("GOTO(I[",i,"],",value,")=",j)

    if s.check_conflict():
        if s.SR != []:
            print("SR conflict")
        for item in s.SR:
            print(item)
        
        if s.RR !=[]:
            print("RR conflict")
            for item in s.RR:
                print (item)
        exit(0)
    else:
        print("\nNO CONFLICT\n")
    s.action_list.extend(s.shift_list)
    s.action_list.extend(s.reduction_list)

    string = input("\n\nEnter String: ")

    try:
        if string[-1] != "$":
            string = string + "$"
    except:
        print("InputError")
        exit(0)
    print("\nTest String: ", string)
    result = s.test_simulation(string)
    if result == 1:
        print("---ACCEPTED---")
    else:
        print("---NOT ACCEPTED---")
    
    return 0

if __name__ == '__main__':
    main()