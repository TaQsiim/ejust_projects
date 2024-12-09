#include <bits/stdc++.h>
#include "DataStructureForTheAssembler.h"
using namespace std;

unordered_map<string, string> INSTRUCTION_SET = {
    {"AND", "000"}, {"ADD", "001"}, {"LDA", "010"}, {"STA", "011"},
    {"BUN", "100"}, {"BSA", "101"}, {"ISZ", "110"},

    {"CLA", "0111100000000000"}, {"CLE", "0111010000000000"}, 
    {"CMA", "0111001000000000"}, {"CME", "0111000100000000"}, 
    {"CIR", "0111000010000000"}, {"CIL", "0111000001000000"},
    {"INC", "0111000000100000"}, {"SPA", "0111000000010000"},
    {"SNA", "0111000000001000"}, {"SZA", "0111000000000100"}, 
    {"SZE", "0111000000000010"}, {"HLT", "0111000000000001"},

    {"INP", "1111100000000000"}, {"OUT", "1111010000000000"},
    {"SKI", "1111001000000000"}, {"SKO", "1111000100000000"},
    {"ION", "1111000010000000"}, {"IOF", "1111000001000000"}
};

unordered_map<string, string> SYMBOL_TABLE ;
string machineCode="\nMachine Code: \n";

string decToBin(string operand)
{
    int num = stoi(operand);
    string binary = bitset<16>(num).to_string();
    // machineCode += binary + "\n";
    // bitset<16 > (n).to_string();
    // cout << "Binary: " << binary << endl;
    return binary;
}

string hexToBin(string operand)
{
    int num = stoi(operand, nullptr, 16);
    string binary = bitset<16>(num).to_string();
    // cout << "Binary: " << binary << endl;
    // machineCode += binary + "\n";
    return binary;
}

void firstPass(vector<Cracker> lines)
{
    int LC = 0;
    for(auto line:lines)
        {
            if(!line.label.empty())
            {
                SYMBOL_TABLE[line.label] = to_string(LC);
            }else if(line.opcode == "ORG")
            {
                LC = stoi(line.operand) -1;
            }else if(line.opcode == "END")
            {
                break;
            }
            LC++;
        }
        cout << "Symbol Table: " << endl;
        for(auto symbol:SYMBOL_TABLE)
        {
            cout << symbol.first << " " << symbol.second << endl;
        }
}

void secondPass(vector<Cracker> lines)
{
    int lc = 0;
    for(auto line:lines)
    {
        if(line.opcode == "ORG" || line.opcode == "HEX" || line.opcode == "DEC" ||line.opcode == "END")
        {
            if (line.opcode == "ORG" )
                lc = stoi(line.operand);
            else if (line.opcode == "END")
                break;
            else if(line.opcode == "DEC")
                {
                    machineCode += to_string(lc) + ": " ;
                    machineCode += decToBin(line.operand) + "\n";
                    lc++;
            }else{
                    machineCode += to_string(lc) + ": " ;
                    machineCode += hexToBin(line.operand) + "\n";
                    lc++;
            }
        }else 
        {
            if(line.opcode == "ADD" || line.opcode == "AND" || line.opcode == "LDA" || line.opcode == "STA" || line.opcode == "BUN" || line.opcode == "BSA" || line.opcode == "ISZ" )
                {
                    machineCode += to_string(lc) + ": " + line.I + INSTRUCTION_SET[line.opcode]; 
                    machineCode += hexToBin(SYMBOL_TABLE[line.operand]).substr(4, 12) + "\n";
                }
            else if (line.opcode == "CLA" || line.opcode == "CLE" || line.opcode == "CMA" || line.opcode == "CME" || line.opcode == "CIR" || line.opcode == "CIL" || line.opcode == "INC" || line.opcode == "SPA" || line.opcode == "SNA" || line.opcode == "SZA" || line.opcode == "SZE" || line.opcode == "HLT" || line.opcode == "INP" || line.opcode == "OUT" || line.opcode == "SKI" || line.opcode == "SKO" || line.opcode == "ION" || line.opcode == "IOF")
                machineCode += to_string(lc) + ": " + INSTRUCTION_SET[line.opcode] + "\n";
            else
                throw "Invalid Opcode" ;
            lc++;
        
        }
    }
}

void displayMachineCode()
{
    cout << machineCode << endl;
}

void assemble(vector<Cracker> lines)
{
    firstPass(lines);
    secondPass(lines);
    displayMachineCode();
}

int main()
{
    string line;
    vector<string> raw_lines;
    vector<Cracker> lines;

while (getline(cin, line) && !line.empty())
    {
        raw_lines.push_back(line);
    }

for(auto line:raw_lines)
{
    Cracker l = Cracker(line);
    lines.push_back(l) ;
    // cout << l.label << ", " << l.opcode << "<-opcode" << l.operand << "<-operand I:" << l.I << endl;
}
assemble(lines);


}

// ORG 100
// LDA SUB
// CMA
// INC
// ADD MIN
// STA DIF
// HLT
// MIN, DEC 83
// SUB, DEC -23
// DIF, HEX 0
// END
