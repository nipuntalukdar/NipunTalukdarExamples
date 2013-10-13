/*
 * ==================================================================================================================
 *  2013, Oct 13, 2013
 *  ------------------
 *  @author Nipun Talukdar 
 
 * ==================================================================================================================
 */
package geet.examples.org;

/*
 *  @author Nipun Talukdar 
 *  Example codes from NipunTalukdar
 */

public class Utility {
	public static void Sleep(long millsec){
		try {
			Thread.sleep(millsec);
		} catch (InterruptedException e){
		}
	}
}
