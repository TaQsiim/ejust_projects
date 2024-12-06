#اي run mn "testscript.py" file
class Assembler(object):
    def __init__(self, asmpath='', mripath='', rripath='', ioipath='') -> None:
        super().__init__()
       #{symbol: location}
        self.__address_symbol_table = {}
        #{location: binary representation}
        self.__bin = {}
        # Load assembly code if the asmpath argument was provided.
        if asmpath:
            self.read_code(asmpath)   
        # memory-reference instructions
        self.__mri_table = self.__load_table(mripath) if mripath else {}
        # register-reference instructions
        self.__rri_table = self.__load_table(rripath) if rripath else {}
        # input-output instructions
        self.__ioi_table = self.__load_table(ioipath) if ioipath else {}
    
#read instruction file must end with asm or s
    def read_code(self, path:str):
        assert path.endswith('.asm') or path.endswith('.S'), \
                        'file provided does not end with .asm or .S'
        self.__asmfile = path.split('/')[-1] #بيقسم  عند كل / وبياخد العنصر الاخير )اسم الملف()
        with open(path, 'r') as f:
            # remove '\n' from each line, convert it to lower case, and split
            # it by the whitespaces between the symbols in that line.
            self.__asm = [s.rstrip().lower().split() for s in f.readlines()]
#s.rstrip() بيشيل space
#make it in lower case
#يقسم النص إلى قائمة من الكلمات
#مثال لو هو
#ORG 100 /starting location
#CLE     / clear E
#CLA
#هيبقي 
#self.__asm = [
  #  ['org', '100', '/starting', 'location'],
  #  ['cle', '/clear', 'e'],
  #  ['cla']
#]

    def assemble(self, inp='') -> dict:
 #check 3al last step
        assert self.__asm or inp, 'no assembly file provided'
        if inp:
            assert inp.endswith('.asm') or inp.endswith('.S'), \
                        'file provided does not end with .asm or .S'
        # if assembly file was not loaded, load it.
        if not self.__asm:
            self.read_code(inp)

        self.__rm_comments()
        self.__first_pass()
        self.__second_pass()
        return self.__bin


    def __load_table(self, path) -> dict:
        with open(path, 'r') as f:
            t = [s.rstrip().lower().split() for s in f.readlines()]
        return {opcode:binary for opcode,binary in t}
#بنستخدمها مع mri w rri w ioi files 
#يعني لو كدا add 0001
#sub 0010
#mul 0011
#هيكون كدا {'add': '0001', 'sub': '0010', 'mul': '0011'}
    def __islabel(self, string) -> bool:
        return string.endswith(',')


    def __rm_comments(self) -> None:
        for i in range(len(self.__asm)): #هيعدي علي كل سطر
            for j in range(len(self.__asm[i])): #هيعدي علي كل كلمه
                if self.__asm[i][j].startswith('/'):
                    del self.__asm[i][j:] #لو comment هيمسح كل الكلام الي بعدو
                    break

#لو كدا
 #ORG 100 /starting location
#CLE     /clear accumulator
#CLA
#هيبقي كدا 
#[
   # ['org', '100'],
    #['cle'],
    #['cla']
#]


    def __format2bin(self, num: str, numformat: str, format_bits: int) -> str:
   
        if numformat == 'dec': 
            value = int(num) 
        elif numformat == 'hex':  
            value = int(num, 16)  
        else:
            raise Exception('format2bin: not supported format provided.')

    # for -ve num
        if value < 0:
            value = (1 << format_bits) + value #2' complement
    
    # chech el value sa7
        if value < 0 or value >= (1 << format_bits):
            raise ValueError(f"Number {num} out of range for {format_bits} bits.")
    
   #return num 
        return '{:0{width}b}'.format(value, width=format_bits)
   


    def __first_pass(self) -> None:
      #علشان امشي علي كل ال lines 
        lc=0
        for i in range(len(self.__asm)): #علشان يعدي علي كل سطر متخزن ف self.__asm
            #لو طلع label 
            if(self.__islabel(self.__asm[i][0])): #check awel word
                self.__address_symbol_table[self.__asm[i][0][0:3]]=self.__format2bin(str(lc),'dec',12) #علشان يعدي علي حرف حرف و asm biggest list i , 0for child  child of child w 12 3l4an el address 12 bit 
                lc+=1  # استخراج (بدون الفاصلة) [0:3] (زي: ROT, → ROT).
            elif self.__asm[i][0]=="org":
                lc=int(self.__asm[i][1],16) # UPDATE EL LC BL elrakam el ganb el org / 16 3l4an y'5aleeh binary
            elif self.__asm[i][0]=="end":
                print("Symbol Table: \n",self.__address_symbol_table)
                return
            #Skip by increment
            else:
               lc+=1 
                
#هتشيك اني صح ب print(self.__address_symbol_table) بعد end case 
     
#بعد ده المفروض
#ORG 100
#ROT, CIL /start rotating AC
#AGN, CLE
#STA CTR
#END
#يبقي
#Symbol Table:{'rot': '000100000000', 'agn': '000100000001'}

    #INSTRUCTION TO BIN
    def __second_pass(self) -> None:
        lc=0
        for i in range(len(self.__asm)): #check the 4 sudoinsctruction (org , dec  hex . end)
            if (self.__asm[i][0]=='org'):
                lc=int(self.__asm[i][1],16) #set lc = org , 1 for 100
            elif (self.__asm[i][0]=='end'):
                return
            elif len(self.__asm[i])>2 and (self.__asm[i][1]=='dec'):#check > 2 ? 3l4an hex lazem ba3do instruction w ablo label so 2 is min len
                self.__bin[self.__format2bin(str(lc),'dec',12)]= self.__format2bin(str(self.__asm[i][2]),'dec',16) #dec to binary and store IN BINit
                lc+=1
                         
            elif len(self.__asm[i])>2 and (self.__asm[i][1]=='hex'):
                self.__bin[self.__format2bin(str(lc),'dec',12)]= self.__format2bin(str(self.__asm[i][2]),'hex',16)
                lc+=1
                #بيشوف لو اول INDEX LABEL فياخد تاني واحد IF NOT هياخد الاول
            instruction=self.__asm[i][1] if self.__islabel(self.__asm[i][0]) else self.__asm[i][0]
            bit_15 ='0' #direct
            
            if instruction in self.__mri_table.keys():# 'cil': '0111', ال للجزء KEY الي علي الشمال
                address=str(self.__address_symbol_table[self.__asm[i][1]])
                opcode= str(self.__mri_table[instruction])
                self.__bin[self.__format2bin(str(lc),'dec',12)]= bit_15 + opcode + address
                lc+=1
            elif instruction in self.__rri_table.keys():
                self.__bin[self.__format2bin(str(lc),'dec',12)]=str(self.__rri_table[instruction])
                lc+=1
            elif instruction in self.__ioi_table.keys():   
                self.__bin[self.__format2bin(str(lc),'dec',12)]=str(self.__ioi_table[instruction])
                lc+=1
    

