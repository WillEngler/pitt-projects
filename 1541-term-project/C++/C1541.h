#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <iostream>
#include <map>
#include <utility>
#include <algorithm>


using std::vector;
using std::string;
using std::map;

int DEFAULT = 0;


//String splitting code adapted from Stack Overflow community wiki: http://stackoverflow.com/questions/236129/split-a-string-in-c

vector<string> split(const string &s, char delim) {
    vector<string> elems;
    std::stringstream ss(s);
    string item;

    while (std::getline(ss, item, delim)) {
        elems.push_back(item);
    }
    return elems;
}

//End code adapted from Stack overflow

vector<string> fileIntoVec(const string fname,const int bufferSize)
{
	//Create strem to read input from
	std::ifstream input(fname);
	if (bufferSize != DEFAULT)
	{
		char buffer[bufferSize];
		input.rdbuf()->pubsetbuf(buffer,bufferSize);
	}
	//Create vector to read input into
	vector<string> contents;

	string line;
	while (std::getline(input,line))
	{
		contents.push_back(line);
	}
	return contents;
}

vector<string> csvIntoVec(const string fname,const int bufferSize)
{
	auto raw = fileIntoVec(fname,bufferSize);
	return split(raw.front(),',');
}

void vecIntoFile(const vector<string> vec, const string fname,const int bufferSize)
{
	std::ofstream output(fname);
	if (bufferSize != DEFAULT)
	{
		char buffer[bufferSize];
		output.rdbuf()->pubsetbuf(buffer,bufferSize);
	}
	for (auto line : vec)
	{
		output << line << std::endl;
	}
}

void findAndReplace(string &substrate, const string toFind, const string replacement )
{
	//Begin searching at position 0
	std::size_t startPos = 0;
	std::size_t matchPos;

	while ( (matchPos = substrate.find(toFind,startPos)) != string::npos)
	{
		substrate.replace(matchPos,toFind.length(),replacement);
		startPos = matchPos + toFind.length();
	}
}

map<string,string> mapToNowhere(const string csvfname,const int bufferSize)
{
	auto values = csvIntoVec(csvfname,bufferSize);
	map<string,string> cheatMap;
	for (auto value : values)
	{
		cheatMap.insert(std::pair<string,string>(value,""));
	}

	return cheatMap;
}

map<string,string> mapToSomewhere(const string csvfname,const int bufferSize)
{
	auto values = csvIntoVec(csvfname,bufferSize);
	if ( (values.size() % 2) != 0 )
	{
		std::cout << "CSV file must have an even number of values." << std::endl;
		exit(1);
	}

	map<string,string> replaceMap;
	for (int i = 0; i < values.size(); i = i + 2)
	{
		replaceMap.insert(std::pair<string,string>(values[i],values[i+1]));
	}

	return replaceMap;
}

void replaceInAllLines(vector<string> &list, const map<string,string> replaceMap)
{
	for (auto pair : replaceMap)
	{
		std::for_each(list.begin(),list.end(), [&pair] (string &s) {findAndReplace(s,pair.first,pair.second);});
	}
}

