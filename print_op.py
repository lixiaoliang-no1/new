from prettytable import PrettyTable
print(
"""
                *********           *********               
            *****************   *****************           
          *****************************************         
         *******************************************        
        *********************************************                                  
        ****************welcome my mysql*************     
         *******************************************        
          *****************************************                
            *************************************                      
              *********************************             
                *****************************               
                  *************************                 
                    *********************                   
                       ***************                      
                          *********                         
                             ***                            
                              * 
"""
)
# table = PrettyTable(['1'])
#     table.add_rows([123.0, 123.0, 12.0, 132.0])
#     print(table)
def println(field,value):

    len_field=len(field)
    len_value=len(value)
    sum_1 = 0
    sum_2 = 0
    for i in field:
        if i =='':
            sum_1+=1
    for j in value:
        if j=='':
            sum_2+=1
    if sum_1!=len_field and sum_2!=len_value:
        print(field,value)