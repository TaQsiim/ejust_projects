#pragma once

#include<bits/stdc++.h>
using namespace std;

static inline void ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {
        return !std::isspace(ch);
    }));
}

// Trim from end (in place)
static inline void rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
        return !std::isspace(ch);
    }).base(), s.end());
}

// Trim from both ends (in place)
static inline void trim(std::string &s) {
    ltrim(s);
    rtrim(s);
}

void doNothing()
{
    return;
}

class  Cracker{
    public:
    string label ="" ,opcode ="" ,operand ="" ,I="0";

    Cracker(string Line)
    {
        string localLine = Line;
        trim(localLine);
        getLabel(localLine);
        getOpcodeOperand(localLine);
        getOperand(localLine);
        getI(localLine);
        doNothing();
    }

void getI(string &localLine)
{
    if(localLine[0] == 'I')
        I = "1";

}

void getLabel(string &localLine)
{

    if(checkForLAbel(localLine)) //return True if there is a label
    {
        for(auto& L:localLine)
            {
                if( L == ',')
                {
                    break;
                }
                label += L;
            }
            localLine = localLine.substr(label.size()+1);
            ltrim(localLine);
    }
}

void getOpcodeOperand(string &localLine)
{
    for(auto& L:localLine)
        {
            if( L == ' ')
            {
                break;
            }
            opcode += L;
        }
        localLine = localLine.substr(opcode.size());
        ltrim(localLine);
}

void getOperand(string &localLine)
{
            for(auto& L:localLine)
        {
            if( L == '/' || L == ' ')
            {
                localLine = localLine.substr(operand.size()+1);
                break;
            }
            operand += L;
        }
    }

bool checkForLAbel(string localLine)
{
    for(auto line:localLine)
        if (line == ',')
            return true;
    return false;
}

};
