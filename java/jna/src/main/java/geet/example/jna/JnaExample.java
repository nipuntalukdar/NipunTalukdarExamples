/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: JnaExample.java,v 1.0 May 27, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.jna;

/*
 *  @author Nipun Talukdar
 *  @version $Id: JnaExample.java,v 1.0 May 27, 2014 1:53:05 PM
 */

public class JnaExample {
	public static void main(String[] args) {
		try {
			System.out.println(System.getProperty("java.library.path"));
			System.out.println(CLibrary.INSTANCE.getpid());
			System.out.println(CLibrary.INSTANCE.getppid());
			long[] timenul = new long[1];
			System.out.println(CLibrary.INSTANCE.time(timenul));
		} catch (UnsatisfiedLinkError e) {
			System.out.println("Exception" + e);
		}
	}
}
