package myProject;

import java.io.File;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;

public class ReadXML {
	
/**
	public void getSigleXML() throws Exception {
		String path = "F:\\XML";
		File XMLfile = new File(path);
		File[] tempList = XMLfile.listFiles();
		for (int i = 0; i < tempList.length; i++) {
			XMLfile = tempList[i];
			getSentences(XMLfile);
			getId(XMLfile);
			getTitle(XMLfile);
			// return XMLfile;
		}
	}
*/
	public String[] getSentences(File file) throws Exception {

		// File f = new File("test.xml");
		//
		File f = file;
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = factory.newDocumentBuilder();
		Document doc = builder.parse(f);
		NodeList nl = doc.getElementsByTagName("sentence");
		String[] sentences = new String[nl.getLength()];
		// System.out.println(nl.getLength());
		for (int i = 0; i < nl.getLength(); i++) {
			String sentence = doc.getElementsByTagName("sentence").item(i)
					.getFirstChild().getNodeValue();
			sentences[i] = sentence;

		}
		return sentences;
	}

	public String getId(File file) throws Exception {
		File f = file;
		// File f = new File("test.xml");
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = factory.newDocumentBuilder();
		Document doc = builder.parse(f);
		NodeList id = doc.getElementsByTagName("id");
		for (int m = 0; m < id.getLength(); m++) {
			String bugId = id.item(m).getFirstChild().getNodeValue();
			// System.out.println(bugId);
			return bugId;
		}
		return null;
	}

	public String getTitle(File file) throws Exception {
		File f = file;
		// File f = new File("test.xml");
		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = factory.newDocumentBuilder();
		Document doc = builder.parse(f);
		NodeList title = doc.getElementsByTagName("title");
		for (int n = 0; n < title.getLength(); n++) {
			String bugTitle = title.item(n).getFirstChild().getNodeValue();
			// System.out.println(bugTitle);
			return bugTitle;
		}
		return null;

	}
}
