/*
 * ==================================================================================================================
 *  @author Nipun Talukdar <a href="mailto:nipun.talukdar@gmail.com">nipun.talukdar@gmail.com</a>
 *  @version $Id: CLIbrary.java,v 1.0 May 27, 2014 
 *  
 * ==================================================================================================================
 */
package geet.example.jna;

import com.sun.jna.Library;
import com.sun.jna.Native;

/*
 *  @author Nipun Talukdar
 *  @version $Id: CLIbrary.java,v 1.0 May 27, 2014 1:55:47 PM
 */

public interface CLibrary extends Library {
	CLibrary INSTANCE = (CLibrary) Native.loadLibrary("c", CLibrary.class);
	
	int getpid();

	int getppid();

	long time(long buf[]);

}
