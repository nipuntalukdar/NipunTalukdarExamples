/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: SimpleData.java,v 1.0 Jun 8, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.hazel;

import java.io.Serializable;

/*
 *  @author Nipun Talukdar
 *  @version $Id: SimpleData.java,v 1.0 Jun 8, 2014 9:50:58 AM
 */

public class SimpleData implements Serializable{
	private int value;
	private static final long serialVersionUID = 123400L;

	public SimpleData(int value) {
		this.value = value;
	}
	public SimpleData() {
		this.value = 0;
	}
	public int getValue() {
		return value;
	}
	public void setValue(int value) {
		this.value = value;
	}
	
}
