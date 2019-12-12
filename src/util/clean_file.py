# file used for cleaning dataset

# remove duplicates within each row

import pandas as pd

# load the external file
df = pd.read_csv('src/util/SomeFoodEx2Codes.csv', low_memory=False)

# create the final dataframe to save
columns = ['btCode']
for i in range(1, 34):  # 33 fc + 1 bt
    columns.append('F'+format(i, '0>2'))  # fill gap

final_df = pd.DataFrame(index=df.index, columns=columns)
final_df['btCode'] = df['btCode']

# drop first col
df.drop('btCode', axis=1, inplace=True)

# print(df.head(10))

# for each row remove duplicates
for index, row in df.iterrows():
    # remove nan values
    cleanedList = [x for x in row if str(x) != 'nan'] 

    # iterate items in cleaned list
    for item in cleanedList:
        facet = item.split('.')
        temp = final_df.loc[index, facet[0]]
        if(pd.isna(temp)): # if nan just copy
            temp = facet[1]
        elif(facet[1] not in temp): # else concat
            temp += "; "+facet[1]

        final_df.at[index, facet[0]]=temp
    

final_df.to_csv('src/util/FoodEx2Hist.csv', index=False)
