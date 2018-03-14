package myProject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Preprocess {
	public static void main(String[] args) throws Exception {
		// getStrings(); //用正则表达式获取指定字符串内容中的指定内容
		// replace();
		ReadXML rx = new ReadXML();

		String path = "E:\\XML\\Version alteration";
		File XMLfile = new File(path);
		File[] tempList = XMLfile.listFiles();
		String bugDescripion = "";

		for (int i = 0; i < tempList.length; i++) {
			XMLfile = tempList[i];

			String[] sentences = rx.getSentences(XMLfile);
			String bugId = rx.getId(XMLfile);
			String bugTitle = rx.getTitle(XMLfile);

			/*
			 * String[] sentences = rx.getSigleXML(); String bugId=rx.getId();
			 * String bugTitle = rx.getTitle().toLowerCase();// 保存读取的原始xml
			 */
			// String stopwords = readStopWord();//暂时不用了。

			// for里面运行删减操作
			for (int n = 0; n < sentences.length; n++) {
				bugDescripion = sentences[n];
				
				bugDescripion = removeLog(bugDescripion);
				 bugDescripion = replaceHttp(bugDescripion);// 替换bug描述中的http网址

				 bugDescripion = replaceAddCharacter(bugDescripion);
				 bugDescripion = replaceAddress(bugDescripion);
				 bugDescripion = replaceIP(bugDescripion);
				 bugDescripion = replaceMACAndHash(bugDescripion);
				 bugDescripion = removeCharacter(bugDescripion);// 删除无效的特殊字符
				 bugDescripion = removeEnter(bugDescripion);
				 bugDescripion = removeLong(bugDescripion);
				 String[] stopwordArray = stopwordsToArray();// 保存stopwords到数组
				 bugDescripion = removeStopwords(bugDescripion, stopwordArray);// 保存了删除stopword的bug描述
				
				sentences[n] = bugDescripion;
				if (sentences[n].equals(""))
					sentences[n] = " ";
			}
			WriteXML wx = new WriteXML();
			wx.saveAsXML(bugId, bugTitle, sentences);
			System.out.println(i + 1);

		}
		System.out.println("preprocesse completed!");
	}

	private static String replaceHttp(String http) {
		Pattern pattern = Pattern
				.compile("(http://|https://|www){0,1}[^\u4e00-\u9fa5\\s]*?\\.(com|net|info|gov|edu|cn|de|org|me|html|tw|fr)[^\u4e00-\u9fa5\\s]*");
		// 空格结束
		Matcher matcher = pattern.matcher(http);
		String s = matcher.replaceAll("_website_");

		return s;
	}

	private static String removeLog(String str) {
		String[] lines = str.split("\n");
//
//		for (int i = 0; i < lines.length; i++) {
//			lines[i] += "\n";
//		}
		// String line = "";
		if (lines.length > 1) {
			for (int i = 0; i < lines.length; i++) {
				// line = lines[i];
				// System.out.println("line"+i+replacelog(line));
				// backup: (TRACE)|(=)|
				String regex = "(root@)"
						+ "|(\\)\\scopied,)"
						+ "|(records\\sout)"
						+ "|(records\\sin)"
						+ "|(Traceback)"
						+ "|(TRACE)|(=)"
						+ "|(return\\s(\\S)+\\()"
						+ "|(SKIP:)"
						+ "|(/[a-z]+/)"
						+ "|(\\d{1,4}[-|\\/|年|\\.]\\d{1,2}[-|\\/|月|\\.]\\d{1,2}([日|号])?(\\s)*(\\d{1,2}([点|时])?((:)?\\d{1,2}(分)?((:)?\\d{1,2}(秒)?(.\\d{3}?)?)?)?)?(\\s)*(PM|AM)?)"
						+ "|([0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})";
				Pattern pattern = Pattern.compile(regex);
				// 空格结束
				Matcher matcher = pattern.matcher(lines[i]);
				if (matcher.find()) {
					lines[i] = "";
					// System.out.println("...........");
				}
			}
			// String s = matcher.replaceAll(" ");
			// String newstr=new String(lines);
			StringBuffer sb = new StringBuffer();
			for (int i = 0; i < lines.length; i++) {
				if(lines[i].equals("")==false) {
					
				sb.append(lines[i]+"\n");
				}
			}
			String newstr = sb.toString();
			return newstr;
		} else {
			return str;
		}
	}

	private static String removeStopwords(String str, String[] arr) {
		String result = "";
		for (int i = 0; i < arr.length; i++) {
			String pattern = arr[i];
			Pattern r = Pattern.compile("[^\\w]" + pattern + "[^\\w]");
			Matcher m = r.matcher(str);
			str = m.replaceAll(" ");
			// test = test.replaceAll(pattern," ");
			result = str;

		}
		return result;

	}

	private static String[] stopwordsToArray() {
		File file = new File("unrelatedWords.txt");
		BufferedReader br = null;
		List<String> list = new ArrayList<String>();
		try {
			br = new BufferedReader(new FileReader(file));
			String str = null;
			while ((str = br.readLine()) != null) {
				list.add(str);
			}
			br.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
		return list.toArray(new String[0]);
	}

	private static String removeCharacter(String str) {// 删除特殊字符
		// str = str.replace('\n', ' ');// 删除回车键
		String regEx = "[`~!@#$%^&*|{}':'<>/~！@#￥%……&*（）_——+|{}【】‘；：”\"“’。，、？]";
		Pattern p = Pattern.compile(regEx);
		Matcher m = p.matcher(str);
		return m.replaceAll(" ");

	}

	private static String removeLongword(String str) {
		String[] words = str.split(" ");
		for (int i = 0; i < words.length; i++) {
			// int wordLength=words[i].length();
			String word = words[i];
			List<Object> array = new ArrayList<>();
			array.add(word);
			if (word.length() > 10) {
				// str=str.replace(words[i], ' ');
				System.out.println(word);
				// words[i]="";
				array.remove(i);
				return str;
			}
			// return str;

		}
		return str;
	}

	private static String removeLogByDate(String dateStr) {
		// List matches = null;
		String regex = "(\\d{1,4}[-|\\/|年|\\.]\\d{1,2}[-|\\/|月|\\.]\\d{1,2}([日|号])?(\\s)*(\\d{1,2}([点|时])?((:)?\\d{1,2}(分)?((:)?\\d{1,2}(秒)?(.\\d{3}?)?)?)?)?(\\s)*(PM|AM)?)|([0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})|(\\$)";
		Pattern p = Pattern.compile(regex, Pattern.CASE_INSENSITIVE
				| Pattern.MULTILINE);
		Matcher m = p.matcher(dateStr);
		String str = m.replaceAll("");
		// return m.replaceAll("");
		return str;
	}

	private static String replaceAddress(String ht) {
		// String http1 =
		// "wo ss http://www.zuidaima.com/sdfsdf.htm?aaaa=%ee%sss";
		// String http2 = "www.baidu.com";
		Pattern pattern = Pattern
				.compile("(/.*,)|(/.*:)|(/home.*.)|(/tmp.*/.rb)|(/var.*/.log)|(/etc.*/.local)|(root/@fuel.*//log)");
		// 空格结束
		Matcher matcher = pattern.matcher(ht);
		String s1 = matcher.replaceAll("");

		return s1;
	}

	private static String replaceAddCharacter(String add) {
		// String http1 =
		// "wo ss http://www.zuidaima.com/sdfsdf.htm?aaaa=%ee%sss";
		// String http2 = "www.baidu.com";
		Pattern pattern = Pattern.compile("([+]|[-]|[|])");
		// 空格结束
		Matcher matcher = pattern.matcher(add);
		String s2 = matcher.replaceAll("");

		return s2;
	}

	private static String replaceIP(String ip) {
		// String http1 =
		// "wo ss http://www.zuidaima.com/sdfsdf.htm?aaaa=%ee%sss";
		// String http2 = "www.baidu.com";
		Pattern pattern = Pattern
				.compile("(^(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|[1-9])\\."
						+ "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\."
						+ "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)\\."
						+ "(1\\d{2}|2[0-4]\\d|25[0-5]|[1-9]\\d|\\d)$)");
		// 空格结束
		Matcher matcher = pattern.matcher(ip);
		String s3 = matcher.replaceAll("");

		return s3;
	}

	// 删除mac和hash
	private static String replaceMACAndHash(String mac) {
		// String http1 =
		// "wo ss http://www.zuidaima.com/sdfsdf.htm?aaaa=%ee%sss";
		// String http2 = "www.baidu.com";
		Pattern pattern = Pattern
				.compile("((([A-Fa-f0-9]{2}:){5}[A-Fa-f0-9]{2})|([A-Za-z0-9]{32,}))");
		// 空格结束
		Matcher matcher = pattern.matcher(mac);
		String s4 = matcher.replaceAll("");

		return s4;
	}

	private static String removeEnter(String str) {
		Pattern pattern = Pattern.compile("\\s+");
		// 空格结束
		Matcher matcher = pattern.matcher(str);
		String s1 = matcher.replaceAll(" ");
		return s1;

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

	private static String removeLong(String str) {
		Pattern pattern = Pattern.compile("(\\S){15,}");
		// 空格结束
		Matcher matcher = pattern.matcher(str);
		String s = matcher.replaceAll("");

		return s;
	}

}
