import pandas as pd 

df = pd.read_csv('src/japan_meigara.csv',encoding='shift-jis',usecols=[1])

ind = 0

codes = df.values.tolist()
meigara = ""

path = 'src/japan_meigara.txt'

with open(path, mode='w') as file:
    for i in df.index:
        # ind += 1
        # if ind == 10:
        #     break
        code = '\"'+str(codes[i][0])+'.T\",'+'\n'
        file.write(code)
        print(codes[i][0])