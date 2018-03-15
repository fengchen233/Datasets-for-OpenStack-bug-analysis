package myProject;

import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TempFunc {

	public static void main(String[] args) throws Exception {

		String str = " dsds1212ffff311111 a dfdfda 012345678945454";
		System.out.println(removeLong(str));
		//System.out.println(removeLongwords(str));
	}

		private static String removeLong(String str) {
			Pattern pattern = Pattern
					.compile("(\\S){15,}");
			// ¿Õ¸ñ½áÊø
			Matcher matcher = pattern.matcher(str);
			String s = matcher.replaceAll("");

			return s;
		}
		private static String removeLongwords(String str) {
			// str = replaceHttp(str);
			// System.out.println(str);
			String words[] = str.split(" ");
			String emptyStr = "";
			for (int i = 0; i < words.length; i++) {
				// System.out.println(words[i]+"\n...........................");
				emptyStr = words[i];
				if (emptyStr.length() > 11) {
					words[i] = "";
					// System.out.println();
				}
			}

			return Arrays.toString(words);

		}		
}
