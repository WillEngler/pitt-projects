import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.io.*;

class JReplace
{
	public static void main(String[] args)
	{
		long start = System.nanoTime();

		//Need to open 2 files specified on the command line
		//CSV of phrases to delete
		//File from which to delete phrases
		//Need to regex for occurrence of desired stirng?

		if (args.length != 2)
		{
			System.out.println("Expected usage: JReplace <file to modify> <CSV file of phrases to find and replace>");
			System.exit(1);
		}

		String targetFileName = args[0];
		List<String> target = J1541.popFile(targetFileName);
		
		//Read the CSV file into a map from phrases to find
		//to phrases to replace 
		Map<String,String> phraseMap = csvAsMap(args[1]);	

		//Replace all of the phrases
		replaceOccurrences(phraseMap,target);
		
		//Replace the file
		Path targetFile = Paths.get(targetFileName);
		J1541.pushFile(targetFile,target);

		long finish = System.nanoTime();

		System.out.printf("Time elapsed: %d milliseconds.\n",(finish-start)/1000000);
	}
	public static Map<String,String> csvAsMap (String fname)
	{
		//Load the CSV into an array
		List<String> raw = J1541.fileAsList(fname);
		String[] values = raw.get(0).split(",");
		if ((values.length % 2) != 0)
		{
			System.out.println("CSV file must contain an even number of values.");
			System.exit(1);
		} 

		//Load the values into a map
		HashMap<String,String> phraseMap = new HashMap<String,String>();
		for (int i = 0; i < values.length; i = i+2 )
		{
			phraseMap.put(values[i],values[i+1]);
		}

		return phraseMap;
	}
	public static void replaceOccurrences(Map<String,String> phrases, List<String> target)
	{

		for (String toReplace : phrases.keySet())
		{
			for (int i =0; i < target.size(); i++)
			{
				String line = target.get(i);
				target.set(i,line.replace(toReplace,phrases.get(toReplace)));
			} 
			
		}	

	}
}