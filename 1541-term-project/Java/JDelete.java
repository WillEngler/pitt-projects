import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.io.*;

class JDelete 
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
			System.out.println("Expected usage: JDelete <file to modify> <CSV file of phrases to delete>");
			System.exit(1);
		}

		//Read the target file into a list
		String targetFileName = args[0];
		Path targetFile = Paths.get(targetFileName);
		List<String> target = J1541.popFile(targetFileName);
		
		//Read the CSV file into a set
		Set<String> phrases = J1541.csvAsSet(args[1]);		

		//Delete all of the phrases
		deleteOccurrences(phrases,target);
		
		//Recreate the file and write to it
		J1541.pushFile(targetFile,target);

		long finish = System.nanoTime();

		System.out.printf("Time elapsed: %d milliseconds.\n",(finish-start)/1000000);
	}

	public static void deleteOccurrences(Set<String> phrases, List<String> target)
	{

		for (String phrase : phrases)
		{
			//Create a regex pattern for each phrase to be deleted
			Pattern pattern = Pattern.compile(phrase);

			for (int i =0; i < target.size(); i++)
			{
				//Split each string around the regex 
				String line = target.get(i);
				String[] tokens = pattern.split(line);

				//Construct a new string from the regex-delimited tokens
				String replacement = "";
				for (int j=0; j < tokens.length; j++)
				{
					replacement = replacement + tokens[j];
				}

				//And replace the old string with the new string
				target.set(i,replacement);
				//System.out.println(replacement);
			} 
			
		}	

	}



}