#include "C1541.h"
#include <chrono>
using std::cout;




int main(int argc, char const *argv[])
{
	int bufferSize = DEFAULT;

	//Timing code adapted from Rapptz's response at http://stackoverflow.com/questions/12231166/timing-algorithm-clock-vs-time-in-c
	auto start = std::chrono::high_resolution_clock::now();

	if (argc < 3)
	{
		cout << "Expected two filenames as arguments" << std::endl;
		return 1;
	}
	auto targetName = string(argv[1]);
	auto csvName = string(argv[2]);

	if (argc == 4)
	{
		bufferSize = std::stoi(argv[3]);
	}
	else
	{
		bufferSize = DEFAULT;
	}

	auto contents = fileIntoVec(targetName,bufferSize);
	auto replaceMap = mapToSomewhere(csvName,bufferSize);

	replaceInAllLines(contents,replaceMap);
	vecIntoFile(contents,targetName,bufferSize);

	auto finish = std::chrono::high_resolution_clock::now();
	std::cout << "Time elapsed: "
              << std::chrono::duration_cast<std::chrono::milliseconds>(finish-start).count()
              << " milliseconds\n";

	return 0;
}