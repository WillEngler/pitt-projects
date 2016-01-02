import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
import java.io.*;

class J1541
{
	public static void pushFile(Path file, List<String> target)
	{
		//Recreate the file and write to it
		try
		{
			Files.write(file,target);
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
	}

	public static List<String> popFile(String fname)
	{
		//Read the target file into a list
		List<String> target = J1541.fileAsList(fname);

		//Delete the file
		Path targetFile = Paths.get(fname);
		try
		{
			Files.delete(targetFile);
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}

		return target;
	}


	public static List<String> fileAsList(String fname)
	{
		Path targetFileName = Paths.get(fname);
		List<String> targetLines = new ArrayList<String>();

		try
		{
			targetLines = Files.readAllLines(targetFileName);
		}
		catch (IOException exc)
		{
			exc.printStackTrace();
		}
		return targetLines;
	}

	public static Set<String> csvAsSet(String fname)
	{
		List<String> raw = fileAsList(fname);
		String[] valueList = raw.get(0).split(",");
		HashSet<String> valueSet = new HashSet<String>(); 
		
		for (String phrase : valueList)
		{
			valueSet.add(phrase);
		}
		return valueSet;

	}

}

