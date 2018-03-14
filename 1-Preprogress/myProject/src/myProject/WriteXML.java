package myProject;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;
import org.w3c.dom.Element;

public class WriteXML {

	public void saveAsXML(String bugId, String bugTitle, String[] bugDescription) throws Exception {

		DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
		DocumentBuilder builder = factory.newDocumentBuilder();
		Document document = builder.newDocument();
		// Element bug = document.createElement("bug");
		Element bug = document.createElement("bug");
		bug.setAttribute("id", bugId);
		Element title = document.createElement("title");
		title.setTextContent(bugTitle);
		bug.appendChild(title);

		Element description = document.createElement("description");
		bug.appendChild(description);

		for (int i = 0; i < bugDescription.length; i++) {
			Element sentence = document.createElement("sentence");
			if (bugDescription[i] == "")
				bugDescription[i] = "temp";
			sentence.setTextContent(bugDescription[i]);
			// while (sentence != null)
			description.appendChild(sentence);

		}
		document.appendChild(bug);

		TransformerFactory tff = TransformerFactory.newInstance();
		// 创建Transformer对象
		Transformer tf = tff.newTransformer();
		// 使用Transformer的transform()方法将DOM树转换成XML
		// tf.setAttribute("indent-number", new Integer(2));
		tf.setOutputProperty(OutputKeys.INDENT, "yes");
		// tf.setOutputProperty(OutputKeys.OMIT_XML_DECLARATION, "yes");
		// tf.setOutputProperty(OutputKeys.ENCODING, "UTF-8");
		document.setXmlStandalone(true);
		String path = "E:\\XML_OUT\\Version alteration\\";
		tf.transform(new DOMSource(document), new StreamResult(path + "bug" + bugId + ".xml"));

	}
}
