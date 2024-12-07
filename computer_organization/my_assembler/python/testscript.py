from assembler import Assembler

INPUT_FILE = 'testcode.asm'
OUT_FILE = 'testcode.mc'
MRI_FILE = 'mri.txt'
RRI_FILE = 'rri.txt'
IOI_FILE = 'ioi.txt'

if __name__ == "__main__":
    bin_text = ''
    asm = Assembler(asmpath=INPUT_FILE, \
                    mripath=MRI_FILE, \
                    rripath=RRI_FILE, \
                    ioipath=IOI_FILE)
    print('\n','Assembling...','\n')
    print("------------------------------------")
    binaries = asm.assemble()
    for lc in binaries:
        bin_text += lc + '\t' + binaries[lc] + '\n'
  
    print("Machine language:")
    print(bin_text)
    #print(binaries)
     # with open(OUT_FILE, 'r') as f:
    #     print('TEST PASSED' if f.read() == bin_text else 'TEST FAILED')
    
    if(open(OUT_FILE, 'r').read() == bin_text):
        print("TEST PASSED")
    else:
        print("TEST FAILED")
