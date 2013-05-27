package org.nipun.bd.storm;

import java.net.Inet4Address;
import java.net.UnknownHostException;

import org.hyperic.sigar.Sigar;
import org.hyperic.sigar.SigarException;

public class SystemInformation {
	private static Sigar nativeSigar = null;

	public SystemInformation() {
		nativeSigar = new Sigar();
	}

	long getProcessId() {
		return nativeSigar.getPid();
	}

	String getFQDN() {
		String host = "<Unable to get Host Name>";
		try {
			host = Inet4Address.getLocalHost().getHostAddress();
		} catch (UnknownHostException e) {
			try {
				host = nativeSigar.getFQDN();
			} catch (SigarException e1) {
			}
		}
		return host;
	}

}
